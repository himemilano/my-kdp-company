import os
import yaml

def calculate_cover_dimensions(project_slug="01_tranquil_flora"):
    print(f"📐 [KDP汎用エンジン] プロジェクト '{project_slug}' のカバー寸法を計算中...")
    
    project_root = f"projects/{project_slug}"
    workspace_dir = os.path.join(project_root, "kdp_workspace")
    manifest_path = os.path.join(workspace_dir, "kdp_final_upload_manifest.md")
    
    # デフォルト値
    page_count = 60
    spine_width_inch = 0.1351
    
    # マニフェストから動的に抽出を試みる（簡易パーサー）
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                content = f.read()
                for line in content.splitlines():
                    if "総ページ数" in line:
                        import re
                        numbers = re.findall(r'\d+', line)
                        if numbers:
                            page_count = int(numbers[0])
                    if "背幅" in line:
                        import re
                        floats = re.findall(r'\d+\.\d+', line)
                        if floats:
                            spine_width_inch = float(floats[0])
        except Exception as e:
            print(f"⚠️ マニフェストの解析に失敗しました（デフォルト値を使用します）: {e}")

    trim_width_inch = 8.5
    trim_height_inch = 11.0
    bleed_inch = 0.125
    
    total_width_inch = 2 * (trim_width_inch + bleed_inch) + spine_width_inch
    total_height_inch = trim_height_inch + (2 * bleed_inch)
    
    dimensions = {
        "project_slug": project_slug,
        "page_count": page_count,
        "spine_width_inch": spine_width_inch,
        "total_width_inch": round(total_width_inch, 4),
        "total_height_inch": round(total_height_inch, 4),
        "total_width_pts": round(total_width_inch * 72, 2),
        "total_height_pts": round(total_height_inch * 72, 2),
        "trim_width_pts": trim_width_inch * 72,
        "trim_height_pts": trim_height_inch * 72,
        "bleed_pts": bleed_inch * 72,
        "spine_width_pts": spine_width_inch * 72
    }
    
    print(f"📊 検出ページ数: {page_count}p, 計算背幅: {spine_width_inch}インチ")
    return dimensions

if __name__ == "__main__":
    calculate_cover_dimensions()
