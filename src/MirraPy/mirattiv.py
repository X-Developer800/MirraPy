import httpx
from .service.user import UserService
from .service.live import LiveService
from .service.util import UtilService
from .base import Base

class Client:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client
        self._base = Base(client)
        self.user = UserService(self._base)
        self.live = LiveService(self._base)
        self.util = UtilService(self._base)
        
    def login(self, mr_id) -> None:
        self._client.cookies.set("mr_id", mr_id, domain="www.mirrativ.com")