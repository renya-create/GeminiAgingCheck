# GeminiAgingCheck API

Gemini APIを活用した老朽化インフラ分析ツールのAPI版です。画像をアップロードして、JSON形式でレポートを受け取ることができます。

## 機能

- RESTful APIインターフェース（FastAPI実装）
- 画像アップロードによる老朽化分析
- 構造化されたJSONレスポンス
- ヒートマップ生成オプション
- コンテナ化対応（Docker）

## インストールと実行

### 1. 依存パッケージのインストール

```bash
pip install -r api-requirements.txt
```

### 2. APIサーバーの起動

```bash
python api.py
```

これでAPIサーバーが`http://localhost:8000`で起動します。

### 3. Docker使用時

```bash
# イメージのビルド
docker build -t gemini-aging-check-api .

# コンテナの実行（APIキーを環境変数で渡す）
docker run -p 8000:8000 -e GEMINI_API_KEY=あなたのAPIキー gemini-aging-check-api
```

## APIエンドポイント

### 1. ルートエンドポイント

- URL: `/`
- メソッド: `GET`
- 説明: APIの基本情報を返します

### 2. ヘルスチェック

- URL: `/health`
- メソッド: `GET`
- 説明: APIサーバーの状態を確認します

### 3. 画像分析

- URL: `/analyze`
- メソッド: `POST`
- パラメータ:
  - `file`: 分析する画像ファイル（必須）
  - `generate_heatmap`: ヒートマップを生成するかどうか（オプション、デフォルト: false）
- レスポンス: JSON形式の老朽化レポート

## クライアント使用例

付属の`client_example.py`スクリプトを使用して、APIを簡単に呼び出すことができます：

```bash
# サンプル画像を分析
python client_example.py ./image/sample.png

# 別のAPIエンドポイントを指定
python client_example.py ./image/sample.png http://example.com/analyze
```

## cURLによる呼び出し例

```bash
curl -X POST -F "file=@./image/sample.png" http://localhost:8000/analyze
```

## レスポンス例

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

## 本番環境での注意点

- CORS設定を適切に調整（現在は全オリジンを許可）
- APIキー認証などのセキュリティ強化
- ファイルサイズ制限の追加
- レート制限の実装
- 高可用性のためのロードバランシング

## トラブルシューティング

1. **APIサーバーに接続できない**
   - サーバーが起動しているか確認
   - ポート8000が他のアプリケーションで使用されていないか確認

2. **画像分析エラー**
   - APIキーが正しく設定されているか確認
   - サポートされている画像形式（PNG, JPG, JPEG, WEBP, BMP）か確認

3. **Dockerコンテナが起動しない**
   - 環境変数が正しく設定されているか確認
   - ポートの衝突がないか確認
