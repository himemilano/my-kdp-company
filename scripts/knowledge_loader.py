import os
import glob

def load_organization_knowledge():
    """
    knowledge/ ディレクトリから過去の教訓や美的基準を動的に読み込み、
    エージェントのコンテキスト（制約条件・品質基準）として統合する。
    """
    knowledge_data = {
        "lessons_learned": "",
        "design_principles": (
            "侘び寂び、幽玄、65%以上のネガティブスペース（余白）、"
            "極細の線画（Ultra-fine line art）、ボタニカルの正確性、"
            "幾何学的なダミー図形やテスト用の円・格子の厳禁"
        )
    }
    
    # 過去の教訓ログの読み込み
    lessons_path = "knowledge/lessons_learned.md"
    if os.path.exists(lessons_path):
        with open(lessons_path, "r", encoding="utf-8") as f:
            knowledge_data["lessons_learned"] = f.read()
            
    # knowledgeディレクトリ内の他のMarkdownも動的スキャン
    other_knowledge = []
    for md_file in glob.glob("knowledge/**/*.md", recursive=True):
        if os.path.normpath(md_file) != os.path.normpath(lessons_path):
            if os.path.exists(md_file):
                with open(md_file, "r", encoding="utf-8") as f:
                    other_knowledge.append(f.read())
                
    knowledge_data["additional_notes"] = "\n".join(other_knowledge)
    return knowledge_data
