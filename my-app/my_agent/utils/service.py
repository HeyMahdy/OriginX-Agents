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
