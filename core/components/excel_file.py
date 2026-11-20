from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tempfile import TemporaryDirectory

from pathlib import Path
import xml.etree.ElementTree as ET

import core.utils.converter as Converter
from core.components.excel_sheet import ExcelSheet

# Excelファイル全体の管理
class ExcelFile:
    xlsx_path: Path
    temp_dir: TemporaryDirectory[str]
    temp_dir_path: Path
    sheets: list[ExcelSheet] = []

    def __init__(self, xlsx_path: Path):
        # 解凍
        self.xlsx_path = xlsx_path
        self.temp_dir = Converter.xlsx_to_dir(xlsx_path, Path("."))
        self.temp_dir_path = Path(self.temp_dir.name)

        # workbookから各Sheetを格納
        workbook = ET.parse(self.temp_dir_path.joinpath("xl").joinpath("workbook.xml")).getroot()
        for sheet in workbook.find("{*}sheets").findall("{*}sheet"):
            xml_path = self.temp_dir_path.joinpath("xl").joinpath("worksheets")
            name, sheet_id, r_id = dict(sheet.items()).values()
            excel_sheet = ExcelSheet(xml_path, name, sheet_id, r_id)

            self.sheets.append(excel_sheet)
        
    def get_sheets(self) -> list[ExcelSheet]:
        """すべてのシートを取得"""
        return self.sheets

    def get_sheet_by(self, name: str = "", sheet_id: str = "", r_id: str = "") -> ExcelSheet | None:
        """任意の値からシートを取得"""
        for sheet in self.sheets:
            if sheet.name == name:
                return sheet
            if sheet.sheet_id == sheet_id:
                return sheet
            if sheet.r_id == r_id:
                return sheet

        return None

    def save(self, dest: Path = None):
        """ファイルを保存して書き込む"""
        if dest is None:
            dest = self.xlsx_path

        Converter.dir_to_xlsx(dest, self.temp_dir)
