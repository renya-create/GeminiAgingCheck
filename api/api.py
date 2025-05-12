import os
import uuid
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional
import tempfile

# 既存のプログラムをインポート
from src.analyze import generate_structured_report
from src.schemas import AgingReport

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="老朽化インフラ分析API",
    description="Gemini APIを使用して建物の老朽化状態を分析し、JSONレポートを返すAPI",
    version="1.0.0"
)

# CORS設定（クロスオリジンリクエストを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では特定のオリジンのみを許可するべき
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 一時ファイル保存用のディレクトリ
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
async def root():
    """APIのルートエンドポイント"""
    return {
        "message": "老朽化インフラ分析API",
        "version": "1.0.0",
        "endpoints": {
            "/analyze": "画像分析 (POST)",
            "/health": "ヘルスチェック (GET)"
        }
    }

@app.get("/health")
async def health_check():
    """APIの健全性チェック"""
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_building(file: UploadFile = File(...)):
    """
    アップロードされた建物画像を分析し、老朽化レポートを返す
    
    - **file**: 分析する建物の画像ファイル
    
    Returns:
        JSON: 老朽化分析レポート
    """
    try:
        # サポートされているファイル形式の確認
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp')):
            raise HTTPException(
                status_code=400,
                detail="サポートされていないファイル形式です。PNG, JPG, JPEG, WEBP, BMPのみ許可されています。"
            )
        
        # 一時ファイルに保存
        file_id = str(uuid.uuid4())
        temp_file_path = os.path.join(TEMP_DIR, f"{file_id}_{file.filename}")
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 画像分析の実行
        try:
            print(f"画像分析を開始: {os.path.basename(temp_file_path)}")
            
            # レポートのみ生成（高速）
            report = generate_structured_report(temp_file_path)
            
            print(f"分析完了: 危険度「{report.get('danger_level', '不明')}」")
            
            # 一時ファイルの削除
            os.remove(temp_file_path)
            print(f"一時ファイル削除: {os.path.basename(temp_file_path)}")
            
            return report
            
        except Exception as e:
            # 画像分析中のエラー
            raise HTTPException(
                status_code=500,
                detail=f"画像分析中にエラーが発生しました: {str(e)}"
            )
    
    except Exception as e:
        # その他の予期しないエラー
        raise HTTPException(
            status_code=500,
            detail=f"サーバーエラー: {str(e)}"
        )

@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    print("老朽化インフラ分析APIを起動しています...")
    # 一時ディレクトリのクリーンアップ
    for file in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"一時ファイル削除中にエラー: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    print("APIをシャットダウンしています...")
    # 一時ディレクトリのクリーンアップ
    for file in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"一時ファイル削除中にエラー: {e}")

# 直接実行された場合
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
