import os
import unittest
from pathlib import Path

from core.components.excel_file import ExcelFile
from core.components.excel_sheet import ExcelSheet


class ExcelFileTest(unittest.TestCase):
    def setUp(self):
        self.xlsx_path = Path("sample.xlsx")
        self.dest_excel_file_path = Path("excelfiletest.xlsx")

    def test_excel_file(self):
        excel_file = ExcelFile(self.xlsx_path)

        # excel_fileのオブジェクトの型を確認
        self.assertIsInstance(excel_file, ExcelFile)

        # sample.xlsxのシートの確認
        sheets = excel_file.get_sheets()
        sheetNames = list(map(lambda sheet: sheet.name, sheets))
        self.assertIn("Sheet1", sheetNames)
        self.assertIn("Sheet2", sheetNames)

        # シートの取得: 名前から
        self.assertIsInstance(excel_file.get_sheet_by(name="Sheet1"), ExcelSheet)
        self.assertIsInstance(excel_file.get_sheet_by(name="Sheet2"), ExcelSheet)

        # シートの取得: シートIDから
        self.assertIsInstance(excel_file.get_sheet_by(sheet_id="1"), ExcelSheet)
        self.assertIsInstance(excel_file.get_sheet_by(sheet_id="2"), ExcelSheet)

        # シートの取得: リレーションIDから
        self.assertIsInstance(excel_file.get_sheet_by(r_id="rId1"), ExcelSheet)
        self.assertIsInstance(excel_file.get_sheet_by(r_id="rId2"), ExcelSheet)

        # 実体として保存したエクセルファイルが存在しているかどうかを確認する
        excel_file.save(self.dest_excel_file_path)
        self.assertTrue(self.dest_excel_file_path.exists())

        # 削除
        os.remove(self.dest_excel_file_path)


if __name__ == "__main__":
    unittest.main()