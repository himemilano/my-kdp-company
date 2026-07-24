import os
import yaml

def calculate_cover_dimensions():
    print("📐 [KDP出版部] 表紙寸法・背幅計算エンジン起動中...")
    
    config_path = "config.yml"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    trim_width_inch = 8.5
    trim_height_inch = 11.0
    bleed_inch = 0.125
    
    page_count = config.get("book_specs", {}).get("page_count", 50)
    spine_width_inch = page_count * 0.002252
    
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
    
    print(f"📊 ページ数: {page_count}p, 背幅: {dimensions['spine_width_inch']}インチ")
    print(f"🖼️ カバー総サイズ: 幅 {dimensions['total_width_inch']}in × 高さ {dimensions['total_height_inch']}in")
    
    return dimensions

if __name__ == "__main__":
    calculate_cover_dimensions()
