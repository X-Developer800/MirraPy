from typing import NamedTuple, Optional, Any, TYPE_CHECKING
import httpx
from MirraPy.utils.endpoints import EndPoint
from ..utils.ensure import Ensure
from ..utils.extract import Extract

if TYPE_CHECKING:
    from ..base import Base

class LiveService:
    def __init__(self, base: 'Base'):
        self.base = base
        
    async def status(self, live_id: str | None = None):
        target_live_id = Ensure.live_id(self.base, live_id)

        params = {"live_id": str(target_live_id)}
        data = await self.base.get(url=EndPoint.Live.LIVE, params=params)

        
        class Res(NamedTuple):
            alive: bool
            is_collabo: bool
            raw: dict[str, Any]
            
        is_live_value = bool(data.get("is_live", 0))
        is_collabo = bool(data.get("collab_enabled", 0))
        return Res(alive=is_live_value, is_collabo=is_collabo, raw=data)
    
    async def join(self, live_id: str | None = None):
        target_live_id = Ensure.live_id(self.base, live_id)

        payload = {
            'live_id': str(target_live_id),
            'live_user_key': "",
            'is_ui_hidden': 0,
            'screen_status': 4,
            'screen_settings': 0
        }
        
        data = await self.base.post(url=EndPoint.Live.LIVE_POLLING, data_payload=payload)
        return data
    
    async def leave(self, live_id: str | None = None):
        target_live_id = Ensure.live_id(self.base, live_id)

        payload = {
            'live_id': str(target_live_id),
        }
        
        data = await self.base.post(url=EndPoint.Live.LEAVE, data_payload=payload)
        return data
    
    async def find_id(self, user_id_or_url: str | int) -> Optional[str]:
        target_str = str(user_id_or_url)
        if target_str.startswith("https"): return Extract.url(target_str) 
        
        await Ensure.user_exists(self.base, user_id_or_url)
        params = {"user_id": target_str}
        data = await self.base.get(url=EndPoint.Live.LIVE_HISTORY, params=params)
        
        lives = data.get("lives")
        if lives and isinstance(lives, list) and len(lives) > 0:
            return lives[0].get("live_id")
        return None