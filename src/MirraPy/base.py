import time
import random
import uuid
import httpx
import re
from typing import Any

class MirrativError(Exception):
    pass

class Base:
    DEVICES: list[dict[str, str]] = [
        {"model": "SM-S908N", "os": "12"},
        {"model": "Pixel_7", "os": "13"},
        {"model": "SO-51C", "os": "12"},
        {"model": "SH-51C", "os": "13"}
    ]
    
    def __init__(self):
        self.live_id: str = None

    def set_liveid(self, live_id: str) -> str:
        self.live_id = str(live_id)
        
    def _create_header(self) -> dict[str, str]:
        device = random.choice(self.DEVICES)
        
        return {
            "Host": "www.mirrativ.com",
            "X-Referer": "my_page",
            "User-Agent": f'MR_APP/11.64.1/Android/{device["model"]}/{device["os"]}',
            "Accept-Language": "ja-JP",
            "Http_x_timezone": "Asia/Tokyo",
            "X-Idfv": str(uuid.uuid4()).replace("-", "")[:16], 
            "X-Ad": str(uuid.uuid4()),                     
            "X-Hw": "qcom",
            "X-Network-Status": "2",
            "X-Os-Push": "1",
            "X-Client-Unixtime": str(time.time()),
            "X-Adjust-Adid": str(uuid.uuid4()),         
            "X-Unity-Framework": "6.11.0"
        }
    
    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        try:
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            raise MirrativError(f"HTTP Error: {e.response.status_code}") from e
        except ValueError as e:
            raise MirrativError("サーバーからのレスポンスがJSON形式ではありません。") from e

        if isinstance(data, dict):
            status = data.get("status")
            if isinstance(status, dict):
                if error_msg := (status.get("error") or status.get("message")):
                    raise MirrativError(error_msg)
        return data
    
    async def get_data(self, client: httpx.AsyncClient, url, params) -> dict[str, Any]:
        headers = self._create_header()
        response = await client.get(url, headers=headers, params=params)
        return self._handle_response(response)
    
    async def post_data(self, client: httpx.AsyncClient, url, data_payload) -> dict[str, Any]:
        headers = self._create_header()
        response = await client.post(url, headers=headers, data=data_payload)
        return self._handle_response(response)
    
    def _ensure_live_id(self, live_id: str = None) -> str:
        target_id = live_id or getattr(self, "live_id", None)
        if not target_id: raise MirrativError("live_id が指定されていません。事前に set_liveid を呼ぶか、引数を渡してください。")
        return str(target_id)
    
    def _validate_int(self, num: int | str, comment: str) -> None:
        try:
            int(num)
        except (ValueError, TypeError):
            raise MirrativError(comment)
        
    def extract_url(text) -> str | None:
        url_index = str.find(text, "https://")
        if url_index != -1:
            extracted_url = str.strip(text[url_index:])
            return extracted_url
        
        match = re.search(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', text)
        if match:
            return re.Match.group(match, 0)
        return None
    
    async def _ensure_user_exists(self, user_id: int | str, client: httpx.AsyncClient) -> None:
        self._validate_int(user_id, "有効なユーザーIDを設定してください")
        params = {"q": str(user_id)}
        data = await self.get_data(client=client, url="https://www.mirrativ.com/api/user/search", params=params)
        if not data.get("users"): raise MirrativError("ユーザーがみつかりません。")