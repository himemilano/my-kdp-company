import os
import yaml

def calculate_cover_dimensions():
    print("📐 [KDP出版部] 表紙寸法・背幅計算エンジン起動中...")
    
    # 1. 設定ファイルの読み込み
    if os.path.exists("config.yml"):
        with open("config.yml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    # デフォルト値の定義 (USレターサイズ: 8.5 x 11 インチ)
    trim_width_inch = 8.5
    trim_height_inch = 11.0
    bleed_inch = 0.125
    
    # ページ数の取得（設定ファイルまたはデフォルト50ページ）
    page_count = config.get("book_specs", {}).get("page_count", 50)
    
    # KDP公式背幅計算式 (白紙・白黒ペーパーバックの場合: 1ページあたり約0.002252インチ)
    spine_width_inch = page_count * 0.002252
    
    # 総カバー寸法の計算 (裁ち落とし込み)
    total_width_inch = 2 * (trim_width_inch + bleed_inch) + spine_width_inch
    total_height_inch = trim_height_inch + (2 * bleed_inch)
    
    dimensions = {
        "page_count": page_count,
        "spine_width_inch": round(spine_width_inch, 4),
        "total_width_inch": round(total_width_inch, 4),
        "total_height_inch": round(total_height_inch, 4),
        "total_width_pts": round(total_width_inch * 72, 2),
        "total_height_pts": round(total_height_inch * 72, 2)
    }
    
    print(f"📊 計算結果: ページ数={page_count}p, 背幅={dimensions['spine_width_inch']}インチ")
    print(f"🖼️ カバー総サイズ: 幅 {dimensions['total_width_inch']}in × 高さ {dimensions['total_height_inch']}in")
    
    return dimensions

if __name__ == "__main__":
    calculate_cover_dimensions()
