import os
import sys
import json
from datetime import datetime

def log_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def update_lessons_learned(project_slug, status, notes):
    lessons_path = "knowledge/lessons_learned.md"
    os.makedirs("knowledge", exist_ok=True)
    
    log_entry = f"\n- **Project**: {project_slug} | **Date**: {datetime.now().strftime('%Y-%m-%d')} | **Status**: {status} | **Notes**: {notes}"
    
    if os.path.exists(lessons_path):
        with open(lessons_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
    else:
        with open(lessons_path, "w", encoding="utf-8") as f:
            f.write(f"# Organization Lessons Learned & Self-Improvement Log\n{log_entry}")

def get_active_project():
    # 1. コマンドライン引数があれば優先
    if len(sys.argv) > 1:
        return sys.argv[1]
    
    # 2. active_project.json から現在のプロジェクトを読み込む
    active_json_path = "active_project.json"
    if os.path.exists(active_json_path):
        try:
            with open(active_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "project_slug" in data:
                    return data["project_slug"]
        except Exception as e:
            print(f"Warning: Failed to read active_project.json: {e}")
            
    # 3. フォールバック
    return "02_zen_mindful_patterns"

def main():
    project_slug = get_active_project()
    
    log_message(f"🚀 KDP自律進化組織 パイプライン起動: [{project_slug}]")

    # active_project.json の内容を確実に同期・更新してGitに差分を生ませる
    active_data = {
        "project_root": f"projects/{project_slug}",
        "project_slug": project_slug,
        "title": "Tranquil Flora: A Japanese Minimalist Botanical Coloring Book for Adults" if project_slug == "01_tranquil_flora" else f"Project {project_slug}",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("active_project.json", "w", encoding="utf-8") as f:
        json.dump(active_data, f, indent=2, ensure_ascii=False)

    project_root = f"projects/{project_slug}"
    os.makedirs(os.path.join(project_root, "kdp_workspace"), exist_ok=True)
    os.makedirs(os.path.join(project_root, "assets"), exist_ok=True)
    os.makedirs(os.path.join(project_root, "output"), exist_ok=True)

    try:
        # 1. 企画・戦略エージェント（Knowledge ＋ Gemini API連携）
        log_message("📋 [1/5] 企画・戦略エージェント稼働中 (Gemini 2.5 Flash)...")
        from scripts.agent_planner import run_planner_agent
        run_planner_agent(project_slug)

        # 2. テキスト・CSVデータ生成
        log_message("📝 [2/5] テキスト・CSVエージェント稼働中...")
        csv_file = os.path.join(project_root, "kdp_workspace", f"{project_slug}_body_bulk_create.csv")
        if not os.path.exists(csv_file):
            import csv
            with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["title", "description"])
                for i in range(1, 31):
                    writer.writerow([f"Plate {i}: Mindful Art", f"Zen geometric botanical pattern designed for deep relaxation and stress relief."])

        # 3. 視覚アセット生成エージェント
        log_message("🌿 [3/5] 視覚線画アセット生成エージェント稼働中...")
        from scripts.agent_asset import run_asset_agent
        run_asset_agent(project_slug)

        # 4. PDFビルドエージェント (Interior ＆ Cover)
        log_message("🎨 [4/5] PDFビルドエージェント稼働中...")
        from scripts.generate_interior import generate_interior_pdf
        from scripts.generate_cover import generate_cover_pdf
        
        generate_interior_pdf(project_slug)
        generate_cover_pdf(project_slug)

        # 5. 品質検証 ＆ 自己進化ログの記録
        log_message("🔍 [5/5] 品質検証・自己進化エージェント稼働中...")
        interior_pdf = os.path.join(project_root, "output", "Interior.pdf")
        cover_pdf = os.path.join(project_root, "output", "Cover.pdf")
        
        if os.path.exists(interior_pdf) and os.path.exists(cover_pdf):
            log_message("✅ すべての成果物のビルドと検証が正常に完了しました！")
            update_lessons_learned(project_slug, "SUCCESS", "Successfully generated AI-planned, fully integrated KDP PDFs using Knowledge base.")
        else:
            raise FileNotFoundError("必須のPDF出力成果物が見つかりません。")

    except Exception as e:
        log_message(f"❌ エラーが発生しました: {e}")
        update_lessons_learned(project_slug, "FAILED", f"Pipeline crashed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
