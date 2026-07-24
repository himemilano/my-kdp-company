import os
import csv
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

def generate_interior_pdf(project_slug="01_tranquil_flora"):
    print(f"🎨 [KDP汎用エンジン] プロジェクト '{project_slug}' の内装PDFを構築中...")

    project_root = f"projects/{project_slug}"
    workspace_dir = os.path.join(project_root, "kdp_workspace")
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    interior_pdf_path = os.path.join(output_dir, "Interior.pdf")

    # プロジェクト固有の本文CSVを動的探索
    csv_files = [f for f in os.listdir(workspace_dir) if f.endswith("_body_bulk_create.csv")]
    body_data = []
    if csv_files:
        csv_path = os.path.join(workspace_dir, csv_files[0])
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                body_data.append(row)
        print(f"📂 本文CSV ({csv_files[0]}) から {len(body_data)} 件のデータをロードしました。")

    total_pages = 60 # 基本はマニフェスト・CSV連動（今回は60ページ）[span_1](start_span)[span_1](end_span)

    pt_per_inch = 72
    bleed_pt = 0.125 * pt_per_inch
    trim_width = 8.5 * pt_per_inch
    trim_height = 11.0 * pt_per_inch
    total_width = trim_width + (2 * bleed_pt)
    total_height = trim_height + (2 * bleed_pt)

    c = KDPPrintedCanvas(interior_pdf_path, pagesize=(total_width, total_height))

    csv_index = 0
    for page_num in range(1, total_pages + 1):
        bx = bleed_pt
        by = bleed_pt

        if page_num % 2 == 0:
            title_text = f"Notes - Page {page_num}"
            desc_text = "Project Layout Content"
            
            if csv_index < len(body_data):
                row = body_data[csv_index]
                title_text = row.get("title", title_text)
                desc_text = row.get("description", desc_text)
                csv_index += 1

            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(colors.HexColor("#333333"))
            c.drawString(bx + 36, by + trim_height - 54, title_text)
            c.setFont("Helvetica", 10)
            c.drawString(bx + 36, by + trim_height - 80, desc_text)
            
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
            
            c.setStrokeColor(colors.black)
            c.setLineWidth(1)
            c.rect(x_pos, y_pos, frame_width, frame_height)
            
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.HexColor("#666666"))
            c.drawCentredString(bx + (trim_width / 2), by + (trim_height / 2), "[ Line Art Asset Frame ]")

        c.showPage()

    c.save()
    print(f"✅ 内装PDFの生成が完了しました: {interior_pdf_path}")
    return interior_pdf_path
