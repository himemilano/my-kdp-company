import os
import json
import yaml
from google import genai
from scripts.generate_cover import generate_cover_pdf
from scripts.generate_interior import generate_interior_pdf

def main():
    print("🚀 [KDP出版部] 自律オーケストレーター起動中（完全統合版）...")

    # 1. ユーザー様指定のAPIキー名から読み込み、gemini-2.5-flashを指定
    api_key = os.environ.get("GEMINI_API_KEY_MY_KDP")
    if not api_key:
        raise ValueError("❌ 秘匿キー 'GEMINI_API_KEY_MY_KDP' が環境変数に見つかりません。")
        
    client = genai.Client(api_key=api_key)
    MODEL_NAME = "gemini-2.5-flash"
    print(f"🤖 使用モデル: {MODEL_NAME}")

    # 2. 設定ファイルの読み込み
    if os.path.exists("config.yml"):
        with open("config.yml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    else:
        config = {"book_specs": {"page_count": 50}, "project": {"name": "01_tranquil_flora"}}

    project_slug = config.get("project", {}).get("name", "01_tranquil_flora")
    project_root = f"projects/{project_slug}"
    workspace_dir = os.path.join(project_root, "kdp_workspace")
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # active_project.json の書き出し
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

    # 4. 表紙カバーPDFの自動ビルド執行
    print("\n--- [Step 2] 表紙カバーPDFビルド ---")
    cover_pdf = generate_cover_pdf()

    # 5. Canva用CSVおよびマニフェストの生成
    manifest_csv = os.path.join(workspace_dir, "canva_prompts_manifest.csv")
    with open(manifest_csv, "w", encoding="utf-8") as f:
        f.write("Page,Prompt,Layout_Type\n")
        f.write("1,Japanese minimalist cherry blossom branch in ukiyo-e style line art,Recto_Illustration\n")
        f.write("2,Notes and color testing palette space,Verso_Notes\n")

    print(f"✅ Canva用CSVを生成しました: {manifest_csv}")
    print(f"✨ すべての自動処理（PDF生成含む）が正常に完了しました。")
    print(f"📦 成果物格納先: output/Interior.pdf および output/Cover.pdf")

if __name__ == "__main__":
    main()
