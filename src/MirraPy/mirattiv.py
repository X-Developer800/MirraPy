import httpx, uuid
from .service.user_service import User_Data
from .json_manager import Json_Manager

class Client:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client
        self.user = User_Data(client)
        
    def login(self, mr_id):
        self._client.cookies.set("mr_id", mr_id, domain="www.mirrativ.com")
        
    @property
    def json_manager(self) -> type[Json_Manager]:
        return Json_Manager