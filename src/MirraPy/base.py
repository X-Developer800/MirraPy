import time
import random
import uuid
import httpx

class MirrativError(Exception):
    pass

class Base:
    def __init__(self):
        self.live_id: str | None = None

    def set_liveid(self, live_id: str):
        self.live_id = str(live_id)
        
    def _create_header(self) -> dict:
        devices = [
            {"model": "SM-S908N", "os": "12"},
            {"model": "Pixel_7", "os": "13"},
            {"model": "SO-51C", "os": "12"},
            {"model": "SH-51C", "os": "13"}
        ]
        device = random.choice(devices)
        
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
        
    def _check_response(self, data: dict):
        if not isinstance(data, dict):
            return data
        
        status = data.get("status")
        if isinstance(status, dict):
            error_msg = status.get("error") or status.get("message")
            if error_msg and error_msg != "":
                raise MirrativError(error_msg)
                
        return data
    
    async def get_data(self, client: httpx.AsyncClient, url, params):
        headers = self._create_header()
        response = await client.get(
            url, 
            headers=headers, 
            params=params
        )
        
        response.raise_for_status()
        data = response.json()
        self._check_response(data)
        return data
    
    async def post_data(self, client: httpx.AsyncClient, url, data_payload):
        headers = self._create_header()
        response = await client.post(
            url, 
            headers=headers, 
            data=data_payload
        )
        
        response.raise_for_status()
        data = response.json()
        self._check_response(data)
        return data