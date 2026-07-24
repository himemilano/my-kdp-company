import os
import yaml
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from scripts.calculate_cover import calculate_cover_dimensions

def generate_cover_pdf():
    print("🎨 [KDP出版部] 見開きカバーPDF生成エンジン（個別プロジェクト保存版）起動中...")

    dims = calculate_cover_dimensions()
    total_width = dims["total_width_pts"]
    total_height = dims["total_height_pts"]
    spine_width = dims["spine_width_pts"]
    bleed = dims["bleed_pts"]
    trim_w = dims["trim_width_pts"]
    trim_h = dims["trim_height_pts"]

    # プロジェクト別出力先の取得
    config_path = "config.yml"
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    project_slug = config.get("project", {}).get("name", "01_tranquil_flora")
    output_dir = os.path.join(f"projects/{project_slug}", "output")
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "Cover.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(total_width, total_height))

    back_x = 0
    spine_x = bleed + trim_w
    front_x = spine_x + spine_width

    # 1. 背景色の塗りつぶし
    c.setFillColor(colors.HexColor("#F7F5F0"))
    c.rect(0, 0, total_width, total_height, fill=1, stroke=0)

    # 2. 表1（表紙）
    safe_margin_pt = 9.6 / 25.4 * 72
    c.setFillColor(colors.HexColor("#2C2C2C"))
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(front_x + (trim_w / 2), total_height - 180, "QUIET BLOOMS OF JAPAN")
    
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawCentredString(front_x + (trim_w / 2), total_height - 210, "A Japanese Minimalist Botanical Coloring Book")
    
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(front_x + (trim_w / 2), bleed + safe_margin_pt + 20, "Hiroyoshi Matsui")

    # 3. 背表紙
    if spine_width > 25:
        c.saveState()
        c.translate(spine_x + (spine_width / 2), total_height / 2)
        c.rotate(90)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#333333"))
        c.drawCentredString(0, 0, "Quiet Blooms of Japan  -  Hiroyoshi Matsui")
        c.restoreState()

    # 4. 裏表紙（KDP無料ISBN用ホワイトボックス）
    barcode_w = 2.0 * 72
    barcode_h = 1.2 * 72
    barcode_x = back_x + bleed + trim_w - barcode_w - (9.6 / 25.4 * 72)
    barcode_y = bleed + (9.6 / 25.4 * 72)

    c.setFillColor(colors.white)
    c.rect(barcode_x, barcode_y, barcode_w, barcode_h, fill=1, stroke=1)
    
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#444444"))
    c.drawCentredString(barcode_x + (barcode_w / 2), barcode_y + (barcode_h / 2) + 4, "Leave Blank for")
    c.drawCentredString(barcode_x + (barcode_w / 2), barcode_y + (barcode_h / 2) - 8, "KDP Free Barcode")

    # 5. ガイドライン
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(0.5)
    c.line(spine_x, 0, spine_x, total_height)
    c.line(front_x, 0, front_x, total_height)

    c.showPage()
    c.save()
    print(f"✅ 見開きカバーPDFの生成が完了しました: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    generate_cover_pdf()
