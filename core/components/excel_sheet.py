from pathlib import Path

from core.components.excel_cell import ExcelCell

# ワークシートの管理
class ExcelSheet:
    xml_path: Path
    name: str
    sheet_id: str
    r_id: str
    dirty: bool = False
    _cells: dict[str, ExcelCell] = {}

    def __init__(self, xml_path: Path, name: str, sheet_id: str, r_id: str):
        self.xml_path = xml_path
        self.name = name
        self.sheet_id = sheet_id
        self.r_id = r_id
        self.is_dirty = False

        # TODO: セルを読み込む処理
        self._cells = {}

        # ExcelCellへis_dirtyをTrueにするメソッドを持たせる
        for cell in self._cells.items():
            cell.on_change = self.mark_dirty
        pass

    def mark_dirty(self):
        """セルから呼び出されるメソッド"""
        self.is_dirty = True

    def get_cell(self, address: str) -> ExcelCell | None:
        """セルの取得"""
        if address not in self._cells.keys:
            return None
        return self._cells[address]

    def get_row(self, row: str) -> dict[str, ExcelCell]:
        """指定した行にある全てのセルの取得"""
        pass

    def get_column(self, column: str) -> dict[str, ExcelCell]:
        """指定した列にある全てのセルの取得"""
        pass
