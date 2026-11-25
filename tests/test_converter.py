import os
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

import core.utils.converter as Converter


class ConverterTest(unittest.TestCase):
    def setUp(self):
        self.xlsx_path = Path("sample.xlsx")
        self.temp_path = Path(".")

    def test_extract_and_compress(self):
        # TemporaryDirectory生成
        result = Converter.xlsx_to_dir(self.xlsx_path, self.temp_path)
        
        # 対象がTemporaryDirectoryオブジェクトかどうか
        self.assertIsInstance(result, TemporaryDirectory)
    
        # 実体としてTemporaryDirectoryが存在しているかどうかを確認する
        self.assertTrue(Path(result.name).exists())
    
        # xlsxの圧縮生成
        file = Path(f"{result.name}.xlsx")
        Converter.dir_to_xlsx(file, result)
    
        # 実体として圧縮したxlsxが存在しているかどうかを確認する
        self.assertTrue(file.exists())
    
        # xlsxを削除
        os.remove(file)


if __name__ == "__main__":
    unittest.main()