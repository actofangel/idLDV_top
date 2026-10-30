# idLDV
The Identity of Leonardo da Vinci

(Project2)

[Visit our Wiki](https://github.com/actofangel/idLDV/wiki)

[Web Resource](https://github.com/actofangel/idLDV/wiki/Links1)

## サイト構成

GitHub Pages（ブランチ `main`、ルート）でそのまま公開できる静的サイトです。各ページは CSS を内包した単一ファイル HTML です。

| ファイル | 内容 |
|---|---|
| `index.html` | 概要、記述の三区分（事実、解釈、仮説） |
| `method.html` | 研究方法：レイヤー純度、ソース許容規則、検証可能性 |
| `last-supper.html` | 最後の晩餐の三層分析モデルと作業仮説 |
| `database.html` | 参照データベースの閲覧（`data/*.json` を読み込む） |
| `sources.html` | 許容ソースのカテゴリと登録済み資料 |

## 参照データベース

```
data/
  works.json                  作品（事実層のみ）
  datings.json                年代（事実層または解釈層）
  attributions.json           帰属（解釈層のみ）
  source_records.json         ソース記録（許容カテゴリのみ）
  interpretation_claims.json  解釈主張と作業仮説
  schema/                     各コレクションの JSON スキーマ
```

レコードを追加したら検証を実行します。`data/` を変更した push では GitHub Actions でも自動実行されます。

```bash
pip install jsonschema
python3 tools/validate.py
```

検証内容：スキーマ準拠、すべての典拠が `source_records.json` に登録済みであること、解釈層と仮説層に確実度「事実」を付けていないこと、ID の一意性と参照整合性。反証条件のない解釈主張と、検証スクリプトのない幾何学的主張は警告になります。
