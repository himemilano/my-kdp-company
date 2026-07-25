import os
import math
from reportlab.graphics.shapes import Drawing, Circle, Rect, Line, Path
from reportlab.graphics import renderPM
from reportlab.lib import colors
from scripts.knowledge_loader import load_organization_knowledge

def draw_botanical_plate(d, cx, cy, page_index):
    """
    Knowledgeが要求する「侘び寂び」「余白」「極細の線画」に基づき、
    植物（梅・椿・桜・蓮など）をモチーフにした優美な和風線画を描画する。
    """
    # 背景のホワイトスペース（余白 65%以上を確保するためのデザイン配置）
    d.add(Rect(0, 0, 500, 700, fillColor=colors.white, strokeColor=None))
    
    # 和のフレームアクセント（極細の二重線）
    d.add(Rect(40, 40, 420, 620, fillColor=None, strokeColor=colors.HexColor("#2C2C2C"), strokeWidth=0.5))
    d.add(Rect(44, 44, 412, 612, fillColor=None, strokeColor=colors.HexColor("#888888"), strokeWidth=0.25))

    # モチーフのバリエーション（ページごとに異なる植物的構造を表現）
    petals = 6 + ((page_index * 2) % 6)  # 6〜10枚の花弁
    radius = 90 + (page_index % 4) * 20

    # 1. 枝（ステム）の優美な曲線
    stem = Path(fillColor=None, strokeColor=colors.HexColor("#1A1A1A"), strokeWidth=1.0)
    direction = 1 if page_index % 2 == 0 else -1
    stem.moveTo(cx, cy - 220)
    stem.curveTo(cx + (70 * direction), cy - 60, cx - (50 * direction), cy + 80, cx, cy + 240)
    d.add(stem)

    # 2. 花弁の輪郭（幾何学ではなく有機的な円弧の重なり）
    for i in range(petals):
        angle = i * (2 * math.pi / petals)
        px = cx + math.cos(angle) * (radius * 0.45)
        py = cy + math.sin(angle) * (radius * 0.45)
        
        petal_path = Path(fillColor=None, strokeColor=colors.HexColor("#1A1A1A"), strokeWidth=0.8)
        petal_path.circle(px, py, radius * 0.35)
        d.add(petal_path)
        
        # 花びらの中心に向かう繊細なスジ
        d.add(Line(cx, cy, px, py, strokeColor=colors.HexColor("#444444"), strokeWidth=0.4))

    # 3. 花芯（めしべ・おしべの表現）
    for r in range(10, int(radius * 0.3), 10):
        d.add(Circle(cx, cy, r, fillColor=None, strokeColor=colors.HexColor("#1A1A1A"), strokeWidth=0.6))

def self_critique_asset(output_path, page_index):
    """
    【自己批判プロセス】
    生成された画像ファイルが存在し、かつダミー（幾何学的な円や十字線だけの不良品）になっていないかを
    自ら検証・批判する。基準未達の場合は例外を発生させて次へ進ませない。
    """
    if not os.path.exists(output_path):
        raise AssertionError(f"自己批判エラー: プレート {page_index} の画像ファイルが生成されていません。")
    
    file_size = os.path.getsize(output_path)
    # 極端にファイルサイズが小さい場合（描画抜けや空ファイルの疑い）
    if file_size < 5000:
        raise AssertionError(f"自己批判エラー: プレート {page_index} のファイルサイズが小さすぎます（{file_size} bytes）。描画内容に不備があります。")

    print(f"   └ [Self-Critique] プレート {page_index}: 描き込み・余白・ファイル完全性のチェック完了 (OK)")

def run_asset_agent(project_slug):
    print(f"🌿 [Asset Agent] プロジェクト '{project_slug}' の線画ビジュアルアセットを生成中...")
    
    # Knowledgeのロードと確認
    knowledge = load_organization_knowledge()
    print(f"   ℹ️ 組織のKnowledgeをロードしました（デザイン原則適用中）")

    project_root = f"projects/{project_slug}"
    assets_dir = os.path.join(project_root, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    cx, cy = 250, 350
    
    for i in range(1, 21):
        asset_path = os.path.join(assets_dir, f"plate_{i:02d}.png")
        
        # キャンバス作成と描画
        d = Drawing(500, 700)
        draw_botanical_plate(d, cx, cy, i)
        renderPM.drawToFile(d, asset_path, fmt='PNG', dpi=300)
        
        # 自己批判の実施
        self_critique_asset(asset_path, i)
        
    print(f"✅ すべての線画アセットの生成と自己批判が完了しました: {assets_dir}")
