# AkiyaAgingCheck

空き家の老朽化状態を画像から分析するツール

## 機能

- 画像から建物の老朽化状態を分析
- ひび割れレベル、危険度、理由を自動判定
- APIサーバーとして利用可能
- CLIツールとして利用可能

## ディレクトリ構造

```
AkiyaAgingCheck/
├── api/                # APIサーバー関連
│   ├── api.py         # FastAPIサーバー
│   └── main.py        # APIサーバー起動スクリプト
├── cli/               # CLIツール関連
│   └── main.py        # CLIツール
├── resources/         # リソースファイル
│   ├── image/         # サンプル画像
│   └── prompts/       # プロンプト定義
├── src/              # コアロジック
│   ├── analyze.py     # 画像分析ロジック
│   └── schemas.py     # データモデル定義
├── output/           # 分析結果出力先
├── .env              # 環境変数設定
├── requirements.txt  # 依存パッケージ
└── README.md         # 本ファイル
```

## セットアップ

1. リポジトリをクローン
```bash
git clone https://github.com/yourusername/AkiyaAgingCheck.git
cd AkiyaAgingCheck
```

2. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

3. 環境変数の設定
`.env`ファイルを作成し、以下の内容を設定：
```
GEMINI_API_KEY=your_api_key_here
```

## 使用方法

### CLIツール

1. 単一画像の分析
```bash
python -m cli.main path/to/image.jpg
```

2. ディレクトリ内の全画像を分析
```bash
python -m cli.main --dir path/to/images
```

3. 出力ディレクトリを指定
```bash
python -m cli.main path/to/image.jpg --output-dir custom/output/dir
```

分析結果は`output`ディレクトリに保存されます：
- `analysis_summary.json`: 成功した分析結果
- `analysis_errors.json`: エラー情報
- 個別の画像分析結果: `{画像名}.json`

### APIサーバー

1. サーバーの起動
```bash
python -m api.main
```

2. APIの利用
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/image.jpg"
```

レスポンス例：
```json
{
  "crack_level": 3,
  "danger_level": "中",
  "reasons": ["壁のひび割れ", "屋根の損傷"]
}
```

## 出力形式

### 成功時
```json
{
  "crack_level": 0-5,  // ひび割れレベル（0: なし、5: 深刻）
  "danger_level": "低/中/高",  // 危険度
  "reasons": [  // 判定理由
    "理由1",
    "理由2"
  ]
}
```

### エラー時
```json
{
  "error": true,
  "message": "エラーメッセージ",
  "response": "APIレスポンス"  // オプション
}
```

## 注意事項

- 画像は`.jpg`、`.jpeg`、`.png`形式に対応
- APIキーは必ず`.env`ファイルで設定してください
- 分析結果は`output`ディレクトリに自動保存されます