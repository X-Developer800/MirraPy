import httpx
from ..base import Base, MirrativError
from ..json_manager import Json_Manager
from typing import NamedTuple, Any, Optional, TYPE_CHECKING
from MirraPy.utils.endpoints import EndPoint
from ..utils.ensure import Ensure

if TYPE_CHECKING:
    from ..base import Base

class UserService:
    def __init__(self, base: Optional['Base']):
        self.base = base
            
    async def create_account(self, name: str, description: str = "create by XXX", url: str = "https://x.com/xxxxvtnk", save_mode: bool = None):
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

        class Res(NamedTuple):
            username: str
            userid: str
            mr_id: str

        return Res(
            data.get("name"), 
            str(data.get("user_id")), 
            cookies.get('mr_id', ''),
        )
        
    async def edit_profile(self, user_id: int | str, name: str, description: str = "create by XXX", url: str = "https://x.com/xxxxvtnk") -> dict[str, Any]:
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