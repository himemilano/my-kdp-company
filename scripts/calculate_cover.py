import os
import yaml

def calculate_cover_dimensions():
    print("📐 [KDP出版部] 表紙寸法・背幅計算エンジン起動中...")
    
    config_path = "config.yml"
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    trim_width_inch = 8.5
    trim_height_inch = 11.0
    bleed_inch = 0.125
    
    # ページ数から背幅を厳密に計算（白黒・クリーム紙の標準係数: 0.002252インチ/ページ）
    genre = config.get("genre_layouts", {}).get("coloring_book", {})
    page_count = config.get("book_specs", {}).get("page_count", genre.get("min_pages", 24))
    spine_width_inch = page_count * 0.002252
    
    # KDP見開きカバー総サイズ = (表4幅 + 裁ち落とし) + 背幅 + (表1幅 + 裁ち落とし)
    total_width_inch = 2 * (trim_width_inch + bleed_inch) + spine_width_inch
    total_height_inch = trim_height_inch + (2 * bleed_inch)
    
    dimensions = {
        "page_count": page_count,
        "spine_width_inch": round(spine_width_inch, 4),
        "total_width_inch": round(total_width_inch, 4),
        "total_height_inch": round(total_height_inch, 4),
        "total_width_pts": round(total_width_inch * 72, 2),
        "total_height_pts": round(total_height_inch * 72, 2),
        "trim_width_pts": trim_width_inch * 72,
        "trim_height_pts": trim_height_inch * 72,
        "bleed_pts": bleed_inch * 72,
        "spine_width_pts": spine_width_inch * 72
    }
    
    print(f"📊 ページ数: {page_count}p, 背幅: {dimensions['spine_width_inch']}インチ")
    print(f"🖼️ 見開きカバー総サイズ: 幅 {dimensions['total_width_inch']}in × 高さ {dimensions['total_height_inch']}in")
    
    return dimensions

if __name__ == "__main__":
    calculate_cover_dimensions()
