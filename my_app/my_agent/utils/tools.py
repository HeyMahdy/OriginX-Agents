from langchain.tools import tool
import requests
from firebase_admin import db
from my_agent.utils.service import extract_movement_fields , extract_transaction_fields , extract_report_fields
from firebase_admin.exceptions import FirebaseError

MOCK_MOVEMENTS = {
    "prod_9s8df7": [
        {"from": "Warehouse A", "to": "Warehouse B", "productName": "Brake Pad X1", "movementId": "move_001"},
        {"from": "Warehouse B", "to": "Store C",    "productName": "Brake Pad X1", "movementId": "move_002"},
        {"from": "Store C",    "to": "Customer",    "productName": "Brake Pad X1", "movementId": "move_003"},
    ],
    "prod_allmatch": [
        {"from": "WH1", "to": "WH2",     "productName": "Widget A", "movementId": "move_a1"},
        {"from": "WH2", "to": "Store Z", "productName": "Widget A", "movementId": "move_a2"},
    ],
    "prod_multimismatch": [
        {"from": "HUB",     "to": "WH-X",     "productName": "Gadget B", "movementId": "move_m1"},
        {"from": "WH-X",    "to": "Retail-1", "productName": "Gadget B", "movementId": "move_m2"},
        {"from": "Retail-1","to": "Customer", "productName": "Gadget B", "movementId": "move_m3"},
    ],
}

MOCK_TRANSACTIONS = {
    
    "prod_9s8df7": [
        {"txHash": "0xabc", "movementId": "move_001"},
        {"txHash": "0xabc", "movementId": "move_002"},
        {"txHash": "0xdef", "movementId": "move_003"},
    ],
    # all match
    "prod_allmatch": [
        {"txHash": "0xaaa", "movementId": "move_a1"},
        {"txHash": "0xaaa", "movementId": "move_a2"},
    ],
    # multi mismatch (m1==m3, m2 different)
    "prod_multimismatch": [
        {"txHash": "0x111", "movementId": "move_m1"},
        {"txHash": "0x222", "movementId": "move_m2"},
        {"txHash": "0x111", "movementId": "move_m3"},
    ],
}
"""
@tool
def get_product_movements(product_id: str, page_size: int = 50):
    
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
"""
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
        items = MOCK_MOVEMENTS.get(product_id, [])
        # Keep your existing extractor contract (expects {"items": [...]})
        payload = {"items": items[:page_size]}
        return extract_movement_fields(payload)
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}
    
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
                     "movementId" : "24v"
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
        items = MOCK_TRANSACTIONS.get(productId, [])
        start = max((page - 1) * page_size, 0)
        end = start + page_size
        payload = {"items": items[start:end]}
        return extract_transaction_fields(payload)
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}
    
tools = [get_product_movements,get_product_transactions]
tools_by_name={ tool.name:tool for tool in tools}
        
    
MOCK_REPORTS = [
  
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 12, "riskLevel": "low", "anomalies": [], "confidence": 90, "recommendations": [] }, "scanCount": 110 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 15, "riskLevel": "low", "anomalies": [], "confidence": 88, "recommendations": [] }, "scanCount": 120 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 18, "riskLevel": "low", "anomalies": ["Normal variance"], "confidence": 87, "recommendations": [] }, "scanCount": 132 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 20, "riskLevel": "low", "anomalies": [], "confidence": 85, "recommendations": [] }, "scanCount": 140 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "true", "anomalyScore": 42, "riskLevel": "medium", "anomalies": ["Scan spike observed"], "confidence": 80, "recommendations": ["Monitor activity"] }, "scanCount": 200 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 19, "riskLevel": "low", "anomalies": [], "confidence": 82, "recommendations": [] }, "scanCount": 150 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 21, "riskLevel": "low", "anomalies": [], "confidence": 84, "recommendations": [] }, "scanCount": 160 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "true", "anomalyScore": 55, "riskLevel": "medium", "anomalies": ["Irregular timing pattern"], "confidence": 78, "recommendations": ["Review timings"] }, "scanCount": 230 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 14, "riskLevel": "low", "anomalies": [], "confidence": 90, "recommendations": [] }, "scanCount": 95 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 11, "riskLevel": "low", "anomalies": [], "confidence": 91, "recommendations": [] }, "scanCount": 100 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "true", "anomalyScore": 60, "riskLevel": "medium", "anomalies": ["Repeated scans in short window"], "confidence": 83, "recommendations": ["Investigate"] }, "scanCount": 250 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 16, "riskLevel": "low", "anomalies": [], "confidence": 88, "recommendations": [] }, "scanCount": 145 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 13, "riskLevel": "low", "anomalies": [], "confidence": 89, "recommendations": [] }, "scanCount": 125 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "true", "anomalyScore": 71, "riskLevel": "high", "anomalies": ["Suspicious continuous scans"], "confidence": 92, "recommendations": ["Flag account"] }, "scanCount": 300 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 17, "riskLevel": "low", "anomalies": ["Normal usage"], "confidence": 86, "recommendations": [] }, "scanCount": 155 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 23, "riskLevel": "low", "anomalies": [], "confidence": 85, "recommendations": [] }, "scanCount": 170 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "true", "anomalyScore": 52, "riskLevel": "medium", "anomalies": ["Spike and drop pattern"], "confidence": 81, "recommendations": ["Monitor next week"] }, "scanCount": 225 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 19, "riskLevel": "low", "anomalies": [], "confidence": 87, "recommendations": [] }, "scanCount": 135 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "false", "anomalyScore": 22, "riskLevel": "low", "anomalies": [], "confidence": 84, "recommendations": [] }, "scanCount": 165 },
  { "userId": "uid_001", "analysis": { "isAnomalous": "true", "anomalyScore": 65, "riskLevel": "high", "anomalies": ["Behavior deviation"], "confidence": 89, "recommendations": ["Immediate review"] }, "scanCount": 290 },


]

@tool
def get_reports(userId: str, page: int = 1, page_size: int = 25):
    """
    Fetch user report history for a specific users.

    This function retrieves user reports records related to a given
    user ID using the internal API key (no user token required).
txHash
    Args:
        userId (str): The user ID to fetch report .
        page (int, optional): Page number for pagination (default: 1).
        page_size (int, optional): Maximum number of reports to return (default: 25).

    Returns:
        dict: Parsed JSON response containing report records.

        Example success:
        {
          "total reports" : 40,
          "total valid reports " : 30
        }

        Example error:
        {
            "error": "HTTP error occurred",
            "status_code": 401,
            "details": "Missing or invalid API key"
        }
    """
    try:
        payload = MOCK_REPORTS
        return extract_report_fields(payload,userId)
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}
    
tools = [get_product_movements,get_product_transactions]
tools_by_name={ tool.name:tool for tool in tools}


tools_01 = [get_reports]
tools_by_name_01 = {tool.name: tools for tools in tools_01}
