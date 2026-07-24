import os
import yaml
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from calculate_cover import calculate_cover_dimensions

def generate_cover_pdf():
    print("🎨 [KDP出版部] カバーPDF自動生成エンジン起動中...")

    # 1. 寸法データの取得
    dims = calculate_cover_dimensions()
    total_width = dims["total_width_pts"]
    total_height = dims["total_height_pts"]
    spine_width = dims["spine_width_inch"] * 72

    # 2. 出力ディレクトリの作成
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "Cover.pdf")

    # 3. PDFキャンバスの作成（カスタムサイズ）
    c = canvas.Canvas(pdf_path, pagesize=(total_width, total_height))

    # 4. 背景（表4：裏表紙、背表紙、表1：表紙のレイアウト構築）
    c.setFillColor(colors.HexColor("#F9F9F9"))
    c.rect(0, 0, total_width, total_height, fill=1, stroke=0)

    # 境界線やガイドラインの描画
    c.setStrokeColor(colors.gray)
    c.setLineWidth(0.5)

    center_x = total_width / 2
    c.line(center_x - (spine_width / 2), 0, center_x - (spine_width / 2), total_height)
    c.line(center_x + (spine_width / 2), 0, center_x + (spine_width / 2), total_height)

    # テキスト配置
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 16)
    
    # 表1（右側エリア）のタイトル配置
    c.drawCentredString(total_width * 0.75, total_height - 150, "Quiet Blooms of Japan")
    c.setFont("Helvetica", 12)
    c.drawCentredString(total_width * 0.75, total_height - 180, "A Japanese Minimalist Botanical Coloring Book")

    # 背表紙のタイトル配置
    if spine_width > 20:
        c.saveState()
        c.translate(center_x, total_height / 2)
        c.rotate(90)
        c.setFont("Helvetica", 8)
        c.drawCentredString(0, 0, "Quiet Blooms of Japan")
        c.restoreState()

    # 表4（左側エリア）のバーコードプレースホルダー
    c.rect(54, 54, 100, 75)
    c.setFont("Helvetica", 9)
    c.drawString(54, 140, "[ Barcode Placeholder ]")

    c.showPage()
    c.save()
    print(f"✅ カバーPDFの生成が完了しました: {pdf_path}")

if __name__ == "__main__":
    generate_cover_pdf()
