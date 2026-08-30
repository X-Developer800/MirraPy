import time
import random
import uuid
import httpx
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
    
    async def get(self, client: httpx.AsyncClient, url, params) -> dict[str, Any]:
        headers = self._create_header()
        response = await client.get(url, headers=headers, params=params)
        return self._handle_response(response)
    
    async def post(self, client: httpx.AsyncClient, url, data_payload) -> dict[str, Any]:
        headers = self._create_header()
        response = await client.post(url, headers=headers, data=data_payload)
        return self._handle_response(response)