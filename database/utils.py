import json
from typing import List

def get_json_list(json_str: str) -> List:
    """Convierte un string JSON a lista"""
    try:
        return json.loads(json_str) if json_str else []
    except:
        return []

def set_json_list(items: List) -> str:
    """Convierte una lista a string JSON"""
    return json.dumps(items)
