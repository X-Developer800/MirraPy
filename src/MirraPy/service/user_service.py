import httpx
from ..base import Base, MirrativError
from ..json_manager import Json_Manager
from typing import NamedTuple, Any
from urllib.parse import parse_qs, urlparse

class User_Service(Base):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
    
    async def create_account(self, name: str, description: str = "create by XXX", url: str = "https://x.com/xxxxvtnk", save_mode: bool = None):
        if not url.startswith("https://"):
            raise MirrativError("有効なUrlを指定してください")
            
        headers = self._create_header()
        links_value = '[{"url":"' + url + '"}]'

        r2 = await self.client.get("https://www.mirrativ.com/api/user/me", headers=headers)
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
        data = await self.post_data(client=self.client, url="https://www.mirrativ.com/api/user/profile_edit", data_payload=payload)
        cookies = self.client.cookies
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
        await self._ensure_user_exists(user_id, self.client)
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
        data = await self.post_data(client=self.client, url="https://www.mirrativ.com/api/user/profile_edit", data_payload=payload)
        return data