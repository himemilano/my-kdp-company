import os
from google import genai

def run_planner_agent(project_slug):
    print(f"📋 [Planner Agent] プロジェクト '{project_slug}' の企画立案を開始中...")
    
    api_key = os.environ.get("GEMINI_API_KEY_MY_KDP")
    if not api_key:
        raise ValueError("環境変数 'GEMINI_API_KEY_MY_KDP' が設定されていません。")
    
    client = genai.Client(api_key=api_key)
    
    knowledge_text = ""
    if os.path.exists("knowledge/4_genre_strategy.md"):
        with open("knowledge/4_genre_strategy.md", "r", encoding="utf-8") as f:
            knowledge_text += f.read() + "\n"
            
    lessons_text = ""
    if os.path.exists("knowledge/lessons_learned.md"):
        with open("knowledge/lessons_learned.md", "r", encoding="utf-8") as f:
            lessons_text = f.read() + "\n"

    prompt = f"""
    あなたはAmazon KDPのトッププロデューサー兼エージェントです。
    以下の組織の戦略教科書と過去の学びを完全に遵守し、新規プロジェクト '{project_slug}' のための企画書（Markdown形式）を生成してください。
    
    【組織の戦略教科書】
    {knowledge_text}
    
    【過去の学び・教訓】
    {lessons_text}
    
    出力フォーマット：
    - プロジェクトタイトル（英語）
    - 対象読者・ターゲット層
    - コンセプトの概要（US市場向け）
    - ページ構成案の概要
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
    project_root = f"projects/{project_slug}"
    workspace_dir = os.path.join(project_root, "kdp_workspace")
    os.makedirs(workspace_dir, exist_ok=True)
    
    plan_path = os.path.join(workspace_dir, "project_plan.md")
    with open(plan_path, "w", encoding="utf-8") as f:
        f.write(response.text)
        
    print(f"✅ 企画立案が完了しました: {plan_path}")
    return response.text
