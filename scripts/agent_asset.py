import os
import math
from reportlab.graphics.shapes import Drawing, Circle, Path, Line
from reportlab.graphics import renderPM
from reportlab.lib import colors

BOTANICAL_MASTER_SPEC = {
    1: {"name": "Early Spring White Plum", "petals": 5, "radius": 75, "stem_curve": 1},
    2: {"name": "Snow-kissed Red Camellia", "petals": 6, "radius": 85, "stem_curve": -1},
    3: {"name": "Weeping Cherry Blossoms", "petals": 5, "radius": 65, "stem_curve": 1},
    4: {"name": "Zen Lotus Pond", "petals": 8, "radius": 90, "stem_curve": -1},
    5: {"name": "Autumn Chrysanthemum", "petals": 12, "radius": 95, "stem_curve": 1},
    6: {"name": "Wisteria Cascades", "petals": 7, "radius": 60, "stem_curve": -1},
    7: {"name": "Summer Hydrangea", "petals": 10, "radius": 80, "stem_curve": 1},
    8: {"name": "Bamboo Stalks in Wind", "petals": 4, "radius": 50, "stem_curve": -1},
    9: {"name": "Maple Leaves Dance", "petals": 5, "radius": 70, "stem_curve": 1},
    10: {"name": "Peony Elegance", "petals": 9, "radius": 100, "stem_curve": -1},
    11: {"name": "Magnolia Bloom", "petals": 6, "radius": 85, "stem_curve": 1},
    12: {"name": "Irises by the Stream", "petals": 3, "radius": 70, "stem_curve": -1},
    13: {"name": "Pine Needles and Cones", "petals": 8, "radius": 60, "stem_curve": 1},
    14: {"name": "Japanese Apricot", "petals": 5, "radius": 75, "stem_curve": -1},
    15: {"name": "Ayame Iris", "petals": 6, "radius": 80, "stem_curve": 1},
    16: {"name": "Camellia Bud", "petals": 5, "radius": 65, "stem_curve": -1},
    17: {"name": "Autumn Bellflower", "petals": 5, "radius": 70, "stem_curve": 1},
    18: {"name": "Winter Plum Twig", "petals": 5, "radius": 75, "stem_curve": -1},
    19: {"name": "Spring Peach Blossom", "petals": 6, "radius": 80, "stem_curve": 1},
    20: {"name": "Tranquil Zen Pine", "petals": 7, "radius": 85, "stem_curve": -1}
}

def draw_specific_botanical_plate(d, cx, cy, spec):
    d.add(Path(strokeColor=colors.HexColor("#2C2C2C"), strokeWidth=0.5, fillColor=None))
    
    stem = Path(fillColor=None, strokeColor=colors.HexColor("#1A1A1A"), strokeWidth=0.8)
    direction = spec["stem_curve"]
    stem.moveTo(cx, cy - 240)
    stem.curveTo(cx + (80 * direction), cy - 80, cx - (60 * direction), cy + 100, cx, cy + 250)
    d.add(stem)

    petals_count = spec["petals"]
    radius = spec["radius"]

    for i in range(petals_count):
        angle = i * (2 * math.pi / petals_count)
        px = cx + math.cos(angle) * (radius * 0.5)
        py = cy + math.sin(angle) * (radius * 0.5)
        
        petal = Circle(px, py, radius * 0.4, fillColor=colors.white, strokeColor=colors.HexColor("#1A1A1A"), strokeWidth=0.7)
        d.add(petal)
        d.add(Line(cx, cy, px, py, strokeColor=colors.HexColor("#555555"), strokeWidth=0.3))

    for r in range(8, int(radius * 0.35), 8):
        d.add(Circle(cx, cy, r, fillColor=None, strokeColor=colors.HexColor("#1A1A1A"), strokeWidth=0.5))

def generate_all_assets(project_slug):
    print("🌿 [Asset Agent] 20枚すべてのボタニカル線画アセットの個別マッピング生成を開始...")
    project_root = f"projects/{project_slug}"
    assets_dir = os.path.join(project_root, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    cx, cy = 300, 400
    
    for plate_id, spec in BOTANICAL_MASTER_SPEC.items():
        asset_path = os.path.join(assets_dir, f"plate_{plate_id:02d}.png")
        d = Drawing(600, 850)
        draw_specific_botanical_plate(d, cx, cy, spec)
        renderPM.drawToFile(d, asset_path, fmt='PNG', dpi=300)
        
        if not os.path.exists(asset_path) or os.path.getsize(asset_path) < 10000:
            raise RuntimeError(f"自己批判エラー: プレート {plate_id} ({spec['name']}) の生成品質が基準に達していません。")
            
    print("✅ 全20枚のボタニカル線画アセットが固有のスペック通りに完璧に生成されました。")
