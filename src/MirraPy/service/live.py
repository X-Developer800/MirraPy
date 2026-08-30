from typing import NamedTuple
import httpx
from ..base import Base, MirrativError
from MirraPy.utils.endpoints import EndPoint
from ..utils.ensure import Ensure

class LiveService(Base):
    def __init__(self, client: httpx.AsyncClient):
        super().__init__(client) 
        self.client = client
        
    async def Collabo_Request(self, live_id: str | None = None):
        target_live_id = Ensure.live_id(self, live_id)

        payload = {
            'live_id': str(target_live_id),
            'collab_type': 1
        }

        data = await self.post(url=EndPoint.Collab.REQUEST, data_payload=payload)
        return data
    
    async def Collabo_Cancel(self, live_id: str | None = None):
        target_live_id = Ensure.live_id(self, live_id)

        payload = {
            'live_id': str(target_live_id),
        }
        
        data = await self.post(url=EndPoint.Collab.CANCEL, data_payload=payload)
        return data
    
    async def check_live(self, live_id: str | None = None):
        target_live_id = Ensure.live_id(self, live_id)

        params = {"live_id": str(target_live_id)}
        data = await self.get(url=EndPoint.Live.LIVE, params=params)

        
        class Res(NamedTuple):
            alive: bool
            is_collabo: bool
            raw: str
            
        is_live_value = bool(data.get("is_live", 0))
        is_collabo = bool(data.get("collab_enabled", 0))
        return Res(alive=is_live_value, is_collabo=is_collabo, raw=data)
    
    async def live_join(self, live_id: str | None = None):
        target_live_id = Ensure.live_id(self, live_id)

        payload = {
            'live_id': str(target_live_id),
            'live_user_key': "",
            'is_ui_hidden': 0,
            'screen_status': 4,
            'screen_settings': 0
        }
        
        data = await self.post(url=EndPoint.Live.LIVE_POLLING, data_payload=payload)
        return data
    
    async def live_leave(self, live_id: str | None = None):
        target_live_id = Ensure.live_id(self, live_id)

        payload = {
            'live_id': str(target_live_id),
        }
        
        data = await self.post(url=EndPoint.Live.LEAVE, data_payload=payload)
        return data