import httpx, uuid
from .service.user_service import User_Service
from .service.live_service import Live_Service
from .service.util_service import Util_Service
from .json_manager import Json_Manager
from .base import Base

class Client:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client
        self.user = User_Service(client)
        self.live = Live_Service(client)
        self.util = Util_Service(client)
        
    def login(self, mr_id) -> None:
        self._client.cookies.set("mr_id", mr_id, domain="www.mirrativ.com")
        
    @property
    def json_manager(self) -> type[Json_Manager]:
        return Json_Manager