from langchain.tools import tool
import requests
from firebase_admin import db
from my_agent.utils.service import extract_movement_fields , extract_transaction_fields
from firebase_admin.exceptions import FirebaseError



@tool
def get_product_movements(product_id: str, page_size: int = 50):
    """
    Fetch product movement data from the OriginX API.

    This function retrieves all recorded movements for a specific product
    using the OriginX internal API key.

    Args:
        product_id (str): The product ID to filter movements.
        page_size (int, optional): Maximum number of items to return (default: 50).

    Returns:
        dict: Parsed JSON response containing product movement records.
        Example success:
        {
  "items": [
    {
      "from": "Warehouse A",
      "to": "Warehouse B",
      "productName": "Brake Pad X1",
      "productId": "prod_9s8df7"
    }
  ],
  "total": 1,
  "pageSize": 50
}

   
    """
    try:

        ref = db.reference(f"/api/movements/by-product/{product_id}")
        data = ref.get()
        data = extract_movement_fields(data)
        return data
    
    except FirebaseError as fe:
        return {
            "error": "Firebase error occurred",
            "code": getattr(fe, "code", None),
            "details": str(fe)
        }
    except ValueError as ve:
        # e.g., unexpected payload shape from Firebase
        return {
            "error": "Invalid Firebase data",
            "details": str(ve)
        }
    except requests.exceptions.HTTPError as he:
        return {
            "error": "HTTP error occurred",
            "status_code": he.response.status_code if he.response else None,
            "details": str(he)
        }
    except requests.exceptions.RequestException as re:
        return {
            "error": "Request failed",
            "details": str(re)
        }
    except Exception as e:
        return {
            "error": "Unexpected error",
            "details": str(e)
        }


@tool
def get_product_transactions(productId: str, page: int = 1, page_size: int = 25):
    """
    Fetch transaction history for a specific product from the OriginX API.

    This function retrieves blockchain transaction records related to a given
    product ID using the internal API key (no user token required).
txHash
    Args:
        product_id (str): The product ID to fetch transactions for.
        page (int, optional): Page number for pagination (default: 1).
        page_size (int, optional): Maximum number of transactions to return (default: 25).

    Returns:
        dict: Parsed JSON response containing transaction records.

        Example success:
        {
            "items": [
                {
                    "txHash": "0x1f3a...",
                    "type": "PRODUCT_REGISTER",
                    "status": "confirmed",
                    "blockNumber": 1024,
                    "refType": "product",
                    "refId": "prod_9s8df7",
                    "orgId": "org_123",
                    "createdBy": "uid_abc",
                    "createdAt": 1730385600,
                    "confirmedAt": 1730385610,
                    "payload": {
                        "productId": "prod_9s8df7",
                        "productName": "Brake Pad X1",
                        "sku": "BPX1-2025",
                        "category": "automotive"
                    }
                }
            ],
            "total": 250,
            "page": 1,
            "pageSize": 25,
            "hasMore": true
        }

        Example error:
        {
            "error": "HTTP error occurred",
            "status_code": 401,
            "details": "Missing or invalid API key"
        }
    """
    try:
        ref = db.reference(f"/api/transactions/{productId}")
        data = ref.get()
        data = extract_transaction_fields(data)
        return data
    
    except FirebaseError as fe:
        return {
            "error": "Firebase error occurred",
            "code": getattr(fe, "code", None),
            "details": str(fe)
        }
    except ValueError as ve:
        # e.g., unexpected payload shape from Firebase
        return {
            "error": "Invalid Firebase data",
            "details": str(ve)
        }
    except requests.exceptions.HTTPError as he:
        return {
            "error": "HTTP error occurred",
            "status_code": he.response.status_code if he.response else None,
            "details": str(he)
        }
    except requests.exceptions.RequestException as re:
        return {
            "error": "Request failed",
            "details": str(re)
        }
    except Exception as e:
        return {
            "error": "Unexpected error",
            "details": str(e)
        }


tools = [get_product_movements,get_product_transactions]
tools_by_name={ tool.name:tool for tool in tools}
        
    
