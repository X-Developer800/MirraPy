from typing import NamedTuple, Any

class Status(NamedTuple):
    alive: bool
    collab_enabled: bool
    raw: dict[str, Any]