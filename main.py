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
    backstory="あなたは世界のEC・出版の『規約・著作権』の神様です。特にAmazon KDPで実際に売れているジャンル（道徳絵本、知育ワークブック、大人向け塗り絵など）の市場動向を熟知しており、一発で審査を通過する完全オリジナルの企画を立てます。ジャンルごとの実務構造（塗り絵の裏抜け対策、裁ち落としを含む正確なページサイズなど）にも精通しています。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

prompt_engineer = Agent(
    role="著作権クリーン・AIプロンプトデザイナー",
    goal="画像生成AIで、既存の著作権に1ミリも抵触しない、完全オリジナルで最高品質のデザインを出すプロンプトを作る",
    backstory="あなたは知的財産権に配慮したプロンプト設計のプロです。他者の権利を侵害するキーワードを一切排除し、絵本の温かみのあるイラスト、知育本の分かりやすい線、塗り絵の極細線など、ジャンルに合わせた最適な呪文（プロンプト）を設計します。印刷時の裁ち落としサイズや300DPI指定を厳格に呪文に組み込みます。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

marketer = Agent(
    role="リーガル＆SEOマーケティングディレクター",
    goal="Amazon KDPのメタデータガイドラインやEtsyのポリシーに準拠した、安全で爆売れする英語素材を作成する",
    backstory="AmazonやEtsyからペナルティを受けない、規約完全準拠のホワイトハットSEOの専門家です。購入者に商品の仕様（知育の対象年齢、片面印刷仕様、印刷の美しさなど）を正確に伝える魅力的な英語文章を書きます。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

# --- 📅 日替わり業務（偶数日＝KDP、奇数日＝Etsy）の分岐 ---
if day_num % 2 == 0:
    print(f"📅 本日は【偶数日（{current_date}）】のため、Amazon KDP出版部門（マルチジャンル・実務サイズ完全対応版）が稼働します。")
    department = "kdp"
    output_filepath = f"outputs/kdp/{current_date}_kdp_production.md"
    
    task1 = Task(
        description=(
            "Amazon KDPで現在売れ筋となっている以下の【3つのジャンル】の中から、本日出版するテーマを1つ自律的に選定し、新刊1冊分の構成案を企画してください。\n\n"
            "【対象とする3大ジャンル】\n"
            "1. 『日本の道徳教育の概念（思いやり、礼儀、自然への感謝など）』を取り入れた、海外向け児童絵本\n"
            "2. 『幼児向けはさみ練習帳・知育ワークブック』\n"
            "3. 『大人のためのミニマルな和モダン・植物塗り絵シリーズ』\n\n"
            "【選定したジャンルごとの必須実務ルール】\n"
            "- 共通サイズ仕様：印刷時のズレ・切れを防ぐため、すべてのページは『8.625 x 11.25 インチ（裁ち落とし/Bleed対応サイズ）』を想定して企画すること。\n"
            "- 絵本の場合：全15〜20ページの「英語ストーリーの文章」と「挿絵の指示」を作ること。前後にIntroductionとConclusionを含めること。\n"
            "- はさみ練習帳の場合：直線➔波線➔図形➔切り抜きと段階的に難しくなる全20〜25ワークの構成にし、裏面は白紙の片面仕様（総ページ数40〜50P）とすること。\n"
            "- 塗り絵の場合：20作品を厳選し、色移り防止のため裏面は白紙か1〜2行の説明のみにする片面仕様（計40ページ）とし、はじめに・あとがきを含めた総ページ数を算出すること。\n\n"
            "Amazonの著作権審査を一発で通すため、他者の権利を絶対に侵害しない完全オリジナルのコンセプトにしてください。"
        ),
        expected_output="選定したジャンル、本の総ページ数、実務ルール（8.625x11.25インチ前提）に準拠した詳細な全ページ構成案",
        agent=planner,
    )
    task2 = Task(
        description=(
            "プランナーが選定したジャンルの構成案を元に、画像生成AIに入力する【完全著作権クリーンな英語プロンプト】を作成してください。\n"
            "すべてのページのプロンプト末尾に、印刷ずれを防ぐための指定として必ず【 8.625 x 11.25 inch vertical layout with bleed, 300 DPI print-ready resolution 】を記述してください。\n"
            "既存のキャラクターや特定の作家を連想させるワードを完全に排除し、各ジャンルの最適なタッチ（絵本＝温かい、はさみ＝太線、塗り絵＝極細線と65%以上の余白）を徹底してください。\n"
            "すべてのページ用プロンプトに加え、本の【表紙用デザインのプロンプト】も1つ別途作成してください。"
        ),
        expected_output="中身のページ用プロンプト一式（サイズ指定入り） ＋ 表紙用プロンプト1個の一覧（英語）",
        agent=prompt_engineer,
    )
    task3 = Task(
        description=(
            "米国Amazon KDP登録用の安全かつ魅力的な素材を英語で作ってください。\n"
            "1. タイトル＆サブタイトル（商標権に抵触しない安全なもの）\n"
            "2. Amazonガイドラインに沿った検索キーワード用タグ7つ\n"
            "3. 商品説明文（英語）。本のジャンルに合わせて購入者にアピールする文章にし、総ページ数や仕様（片面印刷であること、高品質な印刷サイズであることなど）を明記してください。\n"
            "最後に、KDPの『表紙計算ツール・テンプレート』を使う際のアドバイス（総ページ数から背幅を計算するリマインド）を添えて、すべての成果物をMarkdownでまとめてください。"
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

print(f"🤖 [総括AI] 業務完了！『{output_filepath}』に完全な成果物を保存しました。")
