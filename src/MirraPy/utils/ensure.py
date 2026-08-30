import httpx
from typing import Any
from ..base import Base, MirrativError
from .endpoints import EndPoint
from .validator import Validator

class Ensure:
    @staticmethod
    def live_id(instance, live_id: str = None) -> str:
        target_id = live_id or getattr(instance, "live_id", None)
        if not target_id: 
            raise MirrativError("live_id が指定されていません。事前に set_liveid を呼ぶか、引数を渡してください。")
        return str(target_id)
    
    @staticmethod
    async def user_exists(base, user_id: int | str) -> None:
        Validator.Int(user_id, "有効なユーザーIDを設定してください")
        params = {"q": str(user_id)}
        data = await base.get(url=EndPoint.User.SEARCH, params=params)
        if not data.get("users"): raise MirrativError("ユーザーがみつかりません。")