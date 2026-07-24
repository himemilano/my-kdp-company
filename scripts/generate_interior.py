import os
import yaml
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class KDPPrintedCanvas(canvas.Canvas):
    """KDPの厳格なページ番号・裁ち落としルールを適用するカスタムキャンバス"""
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
        
        # 裁ち落とし領域を考慮した安全な位置にページ番号を配置
        page_text = f"{self._pageNumber}"
        width_pt = 8.5 * 72 + 18 # 裁ち落とし込みの幅
        
        if self._pageNumber % 2 == 0:
            # 偶数ページ（左側）：左側に寄せる
            self.drawString(54, 36, page_text)
        else:
            # 奇数ページ（右側）：右側に寄せる
            self.drawRightString(width_pt - 54, 36, page_text)
            
        self.restoreState()

def generate_interior_pdf():
    print("🎨 [KDP出版部] 厳格仕様・内装PDFレイアウトエンジン起動中...")

    # 1. 設定ファイルの読み込み
    if os.path.exists("config.yml"):
        with open("config.yml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    genre = config.get("genre_layouts", {}).get("coloring_book", {})
    min_pages = genre.get("min_pages", 24)

    # 2. ワークスペースの特定
    if os.path.exists("active_project.json"):
        import json
        with open("active_project.json", "r", encoding="utf-8") as f:
            project_info = json.load(f)
        workspace_dir = os.path.join(project_info["project_root"], "kdp_workspace")
    else:
        workspace_dir = "kdp_workspace"

    os.makedirs(workspace_dir, exist_ok=True)
    pdf_path = os.path.join(workspace_dir, "interior_output.pdf")

    # 3. KDP裁ち落とし（Bleed）を含む厳密な寸法計算
    # 仕上がりサイズ: 8.5 x 11 インチ
    # 裁ち落とし: 上下左右に 0.125インチ (9pt) を追加
    pt_per_inch = 72
    bleed_pt = 0.125 * pt_per_inch
    
    trim_width = 8.5 * pt_per_inch
    trim_height = 11.0 * pt_per_inch
    
    total_width = trim_width + (2 * bleed_pt)   # 630 pt
    total_height = trim_height + (2 * bleed_pt) # 810 pt

    c = KDPPrintedCanvas(pdf_path, pagesize=(total_width, total_height))

    # 4. ページごとのレイアウト構築（KDP安全マージン厳守）
    for page_num in range(1, min_pages + 1):
        c.saveState()
        
        # 裁ち落とし分のオフセットを適用
        c.translate(bleed_pt, bleed_pt)

        if page_num % 2 == 0:
            # 偶数ページ（左側 / Verso）：裏写り防止＆解説・メモスペース
            # ノド元（右側）と小口（左側）の安全マージンを確保
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(colors.HexColor("#333333"))
            c.drawString(36, trim_height - 54, f"Coloring Notes & Palette - Page {page_num}")
            
            c.setFont("Helvetica", 10)
            c.drawString(36, trim_height - 80, "Use this page for testing markers or recording color combinations.")
            
            # 安全枠（Live Area Frame）の描画
            c.setStrokeColor(colors.HexColor("#CCCCCC"))
            c.setLineWidth(0.5)
            c.rect(36, 54, trim_width - 72, trim_height - 120)
        else:
            # 奇数ページ（右側 / Recto）：AI線画イラスト用フレーム
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(colors.HexColor("#333333"))
            c.drawString(36, trim_height - 36, f"Plate {page_num // 2 + 1}")
            
            # KDPの安全領域（Safe Zone）内に収まる線画フレーム
            # はみ出しエラーを防ぐため、マージンを安全に確保
            margin = 36 # 0.5インチの安全マージン
            frame_width = trim_width - (2 * margin)
            frame_height = trim_height - 90
            
            c.setStrokeColor(colors.black)
            c.setLineWidth(1)
            c.rect(margin, 45, frame_width, frame_height)
            
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.HexColor("#666666"))
            c.drawCentredString(trim_width / 2, trim_height / 2, "[ AI Line Art Illustration Frame (Safe Zone Protected) ]")

        c.showPage()
        c.restoreState()

    c.save()
    print(f"✅ KDP完全準拠の内装PDF生成が完了しました: {pdf_path}")

if __name__ == "__main__":
    generate_interior_pdf()
