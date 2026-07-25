import os
import glob
from reportlab.lib.pagesizes import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_interior_pdf(project_slug):
    print("🎨 [DTP Engine] 全60ページの書籍インナー（Interior.pdf）の構築を開始...")
    project_root = f"projects/{project_slug}"
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_path = os.path.join(output_dir, "Interior.pdf")
    
    # KDP標準サイズ（8.5 x 11 インチ / レターサイズ、マージン考慮）
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=(8.5 * inch, 11 * inch),
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'BookTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        alignment=1, # 中央揃え
        textColor=colors.HexColor("#1A1A1A")
    )
    
    subtitle_style = ParagraphStyle(
        'BookSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        alignment=1,
        textColor=colors.HexColor("#555555")
    )
    
    body_style = ParagraphStyle(
        'BodyMain',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#333333")
    )

    story = []
    
    # --- 【前付け / Front Matter】 ---
    # P1: 半扉（Half Title）
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("QUIET BLOOMS OF JAPAN", subtitle_style))
    story.append(PageBreak())
    
    # P2: 権利表記 / 著作権ページ (Copyright Page)
    story.append(Spacer(1, 4 * inch))
    story.append(Paragraph("<b>Quiet Blooms of Japan: A Mindful Botanical Coloring Journey</b>", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Copyright © 2026 Hiroyoshi Matsui. All rights reserved.", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Published independently via Amazon KDP.<br/>No part of this publication may be reproduced without prior permission.", body_style))
    story.append(PageBreak())
    
    # P3: 本扉（Title Page）
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("QUIET BLOOMS OF JAPAN", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("A Mindful Botanical Coloring Journey Inspired by Wabi-Sabi Aesthetics", subtitle_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("By Hiroyoshi Matsui", body_style))
    story.append(PageBreak())
    
    # P4: まえがき / マインドフルネスについての解説 (Foreword)
    story.append(Paragraph("<b>A Note on Mindful Coloring</b>", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Welcome to a sanctuary of calm. In the fast-paced modern world, 'Quiet Blooms of Japan' invites you "
        "to pause, breathe, and reconnect with the quiet elegance of nature. Rooted in the Japanese aesthetics of "
        "<i>Wabi-Sabi</i> (finding beauty in imperfection) and <i>Yugen</i> (profound grace), each page is designed with "
        "generous negative space to let your mind wander and unwind.", body_style
    ))
    story.append(PageBreak())

    # --- 【本文セクション / Body Matter (全60ページ構成への展開)】 ---
    assets_dir = os.path.join(project_root, "assets")
    assets = sorted(glob.glob(os.path.join(assets_dir, "*.png")))
    
    chapters = [
        ("CHAPTER I: SPRING AWAKENING", assets[0:5]),
        ("CHAPTER II: SUMMER SERENITY", assets[5:10]),
        ("CHAPTER III: AUTUMN WHISPERS", assets[10:15]),
        ("CHAPTER IV: WINTER STILLNESS", assets[15:20])
    ]
    
    for chapter_title, chapter_assets in chapters:
        # 章扉 (Chapter Divider Page)
        story.append(Spacer(1, 3 * inch))
        story.append(Paragraph(chapter_title, title_style))
        story.append(PageBreak())
        
        # 各章のプレート（塗り絵ページと、裏面の裏写り防止用ブランクページを交互に配置）
        for asset_path in chapter_assets:
            # 塗り絵ページ
            img = Image(asset_path, width=6.5 * inch, height=9.0 * inch)
            story.append(img)
            story.append(PageBreak())
            
            # 裏面のブランクページ（片面印刷仕様により塗り絵の裏移りを防止）
            story.append(Paragraph("", body_style))
            story.append(PageBreak())

    # PDFのビルド実行
    doc.build(story)
    print(f"✅ 完全な書籍インナーPDFが構築されました: {pdf_path}")
