import json
import os
from typing import List, Dict, Any, Type, TypeVar

T = TypeVar("T")

class JsonManager:
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
    
    def load_all(self) -> List[Dict[str, Any]]:
         with open(self.filepath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def save_all(self, data: List[Dict[str, Any]]) -> None:
         with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add(self, item: Dict[str, Any]) -> None:
         data = self.load_all()
         data.append(item)
         self.save_all(data)

    def update(self, item_id: str, new_data: Dict[str, Any], id_field: str = "id") -> bool:
         data = self.load_all()
         for i, obj in enumerate(data):
            if obj.get(id_field) == item_id:
                data[i] = new_data
                self.save_all(data)
                return True
         return False

    def delete(self, item_id: str, id_field: str = "id") -> bool:
         data = self.load_all()
         new_data = [d for d in data if d.get(id_field) != item_id]
         if len(new_data) == len(data):
             return False
         self.save_all(new_data)
         return True
