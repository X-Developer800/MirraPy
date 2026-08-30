import urllib.parse
import re
from ..base import MirrativError

class Extract:
    @staticmethod
    def url(url: str) -> str | None:
        if not isinstance(url, str):
            raise MirrativError("URLは文字列である必要があります。")
        
        match = re.search(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', url)
        if not match:
            return None
            
        extracted_url = match.group(0)
        
        try:
            decoded_url = urllib.parse.unquote(extracted_url)
        except Exception as exc:
            raise MirrativError("URLのデコードに失敗しました。") from exc
        
        live_match = re.search(r'/live/([a-zA-Z0-9_-]+)', decoded_url)
        if live_match:
            return live_match.group(1)
            
        return None