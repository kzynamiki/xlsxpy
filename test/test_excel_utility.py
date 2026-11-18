import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from api.excel_utility import ExcelUtility

class ExcelUtilityTest(unittest.TestCase):
    def test_extract_and_compress(self):
        xlsx_path = Path("sample.xlsx")
        temp_path = Path(".")
        need_indent = True
        result = ExcelUtility.extract_xlsx(xlsx_path, temp_path, need_indent)

        # 対象がTemporaryDirectoryオブジェクトかどうか
        self.assertIsInstance(result, TemporaryDirectory)

        # 実体としてTemporaryDirectoryが存在しているかどうかを確認する
        self.assertTrue(Path(result.name).exists())

        # TODO: ExcelUtility.compress()のテスト
        
        # TemporaryDirectoryの削除
        result.cleanup()


if __name__ == "__main__":
    unittest.main()