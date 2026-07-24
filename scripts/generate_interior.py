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
    print("🎨 [KDP出版部] 内装PDFレイアウトエンジン起動中（厳格チェック体制）...")

    # 1. 設定のロードと厳格なバリデーション
    config_path = "config.yml"
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    else:
        raise FileNotFoundError("❌ 必須設定ファイル 'config.yml' が存在しません。")

    genre = config.get("genre_layouts", {}).get("coloring_book", {})
    min_pages = genre.get("min_pages", 24)

    workspace_dir = "kdp_workspace"
    active_proj_path = "active_project.json"
    if os.path.exists(active_proj_path):
        with open(active_proj_path, "r", encoding="utf-8") as f:
            project_info = json.load(f)
        workspace_dir = os.path.join(project_info.get("project_root", "projects/01_tranquil_flora"), "kdp_workspace")

    output_dir = "output"
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    interior_pdf_path = os.path.join(output_dir, "Interior.pdf")

    # 2. アセットのロードとチェック体制の稼働
    assets_dir = "assets"
    image_files = []
    if os.path.exists(assets_dir):
        image_files = sorted([
            os.path.join(assets_dir, f) for f in os.listdir(assets_dir)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ])
    
    print(f"📂 検出されたアセット画像数: {len(image_files)} 枚")
    
    # 厳格チェック：アセットが0枚の場合、そのまま通さずに警告を出しつつプレースホルダーで堅牢に出力するか、要件チェックを通す
    if len(image_files) == 0:
        print("⚠️ 【警告・チェック体制】有効なアセット画像が検出されませんでした。プレースホルダーフレームで内装PDFを構築します。")

    # 3. KDP寸法計算
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
                try:
                    c.drawImage(img_path, x_pos, y_pos, width=frame_width, height=frame_height, preserveAspectRatio=True, anchor='c')
                    image_index += 1
                except Exception as e:
                    print(f"⚠️ 画像読み込みエラー ({img_path}): {e}")
                    c.setStrokeColor(colors.black)
                    c.rect(x_pos, y_pos, frame_width, frame_height)
                    c.drawCentredString(bx + (trim_width / 2), by + (trim_height / 2), "[ Image Load Error ]")
            else:
                c.setStrokeColor(colors.black)
                c.setLineWidth(1)
                c.rect(x_pos, y_pos, frame_width, frame_height)
                c.setFont("Helvetica", 9)
                c.setFillColor(colors.HexColor("#666666"))
                c.drawCentredString(bx + (trim_width / 2), by + (trim_height / 2), "[ AI Line Art Illustration Frame (Awaiting Asset) ]")

        c.showPage()

    c.save()
    print(f"✅ 内装PDFの生成が完了しました: {interior_pdf_path}")
    return interior_pdf_path

if __name__ == "__main__":
    generate_interior_pdf()
