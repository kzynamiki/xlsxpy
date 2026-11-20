from typing import Callable, Any

# セル情報の取得・変更
class ExcelCell:
    address: str
    on_change: Callable[[], None] = None
    _value: Any = None

    def __init__(self, address: str, value: Any = None):
        self.address = address
        self._value = value
    