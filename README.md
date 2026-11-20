# xlsxpy
Excelの内部構造解析及びAPI


## ■ 目的
スキルマップのエクセルシートなどを扱うにあたって、折り畳みや絞り込みが極めて複雑であることから、自分用にちょっとしたアプリケーションを作りたい。  
しかし、外部のライブラリ利用はソフトウェア利用申請が必要になるので、自分でAPIを実装すればよいのではないかというほんの好奇心。


## ■ 解析に使う環境について
- Python 3を使う。  
- 追加のライブラリは使わず、*.xlsxそのものを解体して解析する。  


## ■ 主要な標準ライブラリ
- unittest
    - 単体テストの標準ライブラリ
- xml.etree.ElementTree
    - *.xmlを解析する標準ライブラリ
    - 場合によっては、 `xml.dom.minidom` も検討


## ■ 実装予定の機能
- エクセルファイルの読み込み
- エクセルファイルを再生成
- 最終更新日などのメタデータ取得 (あれば)
- シートの取得
- セルの取得
- セルの変更


## ■ 実装を予定しない機能
- 列や行の追加
    - これをするのは基本的にエクセルファイルで編集すべきと判断。
    - リレーションの複雑さや、列や行を入れるだけでそれより下や右の要素すべてへ更新が走るため、この点をどう綺麗に実装するかを検討する必要がある。


## ■ 参照したドキュメント
- https://docs.python.org/ja/3/library/os.html
- https://docs.python.org/ja/3/library/pathlib.html
- https://docs.python.org/ja/3/library/tempfile.html
- https://docs.python.org/ja/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
- https://docs.python.org/ja/3/library/zipfile.html
- https://learn.microsoft.com/ja-jp/dotnet/api/documentformat.openxml.spreadsheet?view=openxml-3.0.1


## ■ プロジェクト構造
```mermaid
classDiagram
    direction LR

    class ExcelFile {
        <<core/components/excel_file.py>>
        +Path xlsx_path
        +TemporaryDirectory temp_dir
        +Path temp_dir_path
        +list~ExcelSheet~ sheets

        +list~ExcelSheet~ get_sheets()
        +ExcelSheet get_sheet_by()
        +save()
    }

    class ExcelSheet {
        <<core/components/excel_sheet.py>>
        +Path xml_path
        +str name
        +str sheet_id
        +str r_id
        +bool dirty
        +dict~str, ExcelCell~ cells

        +mark_dirty()
        +ExcelCell get_cell()
        +dict~str, ExcelCell~ get_row()
        +dict~str, ExcelCell~ get_column()
    }

    class ExcelCell {
        <<core/components/excel_cell.py>>
        +str address
        +Any value
        -Callable~[], None~ on_change
    }

    class Converter {
        <<core/components/converter.py>>

        +TemporaryDirectory xlsx_to_dir()
        +dir_to_xlsx()
    }

    ExcelFile o-- "0..*" ExcelSheet : 集約
    ExcelSheet o-- "0..*" ExcelCell : 集約
    ExcelCell --> "1" ExcelSheet : 参照・dirty通知
    Converter ..> ExcelFile : 利用・変換
```
※2026/11/13時点


## ■ 責務
### ExcelCell
セルの要素や、番地などの情報を扱う。  
更新がされた場合にコールバックより、ExceSheetでdirtyフラグを立てる。

### ExcelSheet
シートの名前やアクティブセル、リレーションなどの情報を扱う。  
このクラスでセルの集約を行っている。

### ExcelFile
エクセルファイルは最終更新日や人などの情報が入っている場合があるため、その情報を扱う。  
このクラスでExcelSheetの集約を行っている。

### Converter
\*.xlsx形式のファイルからxmlを抽出する規定処理と、抽出したxml群を圧縮して\*.xlsx形式へ戻す処理を担う。


## ■ sample.xlsxの要素
### Sheet1
| | A | B | C |
|:---:|:---:|:---:|:---:|
| **1** | このセルはA1です |  |  |
| **2** |  | Here is B2 |  |
| **3** |  |  | 123 |

### Sheet2
| | A | B | C |
|:---:|:---:|:---:|:---:|
| **1** |  |  | このセルはC1です |
| **2** | Here is A2 |  |  |
| **3** |  | 456 | |


## ■ テストの実装
本プロジェクトでは、取り組みの一環としてテストの実装と運用を行う。  
作成に当たって、以下を参考にした。

- https://qiita.com/KENTAROSZK/items/ae40bd509d0c114c3519
- https://docs.kanaries.net/ja/topics/Python/python-unittest


## ■ 備考
- リレーション周りがおそらく複雑なので、それらを処理するクラスを用意したほうがいいかもしれない。