from pathlib import Path
from tempfile import TemporaryDirectory
import re
import xml.etree.ElementTree as ET
import zipfile


# 解析・変換
class ExcelUtility:
    def extract_xlsx(xlsx_path: Path, temp_path: Path = Path("."), need_indent: bool = False) -> TemporaryDirectory[str]:
        """一時フォルダへエクセルファイルを展開"""
        temp_dir = TemporaryDirectory(prefix=".", dir=temp_path.name)
        temp_dir_path = Path(temp_dir.name)

        # zipfileで一時ディレクトリへ全展開
        with zipfile.ZipFile(xlsx_path, mode="r") as zf:
            zf.extractall(path=temp_dir_path)

        for xml_file in temp_dir_path.rglob("*.xml"):

            # xmlnsのタグがns0などに置換されるのを防ぐために自動で取得する
            for _, (prefix, uri) in ET.iterparse(xml_file, events=["start-ns"]):
                if not re.match(r"^ns\d+$", prefix):
                    ET.register_namespace(prefix, uri)

            # インデントが必要ならインデントをする
            if need_indent:
                tree = ET.parse(xml_file)
                ET.indent(tree, space="  ")

            # 生成された*.xmlへフォーマットの適用
            tree.write(xml_file, encoding="utf-8", xml_declaration=True)

        return temp_dir

    def compress_xlsx(xlsx_path: Path, temporary_dir: TemporaryDirectory[str]):
        """一時フォルダの中身を圧縮してエクセルファイルへ戻す"""
        # TODO: 圧縮して*.xlsxへ変換する処理
        temporary_dir.cleanup()
