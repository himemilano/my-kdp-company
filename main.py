import os
import json
import datetime from datetime, timedelta, timezone
from crewai import Agent, Crew, Process, Task
from langchain_google_genai import ChatGoogleGenerativeAI  # 🔥 5行目にこれを追加！

# --- ⚙️ タイムゾーンと日付の設定 ---
# --- ⚙️ タイムゾーンと日付の設定 ---
import datetime as dt
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
        "platform": None,
        "title": "未定",
        "status": "START_NEW_PROJECT",
        "current_page": 0,
        "target_pages": 40,
        "history": []
    }

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=4)

state = load_state()

# --- 👔 新・5人体制のAIプロ集団（エージェント定義） ---

coo_pm = Agent(
    role="最高執行責任者 (COO) 兼 プロジェクトマネージャー",
    goal="1つのデジタルコンテンツを企画から出版まで数日かけてでも1ミリの妥協なく完遂する",
    backstory="現在のプロジェクト進捗状況（ステート）を厳格に分析し、本日チームが集中すべき最も重要な実務を定義・指揮する冷徹なリーダー。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

creator = Agent(
    role="AIプロンプトエンジニア 兼 ジュニアクリエイティブ",
    goal="画像生成AIの専門知識を活かし、他者の権利を侵さない完全クリーンで最高品質のプロンプトを設計する",
    backstory="AI画像生成の専門家。塗り絵の極細線、絵本のタッチなど、ビジュアルを呪文（プロンプト）に落とし込む実務に特化したクリエイター。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

dtp_layout_specialist = Agent(
    role="DTP 兼 レイアウトスペシャリスト",
    goal="KDP/Etsyの厳格な技術的要件（サイズ、解像度、裁ち落とし）を完璧に監査し、品質保証する",
    backstory="印刷・出版フォーマットの神様。プロンプト末尾の『8.625 x 11.25 inch with bleed, 300 DPI』等の技術要件が厳密に守られているかをミリ単位でチェックする専門職。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

native_copywriter = Agent(
    role="英語ネイティブ編集 兼 SEOコピーライター",
    goal="海外のターゲット層に響く完璧な英語表現と、検索上位表示（SEO）を最大化するマーケティングコピーを作る",
    backstory="英語ネイティブの言葉の魔術師。KDPのSEOメタデータ（タイトル、キーワード）や、読者エンゲージメントを最大化する商品説明文を専門に執筆する。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)

marketer_qa = Agent(
    role="リーガル 兼 品質保証（QA）最高責任者",
    goal="成果物の著作権・商標権検閲、およびプロジェクト完了時のさらなる組織改善案（KAIZEN）を統括する",
    backstory="Amazon/Etsyの規約、知財コンサルティングの権威。チーム全体の成果物を最終検閲し、一発審査通過を保証する砦。",
    verbose=True,
    llm="gemini/gemini-2.5-flash",
)


# --- 🧭 プロジェクトの状態に応じたプロ業務の割り当て ---
tasks = []

if state["status"] == "START_NEW_PROJECT":
    print("🆕 [5人体制始動] 新しいプロジェクトを自律的に立ち上げます。")
    task1 = Task(
        description="現在売れ筋のトレンドから、今回総力を挙げて完成させる1つの大物プロジェクトを厳選し、マイルストーン計画を立ててください。",
        expected_output="プロジェクト企画書", agent=coo_pm
    )
    task2 = Task(
        description="企画の核となる表紙デザインおよび中身の基本構成案のAIプロンプトの初稿を作成してください。",
        expected_output="プロンプト初稿", agent=creator
    )
    task3 = Task(
        description="作成された企画とプロンプトが、KDP等の規格（8.625 x 11.25 inch with bleed, 300 DPI）を満たしているかレイアウト監査を行ってください。",
        expected_output="DTP技術要件クリアの承認", agent=dtp_layout_specialist
    )
    task4 = Task(
        description="この新プロジェクトの初期SEOキーワードタグと、魅力的な仮タイトルを英語ネイティブ視点で考案してください。",
        expected_output="初期SEO・タイトル提案", agent=native_copywriter
    )
    task5 = Task(
        description="知的財産権の侵害がないかリーガルチェックを行い、プロジェクトの開始を承認してください。",
        expected_output="リーガル承認ログ", agent=marketer_qa
    )
    tasks = [task1, task2, task3, task4, task5]
    
    state["status"] = "IN_PROGRESS"
    state["title"] = f"Project_{current_date}"
    state["current_page"] = 1
    state["target_pages"] = 40

elif state["status"] == "IN_PROGRESS":
    p_title = state["title"]
    curr = state["current_page"]
    target = state["target_pages"]
    print(f"⏳ [5人体制進行] プロジェクト『{p_title}』の {curr} / {target} ページ目を専門職の連携で制作します。")
    
    task1 = Task(
        description=f"プロジェクト『{p_title}』の進捗に基づき、本日制作すべき具体的なページ内容の指示を出してください。",
        expected_output="本日の制作指示書", agent=coo_pm
    )
    task2 = Task(
        description="PMの指示に基づき、本日分の画像生成用英語プロンプトの高品質な呪文を設計してください。",
        expected_output="本日分のプロンプト初稿", agent=creator
    )
    task3 = Task(
        description="本日分のプロンプトに必ず『8.625 x 11.25 inch vertical layout with bleed, 300 DPI print-ready resolution』が組み込まれ、余白の美（ミニマリズム）が担保されているか技術検証・修正してください。",
        expected_output="レイアウト最適化済みのプロンプト一覧", agent=dtp_layout_specialist
    )
    task4 = Task(
        description="完成したプロンプトに商標侵害などの法的リスクがないか厳格に検閲してください。",
        expected_output="リーガル＆クオリティ通過の承認ログ", agent=marketer_qa
    )
    tasks = [task1, task2, task3, task4]
    
    state["current_page"] += 3
    if state["current_page"] >= state["target_pages"]:
        state["status"] = "FINAL_REVIEW"

elif state["status"] == "FINAL_REVIEW":
    p_title = state["title"]
    print(f"🎉 [5人体制最終章] 『{p_title}』の最終出版パッケージ化、および自律組織改善会を行います。")
    
    task1 = Task(
        description=f"プロジェクト『{p_title}』の全成果物を総括し、固定された最終出版台帳を構成してください。",
        expected_output="最終出版パッケージ台帳", agent=coo_pm
    )
    task2 = Task(
        description="Amazonガイドラインに完全準拠し、ターゲットに刺さる完璧な英語の商品説明文と、厳選された検索キーワード7つを完成させてください。",
        expected_output="ネイティブSEOテキスト一式", agent=native_copywriter
    )
    task3 = Task(
        description="本の総ページ数から『表紙計算ツール・背幅計算』に必要な技術的数値（リマインド情報）を出力してください。",
        expected_output="DTP最終確認データ", agent=dtp_layout_specialist
    )
    task4 = Task(
        description="今回の5人体制での稼働パフォーマンスを振り返り、次回さらに売上を伸ばすための『KDP/Etsy専任デジタルマーケター』の採用計画など、次なる組織改善提案（KAIZENノート）をまとめてください。",
        expected_output="組織改善提案書（KAIZENノート）", agent=marketer_qa
    )
    tasks = [task1, task2, task3, task4]
    
    state["status"] = "START_NEW_PROJECT"
    state["history"].append({"project": p_title, "completed_at": current_date})

# --- 🚀 実行セクション（5人全員が出勤） ---
project_crew = Crew(
    agents=[coo_pm, creator, dtp_layout_specialist, native_copywriter, marketer_qa], # 🔥 新社員2名を含む全員が着席
    tasks=tasks,
    process=Process.sequential,
    verbose=True,
    max_rpm=10 # 🔥 Gemini無料枠の安全ブレーキ
)

print(f"🤖 [自律システム] 5人体制で稼働を開始します。現在のステータス: {state['status']}")
result = project_crew.kickoff()

# 成果物の保存
project_folder = f"outputs/projects/{state['title']}"
os.makedirs(project_folder, exist_ok=True)
report_file = f"{project_folder}/{current_date}_{state['status']}_report.md"

with open(report_file, "w", encoding="utf-8") as f:
    f.write(str(result))

save_state(state)
print(f"💾 [自律システム] 業務完了。5人体制の成果がデスクに格納されました: {report_file}")
