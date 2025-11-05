from typing import Any, Dict, List


def extract_movement_fields(payload: Any):
    keys = ("from", "to", "productName", "movementId")
    items = payload.get("items", [])
    result = []

    for item in items:
        if isinstance(item, dict):
            filtered = {}
            for k in keys:
                filtered[k] = item.get(k)
            result.append(filtered)

    return result

def extract_transaction_fields(payload: Any):
    keys = ("txHash", "movementId")
    items = payload.get("items", [])
    result = []

    for item in items:
        if isinstance(item, dict):
            filtered = {}
            for k in keys:
                filtered[k] = item.get(k)
            result.append(filtered)

    return result


def extract_report_fields(payload:Any,userId:str):
    total = 0
    valid = 0
    for item in payload:
        if item["userId"] == userId:
            total = total + 1
            if item["analysis"]["riskLevel"] == "low":
                valid = valid + 1
        
        return [
            {
               "total reports" : total,
               "total valid reports " : valid
            }
        ]
        

            




