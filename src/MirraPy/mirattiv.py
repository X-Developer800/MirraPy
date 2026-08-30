import httpx
from .service.user import UserService
from .service.live import LiveService
from .service.collab import CollabService
from .base import Base

class Client:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client
        self._base = Base(client)
        self.user = UserService(self._base)
        self.live = LiveService(self._base)
        self.collab = CollabService(self._base)
        
    def login(self, mr_id) -> None:
        self._client.cookies.set("mr_id", mr_id, domain="www.mirrativ.com")
        
    def set_liveid(self, live_id: str) -> str:
        return self._base.set_liveid(live_id)