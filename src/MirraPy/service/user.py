from typing import Any, TYPE_CHECKING
from MirraPy.utils.endpoints import EndPoint
from ..base import Base, MirrativError
from ..json_manager import Json_Manager
from ..models.user import CreateAccount, GetProfile
from ..utils.ensure import Ensure
from ..utils.validator import Validator

if TYPE_CHECKING:
    from ..base import Base

class UserService:
    def __init__(self, base: 'Base'):
        self.base = base
            
    async def create_account(self, name: str, description: str = "create by XXX", url: str = "https://x.com/xxxxvtnk", save_mode: bool = None) -> CreateAccount:
        if not url.startswith("https://"):
            raise MirrativError("有効なUrlを指定してください")
            
        headers = self.base._create_header()
        links_value = '[{"url":"' + url + '"}]'

        r2 = await self.base.client.get(EndPoint.User.ME, headers=headers)
        r2.raise_for_status()
        user_id = r2.json().get('user_id')

        payload = {
            'user_id': str(user_id),
            "links": links_value,
            'name': name,
            "description": description,
            'birthday': '0101',
            'is_visible_birthday': '0',
            'is_vip_public': '1',
            'include_urge_users': '0'
        }
        data = await self.base.post(url=EndPoint.User.PROFILE_EDIT, data_payload=payload)
        cookies = self.base.client.cookies
        if save_mode:
            Json_Manager.save(mr_id=cookies.get('mr_id', ''), user_id=str(user_id))

        return CreateAccount(
            data.get("name"), 
            str(data.get("user_id")), 
            cookies.get('mr_id', ''),
        )
        
    async def update_profile(self, user_id: int | str, name: str, description: str = "create by XXX", url: str = "https://x.com/xxxxvtnk") -> dict[str, Any]:
        await Ensure.user_exists(self.base, user_id)
        if not url.startswith("https://"):
            raise MirrativError("有効なUrlを指定してください")
        
        links_value = '[{"url":"' + url + '"}]'
            
        payload = {
            'user_id': str(user_id),
            "links": links_value,
            'name': name,
            "description": description,
            'birthday': '0101',
            'is_visible_birthday': '0',
            'is_vip_public': '1',
            'include_urge_users': '0'
        }
        data = await self.base.post(url=EndPoint.User.PROFILE_EDIT, data_payload=payload)
        return data
    
    async def profile(self, user_id: int | str): 
        await Ensure.user_exists(self.base, user_id)
        params = {"user_id": str(user_id)}
        data = await self.base.get(url=EndPoint.User.PROFILE, params=params)
            
        return GetProfile(
            name=data["name"],
            description=data["description"],
            image=data["profile_image_url"],
            follower=data["follower_num"],
            follow=data["following_num"],
            user_name=data["name"],
            share_url=data["share_url"]
        )
        
    async def live_request(self, user_id, count: str | int) -> dict[str, Any]:      
        await Ensure.user_exists(self.base, user_id)       
        count = Validator.Int(count, "有効な回数を設定してください")
        safe_count = min(int(count), 9999)
                                    
        payload = {
            'user_id': str(user_id),
            'count': str(safe_count),
            'where': "profile"
        }
        
        data = await self.base.post(url=EndPoint.User.LIVE_REQUEST, data_payload=payload)
        return data