import requests
import json
import sys
import os
from pprint import pprint

"""
APIクライアント例 - 老朽化インフラ分析APIの使用例
"""

def analyze_image(image_path, api_url="http://localhost:8000/analyze"):
    """
    指定された画像をAPIに送信し、分析結果を取得する
    
    Args:
        image_path (str): 分析する画像ファイルのパス
        api_url (str): 分析APIのエンドポイントURL
        
    Returns:
        dict: 分析結果のJSONレスポンス
    """
    # 画像ファイルの存在確認
    if not os.path.exists(image_path):
        print(f"エラー: 指定されたファイル '{image_path}' が見つかりません。")
        return None
    
    # ファイル拡張子の確認
    if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp')):
        print("エラー: サポートされていないファイル形式です。PNG, JPG, JPEG, WEBP, BMPのみ許可されています。")
        return None
    
    try:
        # リクエストの準備
        files = {'file': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')}
        
        # APIリクエスト送信
        print(f"画像 '{os.path.basename(image_path)}' を分析中...")
        print("リクエスト送信中... (最大60秒待機)")
        response = requests.post(api_url, files=files, timeout=60)
        
        # レスポンスのステータスコード確認
        if response.status_code == 200:
            print("分析成功!")
            return response.json()
        else:
            print(f"エラー: APIから {response.status_code} レスポンスを受信しました")
            print(f"詳細: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"エラー: APIサーバー ({api_url}) に接続できません。サーバーが実行中か確認してください。")
        return None
    except requests.exceptions.Timeout:
        print(f"エラー: リクエストがタイムアウトしました。サーバーが処理に時間がかかっているか、負荷が高い可能性があります。")
        print("画像サイズを小さくするか、サーバー側の処理能力を確認してください。")
        return None
    except Exception as e:
        print(f"予期しないエラーが発生しました: {str(e)}")
        return None
        
def save_report(report, output_path):
    """分析レポートをJSONファイルとして保存"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"レポートを保存しました: {output_path}")

def main():
    """メイン実行関数"""
    if len(sys.argv) < 2:
        print("使用法: python client_example.py <画像パス> [API URL]")
        print("例: python client_example.py ./image/sample.png http://localhost:8000/analyze")
        return
    
    # 引数の取得
    image_path = sys.argv[1]
    api_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000/analyze"
    
    # 画像分析
    result = analyze_image(image_path, api_url)
    
    if result:
        # 結果の表示
        print("\n分析結果:")
        pprint(result)
        
        # レポートの保存
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        save_report(result, f"{base_name}_api_report.json")
        
        # 危険度の警告表示
        if result.get("danger_level") == "高":
            print("\n⚠️ 警告: この建物は高い危険度と評価されています！")
            print(f"理由: {', '.join(result.get('reasons', []))}")

if __name__ == "__main__":
    main()
