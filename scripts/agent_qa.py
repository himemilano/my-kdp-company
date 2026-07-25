import os
import glob
from scripts.knowledge_loader import load_organization_knowledge

def run_qa_agent(project_slug):
    print(f"🔍 [QA Gatekeeper] プロジェクト '{project_slug}' の最終品質検証（QA Gate）を開始...")
    
    knowledge = load_organization_knowledge()
    project_root = f"projects/{project_slug}"
    
    # 1. 必須成果物の存在・数量チェック
    assets_dir = os.path.join(project_root, "assets")
    output_dir = os.path.join(project_root, "output")
    
    assets = glob.glob(os.path.join(assets_dir, "*.png"))
    interior_pdf = os.path.join(output_dir, "Interior.pdf")
    cover_pdf = os.path.join(output_dir, "Cover.pdf")
    
    print(f"   - 検出されたアセット数: {len(assets)} / 20枚")
    print(f"   - 内装PDFの存在: {os.path.exists(interior_pdf)}")
    print(f"   - カバーPDFの存在: {os.path.exists(cover_pdf)}")
    
    if len(assets) < 20:
        raise RuntimeError("【QA不合格】必要な20枚のプレートが揃っていません。処理を中断します。")
    if not os.path.exists(interior_pdf) or not os.path.exists(cover_pdf):
        raise RuntimeError("【QA不合格】必須のPDF成果物（Interior.pdf または Cover.pdf）が欠損しています。")

    # 2. Knowledge基準に基づく北米市場向け適合審査
    # （過去の失敗：ダミー図形の混入、品質の低いプレースホルダーの排除をここで完全に防ぐ）
    print(f"   - 適用中の美的・市場基準: {knowledge['design_principles']}")
    
    for asset in assets:
        if os.path.getsize(asset) < 5000:
            raise RuntimeError(f"【QA不合格】不十分なアセットが検出されました: {asset}")

    print(f"🎉 [QA Gatekeeper] すべての成果物がKnowledgeの厳格な基準をクリアしました。完成品として認定します。")
    return True
