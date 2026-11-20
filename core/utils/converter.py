from pathlib import Path
from tempfile import TemporaryDirectory
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom as Minidom
import zipfile
import os


def xlsx_to_dir(xlsx_path: Path, temp_path: Path = Path(".")) -> TemporaryDirectory[str]:
    """一時フォルダへエクセルファイルを展開"""
    temp_dir = TemporaryDirectory(prefix=".", dir=temp_path)
    temp_dir_path = Path(temp_dir.name)

    try:
        # zipfileで一時ディレクトリへ全展開
        with zipfile.ZipFile(xlsx_path, mode="r") as zf:
            zf.extractall(path=temp_dir_path)
        
        return temp_dir
    except:
        # 例外発生時に消して処理を終わらせる
        temp_dir.cleanup()
        raise  


def dir_to_xlsx(xlsx_path: Path, temporary_dir: TemporaryDirectory[str]):
    """一時フォルダの中身を圧縮してエクセルファイルへ戻す"""
    # 圧縮して*.xlsxへ変換
    tmp_path = Path(temporary_dir.name)
    with zipfile.ZipFile(xlsx_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for folder, subfolders, files in os.walk(tmp_path):
            for file in files:
                file_path = os.path.join(folder, file)
                relpath = os.path.relpath(file_path, tmp_path)
                zf.write(file_path, relpath)

    # 一時フォルダの削除
    temporary_dir.cleanup()
