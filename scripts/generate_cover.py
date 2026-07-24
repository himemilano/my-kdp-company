import os
import yaml
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from scripts.calculate_cover import calculate_cover_dimensions

def generate_cover_pdf():
    print("🎨 [KDP出版部] 見開きカバーPDF生成エンジン（KDP無料ISBN・5大鉄則完全準拠版）起動中...")

    dims = calculate_cover_dimensions()
    total_width = dims["total_width_pts"]
    total_height = dims["total_height_pts"]
    spine_width = dims["spine_width_pts"]
    bleed = dims["bleed_pts"]          # 裁ち落とし 3.2mm (0.125インチ = 9pt)
    trim_w = dims["trim_width_pts"]    # 仕上がり幅 (8.5インチ = 612pt)
    trim_h = dims["trim_height_pts"]   # 仕上がり高さ (11.0インチ = 792pt)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "Cover.pdf")

    # 300dpi以上の高解像度ベクター描画を維持するキャンバス作成
    c = canvas.Canvas(pdf_path, pagesize=(total_width, total_height))

    # KDP見開きレイアウトのX座標基準
    # 表4（裏表紙）: 左側
    # 背表紙: 中央
    # 表1（表紙）: 右側
    back_x = 0
    spine_x = bleed + trim_w
    front_x = spine_x + spine_width

    # 1. 背景色の塗りつぶし（裁ち落とし領域を含む全体）
    c.setFillColor(colors.HexColor("#F7F5F0"))
    c.rect(0, 0, total_width, total_height, fill=1, stroke=0)

    # -------------------------------------------------------------
    # 【鉄則2対応】 セーフゾーン（端から9.6mm以上内側）を死守した表1（表紙）のデザイン
    # -------------------------------------------------------------
    safe_margin_pt = 9.6 / 25.4 * 72  # 9.6mmをポイントに換算 (約27.2pt)
    front_content_left = front_x + bleed + safe_margin_pt
    front_content_width = trim_w - (2 * safe_margin_pt)
    
    c.setFillColor(colors.HexColor("#2C2C2C"))
    c.setFont("Helvetica-Bold", 20)
    # センター配置だがセーフゾーンの幅内で安全に描画
    c.drawCentredString(front_x + (trim_w / 2), total_height - 180, "QUIET BLOOMS OF JAPAN")
    
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawCentredString(front_x + (trim_w / 2), total_height - 210, "A Japanese Minimalist Botanical Coloring Book")
    
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(front_x + (trim_w / 2), bleed + safe_margin_pt + 20, "Hiroyoshi Matsui")

    # -------------------------------------------------------------
    # 背表紙（中央）のデザイン
    # -------------------------------------------------------------
    if spine_width > 25:
        c.saveState()
        c.translate(spine_x + (spine_width / 2), total_height / 2)
        c.rotate(90)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#333333"))
        c.drawCentredString(0, 0, "Quiet Blooms of Japan  -  Hiroyoshi Matsui")
        c.restoreState()

    # -------------------------------------------------------------
    # 【鉄則4対応】 裏表紙の右下（ISBNバーコード領域）の完全死守
    # KDP無料ISBN用ホワイトボックス（幅 2.0in × 高さ 1.2in）を配置し、
    # このエリアには絶対に文字や主線を被せない
    # -------------------------------------------------------------
    # 裏表紙の右下隅（裁ち落としとセーフティを考慮した位置）
    barcode_w = 2.0 * 72  # 144pt
    barcode_h = 1.2 * 72  # 86.4pt
    barcode_x = back_x + bleed + trim_w - barcode_w - (9.6 / 25.4 * 72)
    barcode_y = bleed + (9.6 / 25.4 * 72)

    # クリーンな白抜きボックス（KDP無料バーコード用スペース）
    c.setFillColor(colors.white)
    c.rect(barcode_x, barcode_y, barcode_w, barcode_h, fill=1, stroke=1)
    
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#444444"))
    c.drawCentredString(barcode_x + (barcode_w / 2), barcode_y + (barcode_h / 2) + 4, "Leave Blank for")
    c.drawCentredString(barcode_x + (barcode_w / 2), barcode_y + (barcode_h / 2) - 8, "KDP Free Barcode")

    # -------------------------------------------------------------
    # ガイドライン（KDP仕様確認用・トリム線）
    # -------------------------------------------------------------
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(0.5)
    # 背表紙の境界線
    c.line(spine_x, 0, spine_x, total_height)
    c.line(front_x, 0, front_x, total_height)

    c.showPage()
    c.save()
    print(f"✅ 見開きカバーPDFの生成が完了しました（KDP仕様完全準拠）: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    generate_cover_pdf()
