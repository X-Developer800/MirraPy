from ..base import MirrativError

class Validator:
    @staticmethod
    def Int(value: int | str, message: str) -> int:
        try:
            return int(value)
        except (ValueError, TypeError) as exc:
            raise MirrativError(message) from exc