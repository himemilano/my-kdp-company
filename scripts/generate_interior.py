import os
import json
import yaml
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class KDPPrintedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_kdp_footer(num_pages)
            super().showPage()
        super().save()

    def draw_kdp_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        page_text = f"{self._pageNumber}"
        width_pt = 8.5 * 72 + 18 
        
        if self._pageNumber % 2 == 0:
            self.drawString(54, 36, page_text)
        else:
            self.drawRightString(width_pt - 54, 36, page_text)
        self.restoreState()

def generate_interior_pdf():
    print("🎨 [KDP出版部] 内装PDFレイアウトエンジン起動中（事前チェック優先・個別プロジェクト保存）...")

    # 1. 設定のロード
    config_path = "config.yml"
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    genre = config.get("genre_layouts", {}).get("coloring_book", {})
    min_pages = genre.get("min_pages", 24)

    # 2. プロジェクトごとのパス解決
    project_slug = config.get("project", {}).get("name", "01_tranquil_flora")
    project_root = f"projects/{project_slug}"
    workspace_dir = os.path.join(project_root, "kdp_workspace")
    output_dir = os.path.join(project_root, "output") # プロジェクト別出力先
    assets_dir = os.path.join(project_root, "assets") # プロジェクト別アセット格納先（ルートの assets もフォールバック確認）

    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

    interior_pdf_path = os.path.join(output_dir, "Interior.pdf")

    # 3. 【順序修正】PDF生成の前にアセットの厳格チェックを行う
    image_files = []
    search_dirs = [assets_dir, "assets"] # プロジェクト内またはルートのassets
    for d in search_dirs:
        if os.path.exists(d):
            found = sorted([
                os.path.join(d, f) for f in os.listdir(d)
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))
            ])
            if found:
                image_files = found
                break

    print(f"📂 検出されたアセット画像数: {len(image_files)} 枚")
    
    if len(image_files) == 0:
        print(f"❌ 【厳格チェックエラー】有効なアセット画像が {assets_dir}（または assets/）に存在しません。")
        print("💡 対策: 塗り絵の線画画像をプロジェクトのアセットフォルダに配置してください。空のPDF生成を中断します。")
        raise FileNotFoundError("有効な画像アセットが見つからないため、内装PDFの生成を中断しました。")

    # 4. KDP寸法計算とPDF構築
    pt_per_inch = 72
    bleed_pt = 0.125 * pt_per_inch
    trim_width = 8.5 * pt_per_inch
    trim_height = 11.0 * pt_per_inch
    total_width = trim_width + (2 * bleed_pt)
    total_height = trim_height + (2 * bleed_pt)

    c = KDPPrintedCanvas(interior_pdf_path, pagesize=(total_width, total_height))

    image_index = 0
    for page_num in range(1, min_pages + 1):
        bx = bleed_pt
        by = bleed_pt

        if page_num % 2 == 0:
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(colors.HexColor("#333333"))
            c.drawString(bx + 36, by + trim_height - 54, f"Coloring Notes & Palette - Page {page_num}")
            c.setFont("Helvetica", 10)
            c.drawString(bx + 36, by + trim_height - 80, "Use this page for testing markers or recording color combinations.")
            c.setStrokeColor(colors.HexColor("#CCCCCC"))
            c.setLineWidth(0.5)
            c.rect(bx + 36, by + 54, trim_width - 72, trim_height - 120)
        else:
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(colors.HexColor("#333333"))
            c.drawString(bx + 36, by + trim_height - 36, f"Plate {page_num // 2 + 1}")
            
            margin = 36 
            frame_width = trim_width - (2 * margin)
            frame_height = trim_height - 90
            x_pos = bx + margin
            y_pos = by + 45
            
            if image_index < len(image_files):
                img_path = image_files[image_index]
                c.drawImage(img_path, x_pos, y_pos, width=frame_width, height=frame_height, preserveAspectRatio=True, anchor='c')
                image_index += 1

        c.showPage()

    c.save()
    print(f"✅ 内装PDFの生成が完了しました: {interior_pdf_path}")
    return interior_pdf_path

if __name__ == "__main__":
    generate_interior_pdf()
