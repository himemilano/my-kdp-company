import os
import re
import json
from pathlib import Path

def calculate_kdp_cover_size(page_count: int, width: float = 8.5, height: float = 11.0) -> dict:
    """
    Amazon KDP公式の計算ロジックに基づき、Canva用の正確なカバー寸法を計算する
    (白紙・黒白標準インテリア用)
    """
    spine_width = page_count * 0.002252
    bleed = 0.125
    
    total_width = (width * 2) + spine_width + (bleed * 2)
    total_height = height + (bleed * 2)
    
    return {
        "page_count": page_count,
        "spine_width_inch": round(spine_width, 4),
        "canva_width_inch": round(total_width, 4),
        "canva_height_inch": round(total_height, 4)
    }

def main():
    print("🚀 [KDP Automation v2] システムを起動しました。")
    
    # 1. お宝資産 (kdp_production_note.md) の読み込み
    note_path = Path("kdp_production_note.md")
    if not note_path.exists():
        print("❌ エラー: ルート直下に 'kdp_production_note.md' が見つかりません。")
        return

    print("📖 'kdp_production_note.md' から原稿データをスキャン中...")
    with open(note_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. ワークスペースのディレクトリ作成
    workspace_dir = Path("kdp_workspace")
    workspace_dir.mkdir(exist_ok=True)

    # 3. KDPカバー寸法の自動計算 (Tranquil Floraは全60ページ構成)
    dimensions = calculate_kdp_cover_size(page_count=60)
    print(f"📐 KDP公式サイズ計算完了: Canva入力サイズ -> 横 {dimensions['canva_width_inch']} x 縦 {dimensions['canva_height_inch']} インチ")

    # 4. Midjourneyプロンプトの抽出 (Canva一括作成用)
    print("🎨 Canva一括インポート用のプロンプトデータを抽出しています...")
    # プロンプトのブロックを見つける正規表現
    prompt_matches = re.findall(r"【(P\d+(?:-\d+)?|.*?):(.*?)】\s*(.*?)(?=\n【|\n\n\d+\.\s*マーケティング|$)", content, re.DOTALL)
    
    canva_data = ["Page,Section_Title,Midjourney_Prompt"]
    for match in prompt_matches:
        page_info = match[0].strip()
        title_ja = match[1].strip()
        prompt_text = match[2].strip().replace('"', '""') # CSVのエスケープ処理
        
        # 改行などをクレンジング
        prompt_text = " ".join(prompt_text.split())
        canva_data.append(f'"{page_info}","{title_ja}","{prompt_text}"')

    # Canva用CSVの書き出し
    canva_csv_path = workspace_dir / "canva_prompts_manifest.csv"
    with open(canva_csv_path, "w", encoding="utf-8") as f:
        f.write("\n".join(canva_data))
    print(f"💾 Canva用CSVを保存しました: {canva_csv_path}")

    # 5. KDP登録用マーケティング素材の抽出と寸法データのドッキング
    print("📝 KDP登録用（Amazon US向け）のメタデータを整形しています...")
    
    # 元ノートからマーケティングセクションを抽出
    marketing_section = ""
    marketing_match = re.search(r"3\.\s*マーケティング素材.*", content, re.DOTALL)
    if marketing_match:
        marketing_section = marketing_match.group(0)

    # カバーサイズのアドバイスを動的に生成してドッキング
    cover_advice = f"""
## 📐 Canva Cover Design Dimensions (Auto-Calculated)
Go to Canva -> Create a design -> Custom size -> Select **"inches"** and enter:
*   **Width:** `{dimensions['canva_width_inch']}` inches
*   **Height:** `{dimensions['canva_height_inch']}` inches

*   Total Page Count: {dimensions['page_count']} pages
*   Calculated Spine Width: {dimensions['spine_width_inch']} inches
*   Paper Type: Black & White interior with White Paper
"""

    kdp_final_content = f"# KDP Production Package: Tranquil Flora\n\n{cover_advice}\n\n{marketing_section}"
    
    kdp_info_path = workspace_dir / "kdp_final_upload_manifest.md"
    with open(kdp_info_path, "w", encoding="utf-8") as f:
        f.write(kdp_final_content)
    print(f"💾 KDP登録用最終マニフェストを保存しました: {kdp_info_path}")

    print("✨ [SUCCESS] すべてのデータ抽出と計算が完了しました！kdp_workspace フォルダを確認してください。")

if __name__ == "__main__":
    main()
