import os
import yaml
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class NumberedCanvas(canvas.Canvas):
    """ページ番号を動的に描画するためのカスタムキャンバス"""
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
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.gray)
        # 奇数・偶数に応じたシンプルなフッターページ番号配置
        page_text = f"{self._pageNumber}"
        self.drawRightString(8.5 * 72 - 36, 36, page_text)
        self.restoreState()

def generate_interior_pdf():
    print("🎨 [KDP出版部] 内装PDFレイアウトエンジン起動中...")

    # 1. 設定ファイルの読み込み
    if os.path.exists("config.yml"):
        with open("config.yml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    # デフォルトは大人向け塗り絵本モード
    genre = config.get("genre_layouts", {}).get("coloring_book", {})
    min_pages = genre.get("min_pages", 24)

    # 2. アクティブプロジェクトのワークスペース特定
    if os.path.exists("active_project.json"):
        with open("active_project.json", "r", encoding="utf-8") as f:
            project_info = json.load(f)
        workspace_dir = os.path.join(project_info["project_root"], "kdp_workspace")
    else:
        workspace_dir = "kdp_workspace"

    os.makedirs(workspace_dir, exist_ok=True)
    pdf_path = os.path.join(workspace_dir, "interior_output.pdf")

    # 3. 判型設定 (USレターサイズ: 8.5 x 11 インチをポイントに変換)
    width, height = 8.5 * 72, 11.0 * 72
    c = NumberedCanvas(pdf_path, pagesize=(width, height))

    # 4. ページごとのレイアウト構築（裏写り防止ロジック）
    for page_num in range(1, min_pages + 1):
        c.saveState()
        
        if page_num % 2 == 0:
            # 偶数ページ（左側）：タイトル、解説、塗る時のヒント（裏写り防止対策）
            c.setFont("Helvetica-Bold", 14)
            c.drawString(54, height - 72, f"Mindfulness Notes & Tips - Page {page_num}")
            c.setFont("Helvetica", 10)
            c.drawString(54, height - 100, "Use this space for color testing or personal notes.")
        else:
            # 奇数ページ（右側）：AI生成の線画イラスト配置フレーム
            c.setFont("Helvetica-Bold", 12)
            c.drawString(54, height - 54, f"Plate {page_num // 2 + 1}")
            
            # 線画イラスト用プレースホルダー枠
            c.setStrokeColor(colors.black)
            c.setLineWidth(1)
            c.rect(54, 54, width - 108, height - 140)
            
            c.setFont("Helvetica", 10)
            c.drawCentredString(width / 2, height / 2, "[ AI Line Art Illustration Frame ]")

        c.showPage()
        c.restoreState()

    c.save()
    print(f"✅ 内装PDFの生成が完了しました: {pdf_path}")

if __name__ == "__main__":
    generate_interior_pdf()

