from typing import Any, TYPE_CHECKING
from MirraPy.utils.endpoints import EndPoint
from ..utils.ensure import Ensure

if TYPE_CHECKING:
    from ..base import Base

class CollabService:
    def __init__(self, base: 'Base'):
        self.base = base
        
    async def request(self, live_id: str | None = None) -> dict[str, Any]:
        target_live_id = Ensure.live_id(self.base, live_id)

        payload = {
            'live_id': str(target_live_id),
            'collab_type': 1
        }

        data = await self.base.post(url=EndPoint.Collab.REQUEST, data_payload=payload)
        return data
    
    async def cancel(self, live_id: str | None = None) -> dict[str, Any]:
        target_live_id = Ensure.live_id(self.base, live_id)

        payload = {
            'live_id': str(target_live_id),
        }
        
        data = await self.base.post(url=EndPoint.Collab.CANCEL, data_payload=payload)
        return data