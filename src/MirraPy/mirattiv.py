import httpx
from .service.user import UserService
from .service.live import LiveService
from .service.util import UtilService

class Client:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client
        self.user = UserService(client)
        self.live = LiveService(client)
        self.util = UtilService(client)
        
    def login(self, mr_id) -> None:
        self._client.cookies.set("mr_id", mr_id, domain="www.mirrativ.com")