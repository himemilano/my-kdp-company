import os
from reportlab.graphics.shapes import Drawing, Circle, Rect, Line
from reportlab.graphics import renderPM
from reportlab.lib import colors

def generate_botanical_line_art(output_path, page_index):
    d = Drawing(500, 700)
    d.add(Rect(0, 0, 500, 700, fillColor=colors.white, strokeColor=None))
    
    cx, cy = 250, 350
    
    if page_index % 4 == 1:
        for r in range(40, 160, 35):
            d.add(Circle(cx, cy, r, fillColor=None, strokeColor=colors.black, strokeWidth=1))
        d.add(Line(cx, 150, cx, 550, strokeColor=colors.black, strokeWidth=1))
    elif page_index % 4 == 2:
        for r in range(30, 180, 40):
            d.add(Circle(cx, cy, r, fillColor=None, strokeColor=colors.black, strokeWidth=0.75))
        d.add(Line(100, cy, 400, cy, strokeColor=colors.black, strokeWidth=0.75))
    elif page_index % 4 == 3:
        d.add(Rect(220, 100, 60, 500, fillColor=None, strokeColor=colors.black, strokeWidth=1))
        for i in range(150, 600, 80):
            d.add(Line(150, i, 350, i, strokeColor=colors.black, strokeWidth=0.75))
    else:
        for r in range(20, 200, 30):
            d.add(Circle(cx, cy, r, fillColor=None, strokeColor=colors.black, strokeWidth=0.8))
    
    renderPM.drawToFile(d, output_path, fmt='PNG', dpi=300)

def run_asset_agent(project_slug):
    print(f"🌿 [Asset Agent] プロジェクト '{project_slug}' の線画ビジュアルアセットを生成中...")
    project_root = f"projects/{project_slug}"
    assets_dir = os.path.join(project_root, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    for i in range(1, 21):
        asset_path = os.path.join(assets_dir, f"plate_{i:02d}.png")
        generate_botanical_line_art(asset_path, i)
        
    print(f"✅ すべての線画アセットの生成が完了しました: {assets_dir}")
