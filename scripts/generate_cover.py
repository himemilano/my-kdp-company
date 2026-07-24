import os
import csv
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from scripts.calculate_cover import calculate_cover_dimensions

def generate_cover_pdf(project_slug="01_tranquil_flora"):
    print(f"🎨 [KDP汎用エンジン] プロジェクト '{project_slug}' の見開きカバーを構築中...")

    dims = calculate_cover_dimensions(project_slug)
    total_width = dims["total_width_pts"]
    total_height = dims["total_height_pts"]
    spine_width = dims["spine_width_pts"]
    bleed = dims["bleed_pts"]
    trim_w = dims["trim_width_pts"]

    workspace_dir = f"projects/{project_slug}/kdp_workspace"
    output_dir = f"projects/{project_slug}/output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "Cover.pdf")

    # カバー要素CSVを動的探索
    csv_files = [f for f in os.listdir(workspace_dir) if f.endswith("_cover_elements.csv")]
    title_main = "静寂の草花"
    title_sub = "日本のミニマル植物塗り絵"
    author_name = "Hiroyoshi Matsui"
    
    if csv_files:
        cover_csv_path = os.path.join(workspace_dir, csv_files[0])
        with open(cover_csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "title" in row: title_main = row["title"]
                if "subtitle" in row: title_sub = row["subtitle"]
                if "author" in row: author_name = row["author"]

    c = canvas.Canvas(pdf_path, pagesize=(total_width, total_height))

    back_x = 0
    spine_x = bleed + trim_w
    front_x = spine_x + spine_width

    # 1. 背景色の塗りつぶし
    c.setFillColor(colors.HexColor("#F7F5F0"))
    c.rect(0, 0, total_width, total_height, fill=1, stroke=0)

    # 2. 表1（表紙）：セーフゾーン（9.6mm内側）を死守
    safe_margin_pt = 9.6 / 25.4 * 72
    
    c.setFillColor(colors.HexColor("#2C2C2C"))
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(front_x + (trim_w / 2), total_height - 180, title_main)
    
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawCentredString(front_x + (trim_w / 2), total_height - 210, title_sub)
    
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(front_x + (trim_w / 2), bleed + safe_margin_pt + 20, author_name)

    # 3. 背表紙
    if spine_width > 25:
        c.saveState()
        c.translate(spine_x + (spine_width / 2), total_height / 2)
        c.rotate(90)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#333333"))
        c.drawCentredString(0, 0, f"{title_main} - {author_name}")
        c.restoreState()

    # 4. 裏表紙：KDP無料ISBN用ホワイトボックス（右下固定・5大鉄則準拠）
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
