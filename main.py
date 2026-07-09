import os
from datetime import datetime, timedelta, timezone
from crewai import Agent, Crew, Process, Task

# --- ⚙️ 日付とフォルダの自動設定 ---
import datetime as dt
jst = timezone(timedelta(hours=9))
now = datetime.now(jst)
current_date = now.strftime("%Y-%m-%d")
day_num = now.day

os.makedirs("outputs/kdp", exist_ok=True)
os.makedirs("outputs/etsy", exist_ok=True)

# --- 👔 AI社員（エージェント）の定義 ---
planner = Agent(
    role="総合EC・出版最高プランナー",
    goal="Amazon KDPの厳しい審査やEtsy規約を完全クリアする、実務的で安全なデジタルコンテンツ・物販の企画を作る",
    backstory="あなたは世界のEC・出版の『規約・著作権』の神様です。特にAmazon KDPの著作権審査の厳しさ（AI生成物のガイドライン、類似性の問題）を熟知しており、一発で審査を通過する完全オリジナルの企画を立てます。また、塗り絵の裏抜け・色移り対策（片面印刷仕様）などの実務構造にも精通しています。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

prompt_engineer = Agent(
    role="著作権クリーン・AIプロンプトデザイナー",
    goal="画像生成AIで、既存の著作権に1ミリも抵触しない、完全オリジナルで最高品質のデザインを出すプロンプトを作る",
    backstory="あなたは知的財産権に配慮したプロンプト設計のプロです。他者の権利を侵害するキーワードを一切排除し、完全にクリーンでありながら、大人が満足する極細線・美しい余白・植物学的正確さ、あるいはEtsyで売れる和モダン風景を1枚の絵に落とし込む呪文を開発します。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

marketer = Agent(
    role="リーガル＆SEOマーケティングディレクター",
    goal="Amazon KDPのメタデータガイドラインやEtsyのポリシーに準拠した、安全で爆売れする英語素材を作成する",
    backstory="AmazonやEtsyから『キーワードの詰め込み』や『誤解を招く表現』としてペナルティを受けない、規約完全準拠のホワイトハットSEOの専門家です。購入者に商品の仕様（片面印刷仕様であることなど）を正確に伝える魅力的な英語文章を書きます。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

# --- 📅 日替わり業務（偶数日＝KDP、奇数日＝Etsy）の分岐 ---
if day_num % 2 == 0:
    print(f"📅 本日は【偶数日（{current_date}）】のため、Amazon KDP出版部門（厳格審査対策版）が稼働します。")
    department = "kdp"
    output_filepath = f"outputs/kdp/{current_date}_kdp_botanical_coloring.md"
    
    task1 = Task(
        description=(
            "大人のためのミニマルな植物塗り絵シリーズの新刊（1冊分）の構成案を企画してください。\n"
            "【必須の実務構造】:\n"
            "1. 20作品の日本の伝統植物を厳選してください。\n"
            "2. 色移り・裏抜け防止のため、見開きの片側は『白紙』または『その植物に関する1〜2行の英語説明文・詩』のみを配置する裏面仕様とし、塗り絵パートを計40ページにしてください。\n"
            "3. 本の全体構成として、『はじめに（Introduction）』『あとがき（Conclusion）』のページを必ず追加し、総ページ数を明確に算出してください（後で表紙計算ツールに入力するため）。\n"
            "4. Amazonの著作権審査を一発で通すため、他者の権利を侵害しない完全オリジナルの和風コンセプトにしてください。"
        ),
        expected_output="本の総ページ数、構成（はじめに、20作品×裏面説明の40ページ、あとがき）、各植物のテーマ一覧",
        agent=planner,
    )
    task2 = Task(
        description=(
            "プランナーの構成案（20作品分）を元に、画像生成AIに入力する【完全著作権クリーンな英語プロンプト】を20個作成してください。\n"
            "既存のキャラクターや特定の作家を連想させるワードを完全に排除し、単なる植物画を超えた『fine line art, extensive negative space, botanical accuracy, ukiyo-e style, clean white background, 100% original illustration』などの品質・安全指定を徹底してください。\n"
            "また、本の【表紙用デザインのプロンプト】も1つ、背幅やカットラインを意識しやすい構図（中央配置など）で別途作成してください。"
        ),
        expected_output="中身のページ用プロンプト20個 ＋ 表紙用プロンプト1個の一覧（英語）",
        agent=prompt_engineer,
    )
    task3 = Task(
        description=(
            "米国Amazon KDP登録用の安全かつ魅力的な素材を英語で作ってください。\n"
            "1. タイトル＆サブタイトル（商標権に抵触しない安全なもの）\n"
            "2. Amazonガイドラインに沿った検索キーワード用タグ7つ\n"
            "3. 商品説明文（英語）。海外の購入者に『片面印刷（Left-side blank page）なので色移りせず、お気に入りの色鉛筆やマーカーで楽しめます』という実務的な仕様と、総ページ数を明記した文章にしてください。\n"
            "最後に、KDPの『表紙計算ツール・テンプレート』を使う際のアドバイスを添えて、すべての成果物をMarkdownでまとめてください。"
        ),
        expected_output="規約に準拠したKDP登録用テキストと、表紙作成アドバイスを含む全体のMarkdown",
        agent=marketer,
    )

else:
    print(f"📅 本日は【奇数日（{current_date}）】のため、Etsy×Printify物販部門（規約準拠版）が稼働します。")
    department = "etsy"
    output_filepath = f"outputs/etsy/{current_date}_etsy_printify_goods.md"
    
    task1 = Task(
        description=(
            "Etsyの『ハンドメイド・オリジナルデザイン』の規約を厳格に遵守した、Printify向けの和モダン・日本風景グッズ（Tシャツ、マグカップ、キャンバス等）のデザインコンセプトを3〜5つ企画してください。\n"
            "他者の商標やブランド、既存の浮世絵の単純コピーではなく、あなた自身のオリジナルデザインとして出品できるクリーンなテーマに限定してください。"
        ),
        expected_output="Etsy規約に完全準拠したグッズのコンセプト、対象商品、ターゲット層の提案",
        agent=planner,
    )
    task2 = Task(
        description=(
            "プランナーの企画を元に、Printifyの印刷テンプレート（300DPI、透過背景など）に最適で、Etsyのポリシーに違反しない【英語プロンプト】を作成してください。\n"
            "商標やブランド名を避け、印刷時にボヤけない鮮明なグラフィック（vector style, high resolution, 300dpi, clean background）を指定してください。"
        ),
        expected_output="グッズデザイン用の安全で高品質な英語プロンプト一覧",
        agent=prompt_engineer,
    )
    task3 = Task(
        description=(
            "Etsyに出品するためのマーケティング素材を英語で作成してください。\n"
            "1. 規約に沿った商品タイトル（キーワードの過剰な詰め込みを避ける）\n"
            "2. 検索用13個のタグキーワード\n"
            "3. 商品説明文（英語）。Printifyを通したオンデマンド製造である旨や、配送に関する注意、商品の仕様を丁寧に伝える文章にしてください。\n"
            "最後にすべての成果物を1つのレポートにまとめてください。"
        ),
        expected_output="Etsy出品用テキストを含んだ全体のMarkdown",
        agent=marketer,
    )

# --- 🚀 実行セクション ---
publishing_company = Crew(
    agents=[planner, prompt_engineer, marketer],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    verbose=True,
    max_rpm=15,
)

print(f"🤖 [総括AI] {department.upper()}部門の業務を開始します...")
result = publishing_company.kickoff()

with open(output_filepath, "w", encoding="utf-8") as f:
    f.write(str(result))

print(f"🤖 [総括AI] 業務完了！『{output_filepath}』に安全な成果物を保存しました。")
