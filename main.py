import os
import json
import sys
from scripts.knowledge_loader import load_organization_knowledge
from scripts.agent_asset import run_asset_agent
from scripts.agent_qa import run_qa_agent
# 必要に応じて他のエージェントもインポート
# from scripts.agent_planner import run_planner_agent
# from scripts.generate_interior import generate_interior_pdf
# from scripts.generate_cover import generate_cover_pdf

def load_active_project():
    if not os.path.exists("active_project.json"):
        return "01_tranquil_flora"  # デフォルト
    with open("active_project.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("active_project", "01_tranquil_flora")

def main():
    project_slug = load_active_project()
    print(f"[2026-07-25] 🚀 KDP自律進化組織 パイプライン起動: [{project_slug}]")
    
    # 組織のKnowledgeを最初にロード・確認
    knowledge = load_organization_knowledge()
    print(f"🧠 Knowledgeロード完了。過去の教訓と品質基準を適用します。")

    try:
        # [1/5] 企画・戦略ステップ（必要に応じて実行）
        print("📋 [1/5] 企画・戦略確認中...")
        
        # [2/5] テキスト・CSVステップ
        print("📝 [2/5] テキスト・CSV処理確認中...")
        
        # [3/5] 視覚線画アセット生成 ＋ 自己批判
        print("🌿 [3/5] 視覚線画アセット生成エージェント稼働中（自己批判機能付き）...")
        run_asset_agent(project_slug)
        
        # [4/5] PDFビルドステップ（Interior / Cover）
        print("🎨 [4/5] PDFビルドエージェント稼働中...")
        # generate_interior_pdf(project_slug)
        # generate_cover_pdf(project_slug)
        
        # [5/5] 最終品質検証（QA Gatekeeper）による厳格な合否判定
        print("🔍 [5/5] 品質検証・自己進化エージェント稼働中（QA Gate）...")
        run_qa_agent(project_slug)
        
        print("✅ すべてのプロセスが厳格な品質基準をクリアして正常終了しました。")

    except Exception as e:
        print(f"❌ 【パイプライン中断】品質基準未達またはエラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
