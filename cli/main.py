import os
import json
import argparse
from src.analyze import analyze_image

def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description='画像から老朽化状態を分析')
    parser.add_argument('image_path', nargs='?', help='分析する画像のパス')
    parser.add_argument('--dir', help='分析する画像が格納されたディレクトリ')
    parser.add_argument('--output-dir', help='出力ディレクトリ', default='output')
    args = parser.parse_args()

    if args.dir:
        process_directory(args.dir)
    elif args.image_path:
        process_single_image(args.image_path, args.output_dir)
    else:
        print("使用方法:")
        print("  単一画像: python main.py <画像パス>")
        print("  ディレクトリ: python main.py --dir <ディレクトリパス>")
        print("  出力ディレクトリ指定: python main.py <画像パス> --output-dir <出力ディレクトリ>")

def process_directory(directory_path):
    """ディレクトリ内の全画像を処理"""
    if not os.path.isdir(directory_path):
        print(f"エラー: ディレクトリが見つかりません: {directory_path}")
        return
    
    # 画像ファイルを検索
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_files = []
    
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(file_path)
    
    if not image_files:
        print(f"画像ファイルが見つかりません: {directory_path}")
        return
    
    # 一括処理
    results = []
    errors = []
    for img_path in image_files:
        print(f"\n処理中: {os.path.basename(img_path)}")
        result = analyze_image(img_path)
        if result:
            if isinstance(result, dict) and result.get("error"):
                error_info = {
                    "image": os.path.basename(img_path),
                    "error": result["message"]
                }
                errors.append(error_info)
                print(f"分析エラー: {result['message']}")
            else:
                print("\n分析結果:")
                print(json.dumps(result["report"], indent=2, ensure_ascii=False))
                results.append({
                    "image": os.path.basename(img_path),
                    "report": result["report"]
                })
    
    # 結果のサマリーを保存
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    if results:
        summary_path = os.path.join(output_dir, "analysis_summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n分析サマリーを保存しました: {summary_path}")
    
    if errors:
        error_path = os.path.join(output_dir, "analysis_errors.json")
        with open(error_path, 'w', encoding='utf-8') as f:
            json.dump(errors, f, indent=2, ensure_ascii=False)
        print(f"\nエラー情報を保存しました: {error_path}")

def process_single_image(image_path, output_dir):
    """単一画像を処理"""
    result = analyze_image(image_path)
    if result:
        if isinstance(result, dict) and result.get("error"):
            print(f"\n分析エラー: {result['message']}")
            if "response" in result:
                print(f"レスポンス: {result['response']}")
        else:
            print("\n分析結果:")
            print(json.dumps(result["report"], indent=2, ensure_ascii=False))
            print(f"\n結果を保存しました: {os.path.join(output_dir, os.path.splitext(os.path.basename(image_path))[0] + '.json')}")

if __name__ == "__main__":
    main()