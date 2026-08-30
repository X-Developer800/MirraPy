import httpx
from ..base import Base
from ..json_manager import Json_Manager
from typing import NamedTuple
from urllib.parse import parse_qs, urlparse

class User_Data(Base):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def create_account(self, name: str, description: str = "create by XXX", url: str = "https://x.com/xxxxvtnk", save_mode: bool = None):
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
            Json_Manager.save(mr_id=cookies.get('mr_id', ''))

        class AcRes(NamedTuple):
            nickname: str
            userid: str
            mr_id: str

        return AcRes(
            data.get("name"), 
            str(data.get("user_id")), 
            cookies.get('mr_id', ''),
        )