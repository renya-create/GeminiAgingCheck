import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance

def resize_image(image_path, max_size=1024):
    """画像をAPIに適したサイズにリサイズする"""
    img = Image.open(image_path)
    
    # アスペクト比を維持しながらリサイズ
    width, height = img.size
    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        
        img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # 処理した画像を一時ファイルとして保存
    output_dir = os.path.join(os.path.dirname(image_path), "processed")
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.basename(image_path)
    output_path = os.path.join(output_dir, f"resized_{base_name}")
    img.save(output_path)
    
    return output_path

def enhance_image(image_path):
    """画像のコントラストと鮮明さを強調する"""
    img = Image.open(image_path)
    
    # コントラスト強調
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)  # コントラスト強調係数
    
    # シャープネス強調
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.5)  # シャープネス強調係数
    
    # 処理した画像を保存
    output_dir = os.path.dirname(image_path)
    base_name = os.path.basename(image_path)
    output_path = os.path.join(output_dir, f"enhanced_{base_name}")
    img.save(output_path)
    
    return output_path

def detect_edges(image_path):
    """OpenCVを使用してエッジ検出を行う（ひび割れ強調）"""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # ノイズ除去
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # エッジ検出（Canny）
    edges = cv2.Canny(blurred, 50, 150)
    
    # オリジナル画像とエッジを組み合わせる
    edge_highlighted = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    result = cv2.addWeighted(img, 0.8, edge_highlighted, 0.2, 0)
    
    # 処理した画像を保存
    output_dir = os.path.dirname(image_path)
    base_name = os.path.basename(image_path)
    output_path = os.path.join(output_dir, f"edges_{base_name}")
    cv2.imwrite(output_path, result)
    
    return output_path

def preprocess_pipeline(image_path):
    """画像前処理パイプライン"""
    # リサイズ
    resized_path = resize_image(image_path)
    
    # コントラスト強調
    enhanced_path = enhance_image(resized_path)
    
    # エッジ検出（必要に応じて）
    # edge_path = detect_edges(enhanced_path)
    
    return enhanced_path

if __name__ == "__main__":
    # テスト用
    import sys
    if len(sys.argv) > 1:
        input_image = sys.argv[1]
        output_path = preprocess_pipeline(input_image)
        print(f"処理済み画像: {output_path}")
    else:
        print("使用法: python preprocess.py <画像パス>")