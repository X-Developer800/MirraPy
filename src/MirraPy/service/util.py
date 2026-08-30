from typing import NamedTuple, Optional, Any
from urllib.parse import unquote
import httpx
from ..base import Base
from MirraPy.utils.endpoints import EndPoint
from ..utils.ensure import Ensure
from ..utils.validator import Validator
from ..utils.extract import Extract

class UtilService(Base):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        
    async def get_profile(self, user_id: int | str): 
        await Ensure.user_exists(user_id, self.client)
        params = {"user_id": str(user_id)}
        data = await self.get(client=self.client, url=EndPoint.User.PROFILE, params=params)
            
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
        await Ensure.user_exists(user_id, self.client)          
        Validator.Int(count, "有効な回数を設定してください")
        safe_count = min(int(count), 9999)
                                    
        payload = {
            'user_id': str(user_id),
            'count': str(safe_count),
            'where': "profile"
        }
        
        data = await self.post(client=self.client, url=EndPoint.User.LIVE_REQUEST, data_payload=payload)
        return data
    
    async def get_liveID(self, user_id_or_url: str | int) -> Optional[str]:
        target_str = str(user_id_or_url)
        
        if target_str.startswith("https"):
            return self.extract_url(target_str) 
        
        await Ensure.user_exists(target_str, self.client)
        params = {"user_id": target_str}
        data = await self.get(client=self.client, url=EndPoint.Live.LIVE_HISTORY, params=params)
        
        lives = data.get("lives")
        if lives and isinstance(lives, list) and len(lives) > 0:
            return lives[0].get("live_id")
        return None