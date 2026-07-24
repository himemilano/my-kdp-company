import os
import json
import yaml
from google import genai
from scripts.generate_cover import generate_cover_pdf
from scripts.generate_interior import generate_interior_pdf

def main():
    print("🚀 [KDP出版部] 自律オーケストレーター起動中（API認証・プロジェクト個別完全汎用版）...")

    # 1. Gemini APIの秘匿キー検証と初期化
    api_key = os.environ.get("GEMINI_API_KEY_MY_KDP")
    if not api_key:
        raise ValueError("❌ 秘匿キー 'GEMINI_API_KEY_MY_KDP' が環境変数に見つかりません。")
        
    client = genai.Client(api_key=api_key)
    MODEL_NAME = "gemini-2.5-flash"
    print(f"🤖 使用モデル: {MODEL_NAME}")

    # 2. config.yml からアクティブなプロジェクトのslugを動的取得
    config_path = "config.yml"
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
            
    project_slug = config.get("project", {}).get("name", "01_tranquil_flora")
    project_root = f"projects/{project_slug}"
    workspace_dir = os.path.join(project_root, "kdp_workspace")
    output_dir = os.path.join(project_root, "output")
    
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # 3. アクティブプロジェクト情報の書き出し
    active_info = {
        "project_root": project_root,
        "project_slug": project_slug,
        "title": "Tranquil Flora: A Japanese Minimalist Botanical Coloring Book for Adults"
    }
    with open("active_project.json", "w", encoding="utf-8") as f:
        json.dump(active_info, f, ensure_ascii=False, indent=2)

    print(f"📂 アクティブプロジェクト: {project_slug} ({active_info['title']})")

    # 4. Step 1: 本文PDFビルド（プロジェクトslugを渡して汎用実行）
    print("\n--- [Step 1] 本文PDFビルド ---")
    interior_pdf = generate_interior_pdf(project_slug)

    # 5. Step 2: 表紙カバーPDFビルド（プロジェクトslugを渡して汎用実行）
    print("\n--- [Step 2] 表紙カバー見開きPDFビルド ---")
    cover_pdf = generate_cover_pdf(project_slug)

    print(f"\n✨ すべての自動処理が正常に完了しました。")
    print(f"📦 成果物格納先: {output_dir}/Interior.pdf および {output_dir}/Cover.pdf")

if __name__ == "__main__":
    main()
