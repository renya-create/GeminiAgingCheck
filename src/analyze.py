import os
import json
import base64
from typing import Optional, Dict
from PIL import Image
import google.generativeai as genai
from src.schemas import AgingReport

# 環境変数から設定を読み込む
from dotenv import load_dotenv
load_dotenv()

# Gemini API設定
API_KEY = os.getenv("GEMINI_API_KEY", "")

def init_api():
    """Google Generative AI APIの初期化"""
    if not API_KEY:
        raise ValueError("GEMINI_API_KEYが設定されていません")
    genai.configure(api_key=API_KEY)

def generate_structured_report(img_path: str) -> AgingReport:
    """構造化レポート生成"""
    # 画像の前処理
    img = Image.open(img_path)
    
    # モデル初期化
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # プロンプトの読み込み
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              'prompts', 'aging_check.json')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_data = json.load(f)
    
    # APIリクエスト
    try:
        response = model.generate_content([
            prompt_data['system_prompt'],
            img,
            f"出力スキーマ: {json.dumps(prompt_data['output_schema'], ensure_ascii=False)}"
        ])
        
        # JSONとしてパース
        result = json.loads(response.text)
        return AgingReport(**result)
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return AgingReport(
            crack_level=0,
            danger_level="低",
            reasons=[f"エラー: {str(e)}"]
        )

def analyze_image(image_path: str) -> Optional[Dict]:
    """画像分析のメイン処理"""
    try:
        # API初期化
        init_api()
        
        # レポート生成
        print(f"画像を分析中: {image_path}")
        report = generate_structured_report(image_path)
        
        # 結果をJSONファイルとして保存
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.basename(image_path)
        json_path = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}.json")
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report.dict(), f, ensure_ascii=False, indent=2)

        return {
            "image": image_path,
            "report": report.dict()
        }
    except Exception as e:
        print(f"エラー: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = analyze_image(image_path)
        if result:
            print("\n分析結果:")
            print(json.dumps(result["report"], indent=2, ensure_ascii=False))
    else:
        print("使用法: python analyze.py <画像パス>")