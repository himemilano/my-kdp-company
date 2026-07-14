import os
import sys
import time
import subprocess
from datetime import datetime, timedelta, timezone

# 日本時間設定
jst = timezone(timedelta(hours=9))

# 実行ターゲット：トップ階層に配置されている main.py
SCRIPT_TO_RUN = "main.py"

# APIリミットセーフガード (1分間の最大リクエスト数12回：約5秒に1回の間隔)
MAX_REQUESTS_PER_MINUTE = 12
REQUEST_INTERVAL = 60 / MAX_REQUESTS_PER_MINUTE

def run_main_safely():
    if not os.path.exists(SCRIPT_TO_RUN):
        print(f"⚠️ 実行対象の {SCRIPT_TO_RUN} が見つかりません。")
        return False
        
    current_time = datetime.now(jst).strftime("%H:%M:%S")
    print(f"\n[🔄 KDP自律ループ実行] {current_time} - {SCRIPT_TO_RUN} を起動します...")
    
    start_time = time.time()
    try:
        # main.pyをプロセスとして実行
        result = subprocess.run([sys.executable, SCRIPT_TO_RUN], capture_output=True, text=True, timeout=300)
        
        # 実行ログの出力
        print(result.stdout)
        if result.stderr:
            print(f"❌ エラー出力:\n{result.stderr}")
            
        elapsed = time.time() - start_time
        print(f"⏱️ 完了 (処理時間: {elapsed:.1f}秒)")
        
        # API保護待機
        time.sleep(REQUEST_INTERVAL)
        return True
    except subprocess.TimeoutExpired:
        print(f"⚠️ 5分以上応答がないためタイムアウトしました: {SCRIPT_TO_RUN}")
        return False
    except Exception as e:
        print(f"❌ 実行中にエラーが発生しました: {e}")
        return False

def main():
    print("==========================================================")
    print("🔥 my-kdp-company 自律常時限界ループランナー 🔥")
    print("==========================================================")
    
    loop_start_time = time.time()
    max_loop_duration = 5 * 60 * 60 + 40 * 60 # 5時間40分ループを維持
    
    run_count = 0
    while True:
        elapsed_total = time.time() - loop_start_time
        if elapsed_total > max_loop_duration:
            print("⏳ GitHub Actionsの制限時間に達したため、次の巡回サイクルへバトンを繋ぎます。")
            break
            
        run_count += 1
        print(f"\n--- 📚 第 {run_count} 回目の KDP 自律実行サイクル ---")
        
        # main.pyを実行
        run_main_safely()
            
        # 実行完了後のクールダウン
        time.sleep(15)
        
        # main.pyによって更新されたoutputsフォルダや各種マークダウン小説を検知して自動コミット
        try:
            subprocess.run(["git", "config", "--local", "user.email", "action@github.com"], capture_output=True)
            subprocess.run(["git", "config", "--local", "user.name", "GitHub Action"], capture_output=True)
            subprocess.run(["git", "add", "."], capture_output=True)
            
            status_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if status_res.stdout.strip():
                print("📦 新規データ、小説執筆の成果物を検知しました。自動プッシュします...")
                subprocess.run(["git", "commit", "-m", "📚 [KDP-Autonomy] 24時間自律ループにより最新執筆データを自動コミット"], capture_output=True)
                subprocess.run(["git", "push"], capture_output=True)
        except Exception as e:
            print(f"⚠️ 自動コミット処理中にエラーが発生しました: {e}")

if __name__ == "__main__":
    main()

