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

    # ページ数をデータ数から動的算出（デフォルト60ページ、またはCSV量に応じた調整）
    total_pages = max(60, len(body_data) * 2) if body_data else 60

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
            # 偶数ページ（左側）：タイトル、解説、塗る時のヒント
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
            c.setFillColor(colors.HexColor("#555555"))
            c.drawString(bx + 36, by + trim_height - 80, desc_text[:80])
            
            c.setStrokeColor(colors.HexColor("#DDDDDD"))
            c.setLineWidth(0.5)
            c.rect(bx + 36, by + 54, trim_width - 72, trim_height - 120)
        else:
            # 奇数ページ（右側）：Pythonによるミニマル植物線画アートの自動描画
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(colors.HexColor("#333333"))
            c.drawString(bx + 36, by + trim_height - 36, f"Plate {page_num // 2 + 1}")
            
            margin = 36 
            frame_width = trim_width - (2 * margin)
            frame_height = trim_height - 90
            x_pos = bx + margin
            y_pos = by + 45
            
            # 外枠（セーフゾーン）
            c.setStrokeColor(colors.black)
            c.setLineWidth(1)
            c.rect(x_pos, y_pos, frame_width, frame_height)
            
            # Pythonスクリプトによるミニマル線画の描画処理
            c.saveState()
            c.setStrokeColor(colors.HexColor("#222222"))
            c.setLineWidth(0.75)
            
            center_x = x_pos + (frame_width / 2)
            center_y = y_pos + (frame_height / 2)
            
            # 侘び寂び・ミニマリズムを表現する同心円やボタニカルラインのベクター描画
            for r in range(25, 130, 30):
                c.circle(center_x, center_y, r, stroke=1, fill=0)
            
            c.line(center_x, y_pos + 50, center_x, y_pos + frame_height - 50)
            c.line(x_pos + 50, center_y, x_pos + frame_width - 50, center_y)
            
            c.restoreState()
            
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.HexColor("#666666"))
            c.drawCentredString(center_x, y_pos + 15, "Minimalist Botanical Line Art (Generated via Python)")

        c.showPage()

    c.save()
    print(f"✅ 内装PDFの生成が完了しました: {interior_pdf_path}")
    return interior_pdf_path

if __name__ == "__main__":
    generate_interior_pdf()
