import google.generativeai as genai
import os
from dotenv import load_dotenv
import sys

# .envファイルから環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("エラー: GEMINI_API_KEYが環境変数に設定されていません")
    sys.exit(1)

# APIキーを設定
genai.configure(api_key=api_key)

# モデルを選択
model = genai.GenerativeModel('gemini-pro')

# テキスト生成
response = model.generate_content("Explain how AI works in a few words")
print(response.text)

