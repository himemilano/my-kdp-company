import os
from crewai import Agent, Crew, Process, Task

# 1. KDP専門チーム（3人の精鋭）の採用
planner = Agent(
    role="KDPコンテンツプランナー",
    goal="Amazon KDPで世界に向けて出版する、塗り絵・ワークブック・絵本の高品質な企画と構成を作る",
    backstory="あなたはAmazon KDPのグローバルトレンドを熟知した天才プランナーです。特に日本の伝統美（植物・風景）を取り入れた大人向け塗り絵や、子供の心を育てる道徳絵本、知育系ワークブック（はさみ練習など）の企画を得意としています。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

prompt_engineer = Agent(
    role="AIプロンプトデザイナー",
    goal="企画を元に、画像生成AI（Midjourney等）で一発で売れるイラストが出せる『魔法の英語プロンプト』を構築する",
    backstory="あなたは画像生成AIのプロフェッショナルです。大人向け塗り絵に必須な『洗練された極細の線画、美しい余白（65%以上のホワイトスペース）、植物学的に正確な構造』を表現する高度な英語プロンプトや、絵本向けの温かみのあるイラスト用プロンプトを精密に設計できます。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

marketer = Agent(
    role="KDPマーケティングディレクター",
    goal="海外のAmazonで検索上位に引っかかるSEOタイトル、検索キーワード、思わず買いたくなる英語の商品説明文を作成する",
    backstory="あなたは米国Amazon KDPのSEO（検索最適化）の専門家です。海外の購入者が好むフックのある商品タイトルや、購買意欲をそそる商品説明（A+コンテンツの構成案含む）を英語で完璧にライティングします。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

# 2. 業務命令（タスク）の定義
# ★経営者（あなた）の意向に合わせて、いつでも【今回のお題】を「はさみ練習帳」や「道徳絵本」に書き換え可能です
task1 = Task(
    description=(
        "本日の出版プロジェクトを1つ企画してください。\n"
        "【今回のお題】: 日本の伝統的な美（日本画・木版画風）を取り入れた、大人のためのミニマルな植物塗り絵シリーズ（新刊ボリュームの構成）\n"
        "成果物として、本のコンセプト、ターゲット層、全体のページ構成案（各ページに配置する具体的な植物やテーマの一覧）を出力してください。"
    ),
    expected_output="本のコンセプト、ターゲット層、全ページの構成案テキスト",
    agent=planner,
)

task2 = Task(
    description=(
        "プランナーの構成案を元に、画像生成AI（Midjourneyなど）に入力する、各ページ用の【英語の画像生成プロンプト】をすべて作成してください。\n"
        "塗り絵の場合、大人が集中できる美しい極細のラインアート、少なくとも65%以上の豊富なネガティブスペース（余白）、植物学的に正確な構造を持つ、浮世絵や日本画にインスパイアされたテイストになるよう、呪文（プロンプト）の末尾に品質指定の英語（例: fine line art, extensive negative space, botanical accuracy, ukiyo-e style, clean white background）を徹底して仕込んでください。"
    ),
    expected_output="各ページごとのコピペ用英語プロンプト一覧（英語）",
    agent=prompt_engineer,
)

task3 = Task(
    description=(
        "これまでの企画とプロンプトを元に、米国Amazon KDPに出品するためのマーケティング素材を英語で作成してください。\n"
        "1. 魅力的なメインタイトル＆サブタイトル（英語）\n"
        "2. 検索キーワード用タグ（Amazon登録用の重要な7つのワード）\n"
        "3. 購入者の心を掴むHTML装飾入りの商品説明文（英語）\n"
        "最後に、これまでのすべての成果物（企画、英語プロンプト、マーケティング素材）を1つの美しいレポートにまとめて出力してください。"
    ),
    expected_output="KDP登録用のタイトル、キーワード、商品説明文、および全成果物のMarkdownテキスト",
    agent=marketer,
    output_file="kdp_production_note.md", # このファイルに一括納品されます
)

# 3. 組織の結成と実行
kdp_company = Crew(
    agents=[planner, prompt_engineer, marketer],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    verbose=True,
    max_rpm=15, # 混雑エラー（503）対策
)

print("🤖 [総括AI] KDP出版部門、本日の業務を開始します...")
result = kdp_company.kickoff()
print("🤖 [総括AI] 業務完了！『kdp_production_note.md』をオフィスに納品しました。")
