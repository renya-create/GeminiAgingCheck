import os
import json
import base64
from typing import Optional, Dict
from PIL import Image
import google.generativeai as genai
from src.schemas import AgingReport
from dotenv import load_dotenv

def load_env() -> str:
    """
    環境変数の読み込みと検証
    
    Returns:
        str: GEMINI_API_KEYの値
        
    Raises:
        FileNotFoundError: .envファイルが見つからない場合
        ValueError: GEMINI_API_KEYが設定されていない場合
    """
    # プロジェクトのルートディレクトリを取得
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(project_root, '.env')
    
    # .envファイルの存在確認
    if not os.path.exists(env_path):
        raise FileNotFoundError(f".envファイルが見つかりません: {env_path}")
    
    # 現在の環境変数をクリア
    if 'GEMINI_API_KEY' in os.environ:
        del os.environ['GEMINI_API_KEY']
    
    # 環境変数の読み込み（override=Trueを指定）
    load_dotenv(env_path, override=True)
    
    # APIキーの取得と検証
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEYが.envファイルに設定されていません")
    
    return api_key

# Gemini API設定
API_KEY = load_env()

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
        
        # 必要なキーが存在するか確認
        required_keys = ['crack_level', 'danger_level', 'reasons']
        for key in required_keys:
            if key not in result:
                raise ValueError(f"レスポンスに必要なキー '{key}' が含まれていません")
        
        return AgingReport(**result)
        
    except json.JSONDecodeError as e:
        print(f"JSONパースエラー: {str(e)}")
        print(f"レスポンス: {response.text}")
        return AgingReport(
            crack_level=0,
            danger_level="低",
            reasons=[f"JSONパースエラー: {str(e)}"]
        )
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
        
        # AgingReportを辞書に変換
        report_dict = {
            "crack_level": report["crack_level"],
            "danger_level": report["danger_level"],
            "reasons": report["reasons"]
        }
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_dict, f, ensure_ascii=False, indent=2)

        return {
            "image": image_path,
            "report": report_dict
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