from typing import NamedTuple
import httpx
from ..base import Base, MirrativError

class Live_Service(Base):
    def __init__(self, client: httpx.AsyncClient):
        super().__init__() 
        self.client = client
        
    async def Collabo_Request(self, live_id: str | None = None):
        target_live_id = self._ensure_live_id(live_id)

        payload = {
            'live_id': str(target_live_id),
            'collab_type': 1
        }

        data = await self.post_data(client=self.client, url="https://www.mirrativ.com/api/collab/request", data_payload=payload)
        return data
    
    async def Collabo_Cancel(self, live_id: str | None = None):
        target_live_id = self._ensure_live_id(live_id)

        payload = {
            'live_id': str(target_live_id),
        }
        
        data = await self.post_data(client=self.client, url="https://www.mirrativ.com/api/collab/cancel", data_payload=payload)
        return data
    
    async def check_live(self, live_id: str | None = None):
        target_live_id = self._ensure_live_id(live_id)

        params = {"live_id": str(target_live_id)}
        data = await self.get_data(client=self.client, url="https://www.mirrativ.com/api/live/live", params=params)
        
        class Res(NamedTuple):
            alive: bool
            is_collabo: bool
            
        is_live_value = bool(data.get("is_live", 0))
        is_collabo = bool(data.get("collab_enabled", 0))
        return Res(alive=is_live_value, is_collabo=is_collabo)
    
    async def live_join(self, live_id: str | None = None):
        target_live_id = self._ensure_live_id(live_id)

        payload = {
            'live_id': str(target_live_id),
            'live_user_key': "",
            'is_ui_hidden': 0,
            'screen_status': 4,
            'screen_settings': 0
        }
        
        data = await self.post_data(client=self.client, url="https://www.mirrativ.com/api/live/live_polling", data_payload=payload)
        return data
    
    async def live_leave(self, live_id: str | None = None):
        target_live_id = self._ensure_live_id(live_id)

        payload = {
            'live_id': str(target_live_id),
        }
        
        data = await self.post_data(client=self.client, url="https://www.mirrativ.com/api/live/leave", data_payload=payload)
        return data