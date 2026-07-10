import os
import json
from datetime import datetime, timedelta, timezone
from crewai import Agent, Crew, Process, Task

# --- ⚙️ タイムゾーンと日付の設定 ---
jst = timezone(timedelta(hours=9))
now = datetime.now(jst)
current_date = now.strftime("%Y-%m-%d")

# フォルダの作成
os.makedirs("outputs/projects", exist_ok=True)
STATE_FILE = "outputs/projects/project_state.json"

# --- 📖 プロジェクト管理帳（引き継ぎ帳）の読み込み・初期化 ---
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "current_project_id": None,
        "platform": None, # "KDP" or "Etsy"
        "title": "未定",
        "status": "START_NEW_PROJECT", # 進行ステータス
        "current_page": 0,
        "target_pages": 40,
        "history": []
    }

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=4)

state = load_state()

# --- 👔 自律型AI組織の社員（エージェント）定義 ---

coo_pm = Agent(
    role="最高執行責任者 (COO) 兼 プロジェクトマネージャー",
    goal="1つのデジタルコンテンツ（KDP/Etsy）を企画から完成・出版まで数日かけてでも1ミリの妥協なく完遂する",
    backstory=(
        "ナラティブ、スケジュール、品質を統括する冷徹かつ情熱的なリーダー。"
        "現在のプロジェクト進捗状況（ステート）を厳格に分析し、本日チームが集中すべき『最も重要な実務』を定義します。"
        "前回の成果をレビューし、出版ガイドラインをクリアするまで次のプロジェクトへの移行を絶対に許可しません。"
    ),
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

creator = Agent(
    role="制作ディレクター 兼 AIプロンプトデザイナー",
    goal="プロジェクトのテーマに沿った、完全オリジナルで著作権クリーンな高品質コンテンツ（線画・文章）を制作する",
    backstory=(
        "伝統的な和モダン、知育、絵本など、あらゆるジャンルの構造（サイズ、余白、解像度）を熟知したクリエイター。"
        "KDPなら【8.625 x 11.25 inch with bleed, 300 DPI】等の実務規格をプロンプトに完璧に落とし込み、日々ページを積み上げます。"
    ),
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

marketer_qa = Agent(
    role="マーケティング 兼 品質保証（QA）ディレクター",
    goal="成果物のリーガルチェック、KDP/EtsyのSEOメタデータ作成、およびプロジェクト完了時の組織改善案を練る",
    backstory=(
        "AmazonやEtsyの規約、商標権、ホワイトハットSEOの権威。成果物の品質を厳しくチェックします。"
        "プロジェクト完了時には、組織のパフォーマンスを振り返り、『次回よりステップアップするために、どんな新社員（専門エージェント）を雇うべきか』を自律的に考案します。"
    ),
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

# --- 🧭 プロジェクトの状態に応じたタスクの動的生成 ---

tasks = []

if state["status"] == "START_NEW_PROJECT":
    # 🚀 フェーズ1：新しいプロジェクトの立ち上げ
    print("🆕 [組織の判断] 現在進行中のプロジェクトがありません。新しいプロジェクトを企画・選定します。")
    
    task1 = Task(
        description=(
            "Amazonで現在実際に売れているトレンド（日本の道徳教育の概念を取り入れた海外向け絵本、幼児用はさみ練習帳、大人のミニマル植物塗り絵など）"
            "またはEtsyで爆売れしている和モダン物販から、今回【数日間かけて総力を挙げて完成させる1つの大物プロジェクト】を自律的に厳選し、仕様（総ページ数、ターゲット、プラットフォーム）を決定してください。"
        ),
        expected_output="選定したプロジェクトの完全な企画書、ターゲット層、および完成までのマイルストーン計画",
        agent=coo_pm,
    )
    task2 = Task(
        description="決定したプロジェクトの核となる、表紙（またはメインデザイン）の完全著作権クリーンな画像生成プロンプトと、本の基本構成案を作成してください。KDPの場合は【8.625 x 11.25 inch vertical layout with bleed, 300 DPI print-ready resolution】を厳守すること。",
        expected_output="表紙用プロンプトと、全体の章立て・構成案テキスト",
        agent=creator,
    )
    task3 = Task(
        description="この新プロジェクトの市場優位性を検証し、SEOに強いタイトル候補、初期のキーワードタグを考案してください。",
        expected_output="プロジェクト立ち上げ用マーケティングレポート",
        agent=marketer_qa,
    )
    tasks = [task1, task2, task3]
    
    # 状態の更新予測（実行後に手動またはプログラムでフェーズを進める）
    state["status"] = "IN_PROGRESS"
    state["title"] = f"Project_{current_date}"
    state["current_page"] = 1
    state["target_pages"] = 40 # 企画に合わせて自動変動

elif state["status"] == "IN_PROGRESS":
    # ⚙️ フェーズ2：プロジェクトの継続・ページの量産
    p_title = state["title"]
    curr = state["current_page"]
    target = state["target_pages"]
    print(f"⏳ [組織の判断] プロジェクト『{p_title}』を継続中。現在 {curr} / {target} ページ目を制作します。完遂するまで次には行きません。")
    
    task1 = Task(
        description=f"現在進行中のプロジェクト『{p_title}』の進捗（{curr}/{target}ページ目）を確認し、本日制作すべき具体的なページ内容（例：植物塗り絵なら特定の和の植物3種、はさみ練習帳なら難易度ステップに沿った図形）の指示書を出してください。",
        expected_output="本日の制作ターゲットに関する具体的な演出・構造の指示",
        agent=coo_pm,
    )
    task2 = Task(
        description="PMの指示に基づき、本日分の画像生成用英語プロンプト（サイズ・裁ち落とし・300DPIの呪文入り）を完全に著作権クリーンな形で作成してください。",
        expected_output="本日進めるページ分（3〜5ページ分）の完全な英語プロンプト一覧",
        agent=creator,
    )
    task3 = Task(
        description="本日制作したプロンプトのクオリティをチェックし、Amazon/Etsyの規約違反（他者の商標侵害など）がないか厳格に検閲してください。",
        expected_output="リーガル＆クオリティ通過の承認ログ",
        agent=marketer_qa,
    )
    tasks = [task1, task2, task3]
    
    # ページを進める
    state["current_page"] += 3
    if state["current_page"] >= state["target_pages"]:
        state["status"] = "FINAL_REVIEW"

elif state["status"] == "FINAL_REVIEW":
    # 🏁 フェーズ3：最終チェック ＆ メタデータ完全作成 ＆ 自律組織改善会
    p_title = state["title"]
    print(f"🎉 [組織の判断] 『{p_title}』の全素材が揃いました！最終出版メンテ、および組織の『自律改善・新社員スカウト会議』を行います。")
    
    task1 = Task(
        description=f"プロジェクト『{p_title}』の全成果物（中身・表紙プロンプトなど）を総括し、Amazon KDP（またはEtsy）に今すぐ登録できる最終出版パッケージとして構成を固定してください。",
        expected_output="出版直前状態の、非の打ち所がない完全な1冊の構成台帳",
        agent=coo_pm,
    )
    task2 = Task(
        description="この作品が海外で爆売れするための、Amazonガイドライン完全準拠の説明文（英語）、隠れた検索キーワード7つ、表紙計算ツール用のアドバイスを完成させてください。",
        expected_output="完全なKDP/Etsy登録用SEOテキスト",
        agent=creator,
    )
    task3 = Task(
        description=(
            "【最重要・自律進化タスク】今回のプロジェクト全体の組織パフォーマンス（進行速度、クオリティのブレ、規約上の課題など）を徹底的に振り返り、"
            "『次回プロジェクトからさらにステップアップするために、チームに新しく雇用すべき【新社員（専門AIエージェント）】の役割』を自律的に定義してください。"
            "（例：英文校正専門のネイティブエージェント、余白の比率を厳密にチェックするレイアウト監査AI、など）"
        ),
        expected_output="次回に向けた組織改善提案書（新社員の採用・役割定義を含むKAIZENノート）",
        agent=marketer_qa,
    )
    tasks = [task1, task2, task3]
    
    # プロジェクト完了、次回は新しいプロジェクトへ
    state["status"] = "START_NEW_PROJECT"
    state["history"].append({"project": p_title, "completed_at": current_date})

# --- 🚀 実行セクション ---
project_crew = Crew(
    agents=[coo_pm, creator, marketer_qa],
    tasks=tasks,
    process=Process.sequential,
    verbose=True
)

print(f"🤖 [自律システム] 稼働を開始します。現在のステータス: {state['status']}")
result = project_crew.kickoff()

# 成果物の保存
project_folder = f"outputs/projects/{state['title']}"
os.makedirs(project_folder, exist_ok=True)
report_file = f"{project_folder}/{current_date}_{state['status']}_report.md"

with open(report_file, "w", encoding="utf-8") as f:
    f.write(str(result))

# 状態を保存して明日に引き継ぐ
save_state(state)
print(f"💾 [自律システム] 今日の実務が記録されました。進捗は明日のチームへ引き継がれます。成果物: {report_file}")
