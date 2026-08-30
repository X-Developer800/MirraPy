import os
import json

class Json_Manager:
    @staticmethod
    def Base_dir():
        base_dir = os.path.join(os.getcwd(), "Mirrativ_User")
        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, "accounts.json")
    
    @classmethod
    def load(cls) -> list:
        file_path = cls.Base_dir()
        
        if not os.path.exists(file_path):
            return []  
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and "mr_id" in data:
                    return [data]
                return []
        except (json.JSONDecodeError, Exception):
            return []
    
    @classmethod
    def save(cls, mr_id: str):
        file_path = cls.Base_dir()
        accounts = cls.load()
        
        if not any(acc.get("mr_id") == mr_id for acc in accounts):
            accounts.append({"mr_id": mr_id})
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(accounts, f, ensure_ascii=False, indent=4)
            print(f"アカウントを保存しました: {mr_id}")
        else:
            print(f"すでに存在しています: {mr_id}")