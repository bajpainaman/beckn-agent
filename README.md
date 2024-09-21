# Beckn Protocol Shopping Agent with FastAPI and LangGraph

This project provides an AI-powered shopping agent built with FastAPI and LangGraph that helps users shop through the **Beckn Protocol**. The agent can search for items, help with order selection, initialization, confirmation, and even track, cancel, or support orders. Users can interact with the agent conversationally, simulating a shopping experience, or make direct API calls for more control.

## Features

- **Shopping Assistant**: A conversational AI agent that helps you shop by interacting with the decentralized Beckn Protocol. The agent can:
  - Search for items
  - Select items from available providers
  - Initialize and confirm orders
  - Track the status of orders
  - Cancel orders or request support
- **Beckn API Integration**: For advanced users, the project also provides direct API endpoints for various shopping actions such as `search`, `select`, `init`, `confirm`, `status`, `track`, `cancel`, and `support`.
- **User-Friendly Interface**: A simple API-driven interaction model that makes shopping through the Beckn network seamless and efficient.

## Prerequisites

- Python 3.7+
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://github.com/hwchase17/langchain)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/bajpainaman/beckn-agent.git
    cd beckn-agent
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    Alternatively, you can install dependencies manually:

    ```bash
    pip install fastapi uvicorn pydantic langchain_openai langgraph requests
    ```

3. Set up your OpenAI API key by creating a `.env` file or exporting the key directly:

    ```bash
    export OPENAI_API_KEY="your-api-key"
    ```

## Usage

### 1. Run the Server

To start the FastAPI server using Uvicorn, run:

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

### 2. Conversational Shopping Agent

Interact with the AI shopping assistant via the `/chat` endpoint. The agent will guide you through the shopping process on the Beckn Protocol, from searching for items to confirming your orders.

#### Example Chat Request:

```bash
POST http://localhost:8000/chat
Content-Type: application/json
{
    "input": "I want to order a pizza.",
    "chat_history": []
}
```

The agent will respond and continue to guide you through selecting a provider, initializing the order, and completing the purchase.

### 3. Direct Beckn API Endpoints

For more control, you can interact with the Beckn Protocol directly via these API endpoints. Each endpoint handles a specific shopping action such as searching for items, confirming orders, or tracking status.

#### Available Endpoints:

- **Search for Items**: `/search`
- **Select an Item**: `/select`
- **Initialize an Order**: `/init`
- **Confirm an Order**: `/confirm`
- **Check Order Status**: `/status`
- **Track an Order**: `/track`
- **Cancel an Order**: `/cancel`
- **Request Support**: `/support`

#### Example Direct API Call:

```bash
POST http://localhost:8000/search
Content-Type: application/json
{
    "item": "pizza",
    "delivery_location": "12.9715987,77.5945627"
}
```

### Example API Requests

Below are examples of how you can use the various API endpoints to interact directly with the Beckn Protocol:

- **Search for Items**:

    ```json
    POST /search
    {
      "item": "pizza",
      "delivery_location": "12.9715987,77.5945627"
    }
    ```

- **Select an Item**:

    ```json
    POST /select
    {
      "bpp_id": "sandbox-bpp-network.becknprotocol.io",
      "bpp_uri": "https://sandbox-bpp-network.becknprotocol.io",
      "provider_id": "example_provider_id",
      "item_id": "example_item_id"
    }
    ```

- **Initialize an Order**:

    ```json
    POST /init
    {
      "bpp_id": "sandbox-bpp-network.becknprotocol.io",
      "bpp_uri": "https://sandbox-bpp-network.becknprotocol.io",
      "provider_id": "example_provider_id",
      "item_id": "example_item_id",
      "billing_info": {
        "phone": "9999999999",
        "email": "email@example.com",
        "address": "123 Street, City"
      },
      "delivery_info": {
        "location": "12.9715987,77.5945627",
        "address": "456 Street, City",
        "phone": "8888888888"
      }
    }
    ```

- **Confirm an Order**:

    ```json
    POST /confirm
    {
      "bpp_id": "sandbox-bpp-network.becknprotocol.io",
      "bpp_uri": "https://sandbox-bpp-network.becknprotocol.io",
      "provider_id": "example_provider_id",
      "item_id": "example_item_id",
      "billing_info": {
        "phone": "9999999999",
        "email": "email@example.com",
        "address": "123 Street, City"
      },
      "delivery_info": {
        "location": "12.9715987,77.5945627",
        "address": "456 Street, City",
        "phone": "8888888888"
      },
      "payment_info": {
        "method": "credit_card",
        "transaction_id": "txn_12345"
      }
    }
    ```

- **Track an Order**:

    ```json
    POST /track
    {
      "bpp_id": "sandbox-bpp-network.becknprotocol.io",
      "bpp_uri": "https://sandbox-bpp-network.becknprotocol.io",
      "order_id": "example_order_id"
    }
    ```

- **Cancel an Order**:

    ```json
    POST /cancel
    {
      "bpp_id": "sandbox-bpp-network.becknprotocol.io",
      "bpp_uri": "https://sandbox-bpp-network.becknprotocol.io",
      "order_id": "example_order_id"
    }
    ```

- **Request Support**:

    ```json
    POST /support
    {
      "bpp_id": "sandbox-bpp-network.becknprotocol.io",
      "bpp_uri": "https://sandbox-bpp-network.becknprotocol.io",
      "order_id": "example_order_id"
    }
    ```

## Project Structure

```
.
├── beckn_requests.py          # Contains all the Beckn API request functions
├── main.py                    # FastAPI app and agent definition
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## API Documentation

Once the server is running, you can visit the interactive API documentation generated by FastAPI at:

```
http://127.0.0.1:8000/docs
```




