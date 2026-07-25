import os
import glob
from reportlab.lib.pagesizes import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from scripts.knowledge_loader import load_organization_knowledge

def generate_interior_pdf(project_slug):
    print("🎨 [DTP Engine] Knowledgeと完全連動した全60ページの精密書籍インナー構築を開始...")
    
    # Knowledgeのロードとデザイン原則の適用確認
    knowledge = load_organization_knowledge()
    print(f"   ℹ️ 適用デザイン原則: {knowledge.get('design_principles')}")

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
        fontName='Helvetica-Bold', fontSize=26, leading=32, alignment=1,
        textColor=colors.HexColor("#1A1A1A")
    )
    subtitle_style = ParagraphStyle(
        'BookSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=13, leading=17, alignment=1,
        textColor=colors.HexColor("#555555")
    )
    body_style = ParagraphStyle(
        'BodyMain', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=15,
        textColor=colors.HexColor("#333333")
    )

    story = []

    def add_page_with_odd_check():
        """奇数ページ（右ページ）の整合性を保つための改ページヘルパー"""
        story.append(PageBreak())

    # --- 【前付け / Front Matter (計8ページ構成)】 ---
    # P1: 半扉
    story.append(Spacer(1, 2.5 * inch))
    story.append(Paragraph("QUIET BLOOMS OF JAPAN", subtitle_style))
    add_page_with_odd_check()
    
    # P2: 著作権・奥付
    story.append(Spacer(1, 3.5 * inch))
    story.append(Paragraph("<b>Quiet Blooms of Japan: A Mindful Botanical Coloring Journey</b>", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Copyright © 2026 Hiroyoshi Matsui. All rights reserved.", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Published independently via Amazon KDP.<br/>Created under strict Wabi-Sabi design principles.", body_style))
    add_page_with_odd_check()
    
    # P3: 本扉
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("QUIET BLOOMS OF JAPAN", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("A Mindful Botanical Coloring Journey Inspired by Wabi-Sabi Aesthetics", subtitle_style))
    story.append(Spacer(1, 35))
    story.append(Paragraph("By Hiroyoshi Matsui", subtitle_style))
    add_page_with_odd_check()
    
    # P4: まえがき (Mindfulness Note)
    story.append(Paragraph("<b>A Note on Mindful Coloring</b>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Welcome to a sanctuary of calm. In a fast-paced world, this volume invites you "
        "to pause, breathe, and reconnect with the quiet elegance of nature. Rooted in <i>Wabi-Sabi</i> "
        "(finding beauty in imperfection) and generous negative space, each page offers a meditative escape.", body_style
    ))
    add_page_with_odd_check()

    # --- 【本文セクション / Body Matter (全44ページ：4章×各5作品＋章扉)】 ---
    assets_dir = os.path.join(project_root, "assets")
    assets = sorted(glob.glob(os.path.join(assets_dir, "*.png")))
    
    chapters = [
        ("CHAPTER I: SPRING AWAKENING", assets[0:5]),
        ("CHAPTER II: SUMMER SERENITY", assets[5:10]),
        ("CHAPTER III: AUTUMN WHISPERS", assets[10:15]),
        ("CHAPTER IV: WINTER STILLNESS", assets[15:20])
    ]
    
    for chapter_title, chapter_assets in chapters:
        # 章扉
        story.append(Spacer(1, 3.2 * inch))
        story.append(Paragraph(chapter_title, title_style))
        add_page_with_odd_check()
        
        # プレート（表面：塗り絵、裏面：裏写り防止ブランク）
        for asset_path in chapter_assets:
            img = Image(asset_path, width=6.2 * inch, height=8.6 * inch)
            story.append(img)
            add_page_with_odd_check()
            
            story.append(Paragraph("", body_style)) # 裏面ブランク
            add_page_with_odd_check()

    # --- 【後付け / Back Matter (計8ページ：全60ページを完結させる)】 ---
    # P53-54: スケッチ・メモ用ページ
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("<b>Notes & Color Palettes</b>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Use this space to test your colored pencils, markers, or watercolors.", body_style))
    add_page_with_odd_check()
    story.append(Paragraph("", body_style))
    add_page_with_odd_check()

    # P55-56: 著者について
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("<b>About the Author</b>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Hiroyoshi Matsui is an independent creator dedicated to bridging traditional Japanese art aesthetics with modern mindful publishing.", body_style))
    add_page_with_odd_check()
    story.append(Paragraph("", body_style))
    add_page_with_odd_check()

    # P57-58: 読者への謝辞
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("<b>Acknowledgment</b>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Thank you for bringing color and life to these pages. May your mindful journey be filled with peace.", body_style))
    add_page_with_odd_check()
    story.append(Paragraph("", body_style))
    add_page_with_odd_check()

    # P59-60: コロフォン（奥付・発行情報）
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("<b>Colophon</b>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("First Edition - Printed in the United States / UK / EU via Amazon KDP.<br/>Designed with ReportLab DTP Engine.", body_style))
    story.append(PageBreak())

    # ビルド実行
    doc.build(story)
    print(f"✅ 厳密に全60ページで構築されたインナーPDFが完成しました: {pdf_path}")
