import os
import json
import yaml
from google import genai
from scripts.generate_cover import generate_cover_pdf
from scripts.generate_interior import generate_interior_pdf

def main():
    print("🚀 [KDP出版部] 自律オーケストレーター起動中（完全統合・CSV廃止版）...")

    # 1. APIキーの読み込みとモデル指定
    api_key = os.environ.get("GEMINI_API_KEY_MY_KDP")
    if not api_key:
        raise ValueError("❌ 秘匿キー 'GEMINI_API_KEY_MY_KDP' が環境変数に見つかりません。")
        
    client = genai.Client(api_key=api_key)
    MODEL_NAME = "gemini-2.5-flash"
    print(f"🤖 使用モデル: {MODEL_NAME}")

    # 2. 設定ファイルの読み込みと検証
    if os.path.exists("config.yml"):
        with open("config.yml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    else:
        config = {"book_specs": {"page_count": 50}, "project": {"name": "01_tranquil_flora"}}

    project_slug = config.get("project", {}).get("name", "01_tranquil_flora")
    project_root = f"projects/{project_slug}"
    workspace_dir = os.path.join(project_root, "kdp_workspace")
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs("output", exist_ok=True)

    active_info = {
        "project_root": project_root,
        "title": "Tranquil Flora: A Japanese Minimalist Botanical Coloring Book for Adults"
    }
    with open("active_project.json", "w", encoding="utf-8") as f:
        json.dump(active_info, f, ensure_ascii=False, indent=2)

    print(f"📂 アクティブプロジェクト: {active_info['title']}")

    # 3. 本文（インテリア）PDFの自動ビルド執行
    print("\n--- [Step 1] 本文PDFビルド ---")
    interior_pdf = generate_interior_pdf()

    # 4. 表紙カバーPDFの自動ビルド執行（見開き対応）
    print("\n--- [Step 2] 表紙カバー見開きPDFビルド ---")
    cover_pdf = generate_cover_pdf()

    print(f"\n✨ すべての自動処理（PDF生成・見開き表紙ビルド）が正常に完了しました。")
    print(f"📦 成果物格納先: output/Interior.pdf および output/Cover.pdf")

if __name__ == "__main__":
    main()
