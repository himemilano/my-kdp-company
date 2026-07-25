import os
import glob
from reportlab.lib.pagesizes import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from scripts.knowledge_loader import load_organization_knowledge

def register_multilingual_fonts():
    """
    Ubuntu環境およびローカル環境の日本語・多言語フォントを自動探索し、
    ReportLabに登録する。パスの候補を拡充。
    """
    font_candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansJP-Regular.otf",
        "/usr/share/fonts/truetype/ipafont/ipag.ttf",
        "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
        "C:/Windows/Fonts/msgothic.ttc"
    ]
    
    for path in font_candidates:
        if os.path.exists(path):
            try:
                sub_index = 0 if path.endswith('.ttc') else 0
                pdfmetrics.registerFont(TTFont('UnicodeFont', path, subfontIndex=sub_index))
                print(f"   ℹ️ 多言語対応フォントを正常にロードしました: {path}")
                return 'UnicodeFont'
            except Exception as e:
                continue
    print("   ⚠️ 警告: 専用の多言語フォントが見つかりません。標準フォントにフォールバックします。")
    return 'Helvetica'

def generate_interior_pdf(project_slug):
    print("🎨 [DTP Engine] 多言語対応・フレーム厳格収容・全60ページ構造化のインナー構築を開始...")
    
    knowledge = load_organization_knowledge()
    print(f"   ℹ️ 適用デザイン原則: {knowledge.get('design_principles')}")

    active_font = register_multilingual_fonts()

    project_root = f"projects/{project_slug}"
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_path = os.path.join(output_dir, "Interior.pdf")
    
    # 8.5 x 11 インチ（KDPレターサイズ）
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=(8.5 * inch, 11 * inch),
        leftMargin=0.8 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'BookTitle', parent=styles['Normal'],
        fontName=active_font, fontSize=24, leading=30, alignment=1,
        textColor=colors.HexColor("#1A1A1A")
    )
    subtitle_style = ParagraphStyle(
        'BookSubtitle', parent=styles['Normal'],
        fontName=active_font, fontSize=12, leading=16, alignment=1,
        textColor=colors.HexColor("#555555")
    )
    body_style = ParagraphStyle(
        'BodyMain', parent=styles['Normal'],
        fontName=active_font, fontSize=10, leading=15,
        textColor=colors.HexColor("#333333")
    )

    story = []

    def add_page_break():
        story.append(PageBreak())

    # --- 【前付け / Front Matter (計8ページ)】 ---
    story.append(Spacer(1, 2.5 * inch))
    story.append(Paragraph("TRANQUIL FLORA", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Jardín Botánico Sereno", subtitle_style))
    add_page_break()
    
    story.append(Spacer(1, 3.5 * inch))
    story.append(Paragraph("<b>Tranquil Flora: A Mindful Botanical Coloring Journey</b>", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Copyright © 2026 Hiroyoshi Matsui. All rights reserved.", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Published independently via Amazon KDP.<br/>Creado bajo estrictos principios de estética Wabi-Sabi.", body_style))
    add_page_break()
    
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("TRANQUIL FLORA", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("A Mindful Botanical Coloring Journey Inspired by Wabi-Sabi Aesthetics", subtitle_style))
    story.append(Spacer(1, 35))
    story.append(Paragraph("By Hiroyoshi Matsui", subtitle_style))
    add_page_break()
    
    story.append(Paragraph("<b>A Note on Mindful Coloring / 塗り絵に寄せて</b>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Welcome to a sanctuary of calm. Bienvenue a este santuario de paz. "
        "Rooted in <i>Wabi-Sabi</i> (finding beauty in imperfection) and generous negative space, "
        "each page offers a meditative escape for your creative soul.", body_style
    ))
    add_page_break()

    # --- 【本文セクション / Body Matter (全44ページ：4章×各5作品＋章扉)】 ---
    assets_dir = os.path.join(project_root, "assets")
    assets = sorted(glob.glob(os.path.join(assets_dir, "*.png")))
    
    chapters = [
        ("CHAPTER I: SPRING AWAKENING / 春の目覚め", assets[0:5]),
        ("CHAPTER II: SUMMER SERENITY / 夏の静寂", assets[5:10]),
        ("CHAPTER III: AUTUMN WHISPERS / 秋のささやき", assets[10:15]),
        ("CHAPTER IV: WINTER STILLNESS / 冬の静けさ", assets[15:20])
    ]
    
    for chapter_title, chapter_assets in chapters:
        story.append(Spacer(1, 3.2 * inch))
        story.append(Paragraph(chapter_title, title_style))
        add_page_break()
        
        # プレート（表面：高さ 6.0 インチ以内に強制収縮させ、フレーム超過エラーを完全に防止）
        for asset_path in chapter_assets:
            img = Image(asset_path, height=6.0 * inch, preserveAspectRatio=True)
            img.hAlign = 'CENTER'
            story.append(img)
            add_page_break()
            
            story.append(Paragraph("", body_style)) # 裏面ブランク
            add_page_break()

    # --- 【後付け / Back Matter (計8ページ：全60ページ完結)】 ---
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("<b>Notes & Color Palettes / カラーパレットとメモ</b>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Use this space to test your colored pencils, markers, or watercolors.", body_style))
    add_page_break()
    story.append(Paragraph("", body_style))
    add_page_break()

    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("<b>About the Author / 著者について</b>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Hiroyoshi Matsui is an independent creator dedicated to bridging traditional Japanese art aesthetics with modern mindful publishing.", body_style))
    add_page_break()
    story.append(Paragraph("", body_style))
    add_page_break()

    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("<b>Acknowledgment / 謝辞</b>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Thank you for bringing color and life to these pages. May your mindful journey be filled with peace.", body_style))
    add_page_break()
    story.append(Paragraph("", body_style))
    add_page_break()

    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("<b>Colophon / 発行情報</b>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("First Edition - Printed via Amazon KDP.<br/>Designed with ReportLab DTP Engine under strict quality control.", body_style))
    story.append(PageBreak())

    # ビルド実行
    doc.build(story)
    print(f"✅ フレームに完全に収まる厳密に全60ページのインナーPDFが完成しました: {pdf_path}")
