import os
import yaml
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from scripts.calculate_cover import calculate_cover_dimensions

def generate_cover_pdf():
    print("🎨 [KDP出版部] 見開きカバーPDF自動生成エンジン起動中...")

    dims = calculate_cover_dimensions()
    total_width = dims["total_width_pts"]
    total_height = dims["total_height_pts"]
    spine_width = dims["spine_width_pts"]
    bleed = dims["bleed_pts"]
    trim_w = dims["trim_width_pts"]
    trim_h = dims["trim_height_pts"]

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "Cover.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(total_width, total_height))

    # KDP見開きレイアウト座標定義
    # 左側(表4 / 裏表紙): x = 0 ~ (bleed + trim_w)
    # 中央(背表紙): x = (bleed + trim_w) ~ (bleed + trim_w + spine_width)
    # 右側(表1 / 表紙): x = (bleed + trim_w + spine_width) ~ total_width
    
    back_x = 0
    spine_x = bleed + trim_w
    front_x = spine_x + spine_width

    # 1. 背景色の塗りつぶし（和風ミニマリストを意識した上品なオフホワイト）
    c.setFillColor(colors.HexColor("#F7F5F0"))
    c.rect(0, 0, total_width, total_height, fill=1, stroke=0)

    # 2. 表1（表紙・右側）のデザイン構築
    c.setFillColor(colors.HexColor("#2C2C2C"))
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(front_x + (trim_w / 2), total_height - 180, "QUIET BLOOMS OF JAPAN")
    
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawCentredString(front_x + (trim_w / 2), total_height - 210, "A Japanese Minimalist Botanical Coloring Book")
    
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(front_x + (trim_w / 2), 100, "Hiroyoshi Matsui")

    # 3. 背表紙（中央）の文字配置（背幅が十分にある場合のみ回転して配置）
    if spine_width > 25:
        c.saveState()
        c.translate(spine_x + (spine_width / 2), total_height / 2)
        c.rotate(90)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#333333"))
        c.drawCentredString(0, 0, "Quiet Blooms of Japan  -  Hiroyoshi Matsui")
        c.restoreState()

    # 4. 表4（裏表紙・左側）のデザイン構築（バーコード用プレースホルダー枠）
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    c.rect(back_x + bleed + 36, bleed + 36, 100, 75, fill=0, stroke=1)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawString(back_x + bleed + 36, bleed + 120, "[ Barcode Area ]")

    # 5. ガイドライン（KDP裁ち落とし・折り目境界線の視覚化：デバッグ用）
    c.setStrokeColor(colors.HexColor("#E0E0E0"))
    c.setLineWidth(0.5)
    c.line(spine_x, 0, spine_x, total_height)
    c.line(front_x, 0, front_x, total_height)

    c.showPage()
    c.save()
    print(f"✅ 見開きカバーPDFの生成が完了しました: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    generate_cover_pdf()
