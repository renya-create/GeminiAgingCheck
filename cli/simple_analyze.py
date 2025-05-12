import os
import json
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("エラー: GEMINI_API_KEYが環境変数に設定されていません")
    exit(1)

# Gemini APIの設定
genai.configure(api_key=api_key)

def analyze_image(image_path):
    """画像を分析して結果を返す"""
    try:
        # 画像を読み込む
        img = Image.open(image_path)
        
        # 画像サイズをチェック
        width, height = img.size
        if width > 1024 or height > 1024:
            print("警告: 画像サイズが大きすぎます。処理に時間がかかる可能性があります。")
            print("   resize_image.pyを使用してリサイズすることをお勧めします。")
        
        # モデルを初期化
        model = genai.GenerativeModel(
            'gemini-1.5-flash',  # より高速なモデル
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.0,  # より決定論的な応答
                "max_output_tokens": 256,
                "top_p": 0.95,
            }
        )
        
        # プロンプト
        prompt = """
        この建物の老朽化状態を評価し、以下のJSON形式で応答してください:
        {
          "crack_level": [0-5の整数],
          "danger_level": ["低", "中", "高"],
          "reasons": [理由を最大2つ]
        }
        
        余分なテキストは含めず、JSON形式のみで返してください。
        """
        
        # APIリクエスト
        print("Gemini APIにリクエストを送信中...")
        response = model.generate_content([prompt, img])
        
        # 結果をパース
        try:
            result = json.loads(response.text)
            print("分析成功！")
            return result
        except json.JSONDecodeError:
            print("警告: JSONとして解析できませんでした。")
            print("応答テキスト:", response.text)
            # 簡易的なデフォルト値を返す
            return {
                "crack_level": 0,
                "danger_level": "低",
                "reasons": ["解析失敗"]
            }
    
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用法: python simple_analyze.py <画像のパス>")
    else:
        image_path = sys.argv[1]
        result = analyze_image(image_path)
        if result:
            print("\n分析結果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 結果を保存
            output_path = "analysis_result.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"結果を保存しました: {output_path}")
