import sys
import os

# scriptsディレクトリを確実にパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.knowledge_loader import load_organization_knowledge
from scripts.agent_asset import generate_all_assets
from scripts.generate_interior import generate_interior_pdf
from scripts.agent_qa import run_qa_agent

def main():
    project_slug = "01_tranquil_flora"
    print(f"🚀 KDP最高品質自律生成パイプライン起動 [プロジェクト: {project_slug}]")
    
    try:
        # 1. 組織のKnowledgeおよび美的基準のロード
        knowledge = load_organization_knowledge()
        print("🧠 組織のKnowledgeおよび美的基準のロード完了。")

        # 2. アセットエージェントによる線画生成
        generate_all_assets(project_slug)

        # 3. DTPエンジンによる全60ページインナー構築
        generate_interior_pdf(project_slug)

        # 4. QAゲートキーパーによる厳格検証
        run_qa_agent(project_slug)

        print("✨ すべてのプロセスが正常に完了しました。KDP出版データの生成に成功しました。")

    except Exception as e:
        print(f"\n❌ 【パイプライン緊急停止】品質基準未達またはエラーを検知しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
