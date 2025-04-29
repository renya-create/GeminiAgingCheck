# GeminiAgingCheck

Gemini APIを活用した老朽化インフラ分析CLIツール
空き家の写真を分析してJSONフォーマットで空き家の老朽化レベルを分析するレポートを生成

## 機能

- 建物・インフラの老朽化状態を画像から分析
- ひび割れレベル、変色割合、危険度の評価
- 構造化されたJSONレポート生成
- 複数画像の一括処理

## インストール方法

1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/GeminiAgingCheck.git
cd GeminiAgingCheck
```

2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

3. 環境設定

`.env_template`ファイルを`.env`にコピーし、Gemini APIキーを設定します。

```bash
cp .env_template .env
# .envファイルを編集してAPIキーを設定
```

## 使い方

### 1. 環境設定

1. Gemini APIキーの取得
   - [Google AI Studio](https://makersuite.google.com/app/apikey)でAPIキーを取得
   - `.env_template`を`.env`にコピーし、取得したAPIキーを設定

```bash
cp .env_template .env
# .envファイルを編集してGEMINI_API_KEYを設定
```

2. 仮想環境のセットアップ（推奨）

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# または
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. 基本的な使用方法

#### 単一画像の分析

```bash
python main.py image/example.jpg
```

出力：
- `output/`ディレクトリにJSONレポートが生成されます

#### 複数画像の一括分析

```bash
python main.py --dir image/
```

- 指定ディレクトリ内の全画像を分析
- 各画像ごとに個別のレポートを生成
- `output/analysis_summary.json`に全結果のサマリーを保存

### 3. オプション

- `--output-dir`: 出力ディレクトリの指定（デフォルト: output）

例：
```bash
python main.py image/example.jpg --output-dir reports/
```

## 出力例

```json
{
  "crack_level": 3,
  "discoloration_percent": 45.2,
  "danger_level": "中",
  "reasons": [
    "壁面に網目状のひび割れが確認",
    "排水口周辺に藻の繁殖"
  ],
  "maintenance_advice": [
    "防水コーティングの塗り直し",
    "排水路の清掃を実施"
  ]
}
```

## プロジェクト構成

```
GeminiAgingCheck/
├── .env                # 環境変数
├── image/              # 分析対象の画像を格納
├── output/             # 生成されたレポートの出力先
├── prompts/            # AIへの指示プロンプト
│   └── aging_check.json # JSONスキーマを含むプロンプト定義
├── src/
│   ├── analyze.py      # メイン処理・AI連携
│   └── schemas.py      # 出力JSONの型定義
├── main.py             # 実行スクリプト
└── requirements.txt    # 依存パッケージ
```

## 技術スタック

- Python 3.9+
- Google Generative AI (Gemini)
- Pillow（画像処理）

## 注意事項

- Gemini APIキーが必要です
- 分析結果は参考情報であり、専門家の判断を代替するものではありません
- 対応画像形式: JPEG, PNG
