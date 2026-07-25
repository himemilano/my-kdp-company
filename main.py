import os
import json
import sys
from scripts.knowledge_loader import load_organization_knowledge
from scripts.agent_asset import generate_all_assets
from scripts.generate_interior import generate_interior_pdf
from scripts.agent_qa import run_qa_agent

def load_active_project():
    if not os.path.exists("active_project.json"):
        return "01_tranquil_flora"
    with open("active_project.json", "r", encoding="utf-8") as f:
        return json.load(f).get("active_project", "01_tranquil_flora")

def main():
    project_slug = load_active_project()
    print(f"🚀 KDP最高品質自律生成パイプライン起動 [プロジェクト: {project_slug}]")
    
    # Knowledgeのロード
    knowledge = load_organization_knowledge()
    print("🧠 組織のKnowledgeおよび美的基準のロード完了。")

    try:
        # [1] アセット生成（自己批判付き）
        generate_all_assets(project_slug)
        
        # [2] DTPインナーPDF構築（前付け、章扉、全プレート、裏面ブランクの完全構造化）
        generate_interior_pdf(project_slug)
        
        # [3] 最終品質検証（QA Gatekeeper）
        run_qa_agent(project_slug)
        
        print("✅ 全ての工程が妥協なく完了しました。北米Amazon KDP向け出版データが完成しています。")

    except Exception as e:
        print(f"❌ 【パイプライン緊急停止】品質基準未達またはエラーを検知しました: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
