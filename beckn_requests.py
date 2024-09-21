import requests
import json
from typing import Dict, Any
import uuid
from datetime import datetime

BASE_URL = "https://ps-bap-client.becknprotocol.io"

def generate_context(action: str) -> Dict[str, Any]:
    return {
        "domain": "local-retail",
        "country": "IND",
        "city": "std:080",
        "action": action,
        "core_version": "1.1.0",
        "bap_id": "sandbox-bap-network.becknprotocol.io",
        "bap_uri": "https://sandbox-bap-network.becknprotocol.io/",
        "transaction_id": str(uuid.uuid4()),
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat()
    }

def send_request(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def search(item: str, delivery_location: str) -> Dict[str, Any]:
    context = generate_context("search")
    payload = {
        "context": context,
        "message": {
            "intent": {
                "item": {
                    "descriptor": {
                        "name": item
                    }
                },
                "fulfillment": {
                    "end": {
                        "location": {
                            "gps": delivery_location
                        }
                    }
                }
            }
        }
    }
    return send_request("search", payload)

def select(bpp_id: str, bpp_uri: str, provider_id: str, item_id: str) -> Dict[str, Any]:
    context = generate_context("select")
    context.update({
        "bpp_id": bpp_id,
        "bpp_uri": bpp_uri
    })
    payload = {
        "context": context,
        "message": {
            "order": {
                "provider": {
                    "id": provider_id
                },
                "items": [
                    {
                        "id": item_id
                    }
                ]
            }
        }
    }
    return send_request("select", payload)

def init(bpp_id: str, bpp_uri: str, provider_id: str, item_id: str, billing_info: Dict[str, Any], delivery_info: Dict[str, Any]) -> Dict[str, Any]:
    context = generate_context("init")
    context.update({
        "bpp_id": bpp_id,
        "bpp_uri": bpp_uri
    })
    payload = {
        "context": context,
        "message": {
            "order": {
                "provider": {
                    "id": provider_id
                },
                "items": [
                    {
                        "id": item_id
                    }
                ],
                "billing": billing_info,
                "fulfillment": {
                    "end": {
                        "location": {
                            "gps": delivery_info["location"],
                            "address": delivery_info["address"]
                        },
                        "contact": {
                            "phone": delivery_info["phone"]
                        }
                    }
                }
            }
        }
    }
    return send_request("init", payload)

def confirm(bpp_id: str, bpp_uri: str, provider_id: str, item_id: str, billing_info: Dict[str, Any], delivery_info: Dict[str, Any], payment_info: Dict[str, Any]) -> Dict[str, Any]:
    context = generate_context("confirm")
    context.update({
        "bpp_id": bpp_id,
        "bpp_uri": bpp_uri
    })
    payload = {
        "context": context,
        "message": {
            "order": {
                "provider": {
                    "id": provider_id
                },
                "items": [
                    {
                        "id": item_id
                    }
                ],
                "billing": billing_info,
                "fulfillment": {
                    "end": {
                        "location": {
                            "gps": delivery_info["location"],
                            "address": delivery_info["address"]
                        },
                        "contact": {
                            "phone": delivery_info["phone"]
                        }
                    }
                },
                "payment": payment_info
            }
        }
    }
    return send_request("confirm", payload)

def status(bpp_id: str, bpp_uri: str, order_id: str) -> Dict[str, Any]:
    context = generate_context("status")
    context.update({
        "bpp_id": bpp_id,
        "bpp_uri": bpp_uri
    })
    payload = {
        "context": context,
        "message": {
            "order_id": order_id
        }
    }
    return send_request("status", payload)

def track(bpp_id: str, bpp_uri: str, order_id: str) -> Dict[str, Any]:
    context = generate_context("track")
    context.update({
        "bpp_id": bpp_id,
        "bpp_uri": bpp_uri
    })
    payload = {
        "context": context,
        "message": {
            "order_id": order_id
        }
    }
    return send_request("track", payload)

def cancel(bpp_id: str, bpp_uri: str, order_id: str) -> Dict[str, Any]:
    context = generate_context("cancel")
    context.update({
        "bpp_id": bpp_id,
        "bpp_uri": bpp_uri
    })
    payload = {
        "context": context,
        "message": {
            "order_id": order_id,
            "cancellation_reason_id": "5"
        }
    }
    return send_request("cancel", payload)

def support(bpp_id: str, bpp_uri: str, order_id: str) -> Dict[str, Any]:
    context = generate_context("support")
    context.update({
        "bpp_id": bpp_id,
        "bpp_uri": bpp_uri
    })
    payload = {
        "context": context,
        "message": {
            "ref_id": order_id
        }
    }
    return send_request("support", payload)

# Example usage
if __name__ == "__main__":
    # Search for an item
    search_result = search("pizza", "12.9715987,77.5945627")
    print("Search Result:", json.dumps(search_result, indent=2))

    # Assuming we got valid results from search, we can proceed with select
    # (You would need to extract these values from the search result in a real scenario)
    select_result = select(
        "sandbox-bpp-network.becknprotocol.io",
        "https://sandbox-bpp-network.becknprotocol.io",
        "example_provider_id",
        "example_item_id"
    )
    print("Select Result:", json.dumps(select_result, indent=2))

    # Similarly for init, confirm, and other operations
    # You would use the results from previous steps to populate these calls