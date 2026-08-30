from typing import NamedTuple, Optional, Any
import re
from urllib.parse import unquote
import httpx
from ..base import Base, MirrativError

class Util_Service(Base):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        
    async def get_profile(self, user_id: int | str): 
        await self._ensure_user_exists(user_id, self.client)
        params = {"user_id": str(user_id)}
        data = await self.get_data(client=self.client, url="https://www.mirrativ.com/api/user/profile", params=params)
            
        class Res(NamedTuple):
            name: str
            description: str
            image: str
            follower: int
            follow: int
            user_name: str
                
        return Res(
            name=data["name"],
            description=data["description"],
            image=data["profile_image_url"],
            follower=data["follower_num"],
            follow=data["following_num"],
            user_name=data["name"]
        )
    
    async def live_request(self, user_id, count: str | int) -> dict[str, Any]:      
        await self._ensure_user_exists(user_id, self.client)          
        self._validate_int(count, "有効な回数を設定してください")
        safe_count = min(int(count), 9999)
                                    
        payload = {
            'user_id': str(user_id),
            'count': str(safe_count),
            'where': "profile"
        }
        
        data = await self.post_data(client=self.client, url="https://www.mirrativ.com/api/user/post_live_request", data_payload=payload)
        return data
    
    async def get_liveID(self, user_id: str | int) -> Optional[str]:
        await self._ensure_user_exists(user_id, self.client)
        params = {"user_id": str(user_id)}
        data = await self.get_data(client=self.client, url="https://www.mirrativ.com/api/live/live_history", params=params)
        
        lives = data.get("lives")
        if lives and isinstance(lives, list) and len(lives) > 0:
            return lives[0].get("live_id")
        return None
    
    async def parse_url(self, url: str) -> Optional[str]:
        decoded_url = unquote(url)
        match = re.search(r'/live/([a-zA-Z0-9_-]+)', decoded_url)
        
        if match:
            return match.group(1)
        return None
    