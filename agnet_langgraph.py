import os
from typing import List, Dict, Any, TypedDict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentFinish
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import HumanMessage, AIMessage
from langchain_core.messages import SystemMessage
from langchain.tools.render import format_tool_to_openai_function
from langgraph.graph import StateGraph, END
from beckn_requests import search, select, init, confirm, status, track, cancel, support

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-api-key"

# FastAPI app instance
app = FastAPI()

# Define request models for each API call
class SearchRequest(BaseModel):
    item: str
    delivery_location: str

class SelectRequest(BaseModel):
    bpp_id: str
    bpp_uri: str
    provider_id: str
    item_id: str

class InitRequest(BaseModel):
    bpp_id: str
    bpp_uri: str
    provider_id: str
    item_id: str
    billing_info: Dict[str, Any]
    delivery_info: Dict[str, Any]

class ConfirmRequest(BaseModel):
    bpp_id: str
    bpp_uri: str
    provider_id: str
    item_id: str
    billing_info: Dict[str, Any]
    delivery_info: Dict[str, Any]
    payment_info: Dict[str, Any]

class StatusRequest(BaseModel):
    bpp_id: str
    bpp_uri: str
    order_id: str

class TrackRequest(BaseModel):
    bpp_id: str
    bpp_uri: str
    order_id: str

class CancelRequest(BaseModel):
    bpp_id: str
    bpp_uri: str
    order_id: str

class SupportRequest(BaseModel):
    bpp_id: str
    bpp_uri: str
    order_id: str

# Define the tools with Beckn API requests, including status, track, cancel, and support
tools = [
    Tool(
        name="Search",
        func=lambda item, location: search(item, location),
        description="Use this to search for items. Input is the item name and delivery location (GPS coordinates)."
    ),
    Tool(
        name="Select",
        func=lambda bpp_id, bpp_uri, provider_id, item_id: select(bpp_id, bpp_uri, provider_id, item_id),
        description="Use this to select an item. Input is bpp_id, bpp_uri, provider_id, and item_id."
    ),
    Tool(
        name="Init",
        func=lambda bpp_id, bpp_uri, provider_id, item_id, billing_info, delivery_info: init(
            bpp_id, bpp_uri, provider_id, item_id, billing_info, delivery_info),
        description="Use this to initialize an order. Input is bpp_id, bpp_uri, provider_id, item_id, billing and delivery info."
    ),
    Tool(
        name="Confirm",
        func=lambda bpp_id, bpp_uri, provider_id, item_id, billing_info, delivery_info, payment_info: confirm(
            bpp_id, bpp_uri, provider_id, item_id, billing_info, delivery_info, payment_info),
        description="Use this to confirm an order. Input is bpp_id, bpp_uri, provider_id, item_id, billing, delivery, and payment info."
    ),
    Tool(
        name="Status",
        func=lambda bpp_id, bpp_uri, order_id: status(bpp_id, bpp_uri, order_id),
        description="Use this to check the status of an order. Input is bpp_id, bpp_uri, and order_id."
    ),
    Tool(
        name="Track",
        func=lambda bpp_id, bpp_uri, order_id: track(bpp_id, bpp_uri, order_id),
        description="Use this to track an order. Input is bpp_id, bpp_uri, and order_id."
    ),
    Tool(
        name="Cancel",
        func=lambda bpp_id, bpp_uri, order_id: cancel(bpp_id, bpp_uri, order_id),
        description="Use this to cancel an order. Input is bpp_id, bpp_uri, and order_id."
    ),
    Tool(
        name="Support",
        func=lambda bpp_id, bpp_uri, order_id: support(bpp_id, bpp_uri, order_id),
        description="Use this to request support for an order. Input is bpp_id, bpp_uri, and order_id."
    )
]

# Create the agent LLM
llm = ChatOpenAI(temperature=0)

# Define the prompt for the agent
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="You are a helpful AI assistant that helps users order items using the Beckn protocol."),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessage(content="Hello, I'd like to order something."),
        AIMessage(content="Hello! What would you like to order?"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        HumanMessage(template="{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Combine tools and LLM
llm_with_tools = llm.bind(
    functions=[format_tool_to_openai_function(t) for t in tools]
)

# Define the agent state structure
class AgentState(TypedDict):
    input: str
    chat_history: List[str]
    intermediate_steps: List[tuple]

# Conditional function to determine if the conversation should continue
def should_continue(state: AgentState) -> str:
    if state["intermediate_steps"] and state["intermediate_steps"][-1][0].tool == "Confirm":
        return "end"
    return "continue"

# Function to run the agent and process the results
def run_agent(state: AgentState) -> AgentState:
    result = llm_with_tools.invoke(state)
    if isinstance(result, AgentFinish):
        return {"output": result.return_values["output"]}
    else:
        tool = result.tool
        observation = tool.run(result.tool_input)
        new_state = state.copy()
        new_state["intermediate_steps"].append((result, str(observation)))
        return new_state

# Create the graph to control the conversation flow
workflow = StateGraph(AgentState)

workflow.add_node("agent", run_agent)
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "agent",
        "end": END
    }
)

workflow.set_entry_point("agent")
agent_app = workflow.compile()

# FastAPI route for agent interaction
@app.post("/chat")
async def chat(user_input: Dict[str, Any]):
    state = {
        "input": user_input.get("input", ""),
        "chat_history": user_input.get("chat_history", []),
        "intermediate_steps": []
    }

    response = {"response": ""}
    
    for output in agent_app.stream(state):
        if "output" in output:
            response["response"] = output["output"]
            break  # We get the first response and return it
    
    return response

# Define API routes for Beckn API
@app.post("/search")
async def search_item(request: SearchRequest):
    try:
        result = search(request.item, request.delivery_location)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/select")
async def select_item(request: SelectRequest):
    try:
        result = select(request.bpp_id, request.bpp_uri, request.provider_id, request.item_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/init")
async def init_order(request: InitRequest):
    try:
        result = init(
            request.bpp_id, request.bpp_uri, request.provider_id, 
            request.item_id, request.billing_info, request.delivery_info
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/confirm")
async def confirm_order(request: ConfirmRequest):
    try:
        result = confirm(
            request.bpp_id, request.bpp_uri, request.provider_id, 
            request.item_id, request.billing_info, request.delivery_info, 
            request.payment_info
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/status")
async def check_status(request: StatusRequest):
    try:
        result = status(request.bpp_id, request.bpp_uri, request.order_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/track")
async def track_order(request: TrackRequest):
    try:
        result = track(request.bpp_id, request.bpp_uri, request.order_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cancel")
async def cancel_order(request: CancelRequest):
    try:
        result = cancel(request.bpp_id, request.bpp_uri, request.order_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/support")
async def support_request(request: SupportRequest):
    try:
        result = support(request.bpp_id, request.bpp_uri, request.order_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Run FastAPI server with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
