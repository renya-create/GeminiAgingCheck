from PIL import Image
import os

def resize_image(input_path, output_path=None, max_size=1024):
    """画像のサイズを確認し、必要に応じてリサイズする"""
    try:
        # 画像を開く
        img = Image.open(input_path)
        
        # 現在のサイズを取得
        width, height = img.size
        print(f"元の画像サイズ: {width}x{height} ピクセル")
        
        # ファイルサイズを確認
        file_size = os.path.getsize(input_path) / (1024 * 1024)  # MB単位
        print(f"ファイルサイズ: {file_size:.2f} MB")
        
        # サイズが大きい場合はリサイズ
        if width > max_size or height > max_size:
            print(f"画像サイズが大きいため、最大{max_size}ピクセルにリサイズします")
            
            # アスペクト比を維持したままリサイズ
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))
            
            # リサイズ実行
    img = img.resize((new_width, new_height), Image.LANCZOS)
    print(f"新しいサイズ: {new_width}x{new_height} ピクセル")
    
    # 出力パスが指定されていない場合はデフォルトを設定
    if not output_path:
        filename, ext = os.path.splitext(input_path)
        output_path = f"{filename}_resized{ext}"
    
    # 圧縮パラメータを設定
    save_params = {}
    if ext.lower() in ['.jpg', '.jpeg']:
        save_params = {'quality': 85, 'optimize': True}  # JPEGの場合は圧縮品質を指定
    elif ext.lower() == '.png':
        save_params = {'optimize': True}  # PNGの場合は最適化
        
    # リサイズした画像を保存
    img.save(output_path, **save_params)
    print(f"リサイズした画像を保存しました: {output_path}")
            
            # 新しいファイルサイズを確認
            new_file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB単位
            print(f"新しいファイルサイズ: {new_file_size:.2f} MB")
            
            return output_path
        else:
            print("画像サイズは適切です。リサイズは不要です。")
            return input_path
            
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用法: python resize_image.py <画像のパス> [出力パス]")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        resize_image(input_path, output_path)
