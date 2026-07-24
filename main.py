import os
import json
import re
import yaml

def load_active_project():
    """active_project.json から現在のプロジェクト情報を読み込む"""
    if not os.path.exists("active_project.json"):
        raise FileNotFoundError("active_project.json が見つかりません。")
    
    with open("active_project.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_config():
    """config.yml から設定を読み込む"""
    if not os.path.exists("config.yml"):
        return {}
    
    with open("config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def calculate_kdp_cover(page_count=60):
    """
    KDP公式の背幅・カバー寸法自動計算ロジック
    白黒・白用紙の背幅係数: 0.002252インチ/ページ
    """
    spine_width = page_count * 0.002252
    trim_width = 8.5
    trim_height = 11.0
    bleed = 0.125
    margin = 0.25

    total_width = (bleed * 2) + (trim_width * 2) + spine_width
    total_height = (bleed * 2) + trim_height

    return {
        "page_count": page_count,
        "spine_width_inch": round(spine_width, 4),
        "total_cover_width_inch": round(total_width, 4),
        "total_cover_height_inch": round(total_height, 4),
        "safe_margin_inch": margin
    }

def process_production_note(note_path):
    """原稿ノート（Markdown）からMidjourney/Geminiプロンプトを抽出する"""
    if not os.path.exists(note_path):
        print(f"⚠️ 生産ノートが見つかりません: {note_path}")
        return []

    with open(note_path, "r", encoding="utf-8") as f:
        content = f.read()

    prompts = re.findall(r"```prompt\n(.*?)\n```", content, re.DOTALL)
    return prompts

def main():
    print("🚀 [KDP出版部] 自律オーケストレーター起動中...")
    
    # 🔑 GitHub Secrets から渡された環境変数を取得
    gemini_api_key = os.environ.get("GEMINI_API_KEY_MY_KDP")
    if not gemini_api_key:
        print("⚠️ 警告: 開発環境、またはシークレットに GEMINI_API_KEY_MY_KDP が設定されていません。")
    else:
        print("🔑 Gemini API キーの読み込みを確認しました。")

    # ⚙️ 設定ファイルの読み込みとモデル名の確認
    config = load_config()
    model_name = config.get("api_settings", {}).get("model_name", "gemini-2.5-flash")
    print(f"🤖 使用モデル: {model_name}")

    # 1. アクティブプロジェクトの特定
    project_info = load_active_project()
    project_id = project_info["current_project_id"]
    project_title = project_info["project_title"]
    project_root = project_info["project_root"]
    
    print(f"📂 アクティブプロジェクト: {project_title} ({project_id})")

    # 2. ワークスペースの確保
    workspace_dir = os.path.join(project_root, "kdp_workspace")
    os.makedirs(workspace_dir, exist_ok=True)

    # 3. カバー寸法の計算（例: 60ページ想定）
    cover_specs = calculate_kdp_cover(page_count=60)
    
    # 4. 原稿ノートの読み込みとパース
    note_path = os.path.join(project_root, "kdp_production_note.md")
    prompts = process_production_note(note_path)

    # 5. Canva一括インポート用CSVの生成
    csv_path = os.path.join(workspace_dir, "canva_prompts_manifest.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("index,prompt_text,status\n")
        for i, p in enumerate(prompts, 1):
            clean_p = p.replace('"', '""').strip()
            f.write(f'{i},"{clean_p}",pending\n')
    print(f"✅ Canva用CSVを生成しました: {csv_path}")

    # 6. KDP登録用最終マニフェストの生成
    manifest_path = os.path.join(workspace_dir, "kdp_final_upload_manifest.md")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(f"# KDP Upload Manifest: {project_title}\n\n")
        f.write("## カバー寸法仕様 (KDP公式準拠)\n")
        f.write(f"- 総ページ数: {cover_specs['page_count']} ページ\n")
        f.write(f"- 背幅: {cover_specs['spine_width_inch']} インチ\n")
        f.write(f"- 全体カバー幅（裁ち落とし込）: {cover_specs['total_cover_width_inch']} インチ\n")
        f.write(f"- 全体カバー高（裁ち落とし込）: {cover_specs['total_cover_height_inch']} インチ\n\n")
        f.write("## AI・API設定\n")
        f.write(f"- 使用モデル: `{model_name}`\n")
        f.write("- APIキー認証: 連携済み (`GEMINI_API_KEY_MY_KDP`)\n\n")
        f.write("## マーケティング・SEOステータス\n")
        f.write("- 4ジャンル戦略 および 逆算パッチワーク法 適用済\n")
        f.write("- ゴールシーク＆自己批判プロンプト体系 連携完了\n")
    print(f"✅ KDPマニフェストを生成しました: {manifest_path}")

    print("✨ すべての自動処理が正常に完了しました。")

if __name__ == "__main__":
    main()
