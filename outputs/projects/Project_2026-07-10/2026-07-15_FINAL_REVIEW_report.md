**リーガル＆クオリティ通過の承認ログ**

提出された「本日分のプロンプト初稿：高品質画像生成用プロンプトテンプレートと設計ガイドライン」について、著作権、商標権、パブリシティ権、肖像権、および公序良俗の観点から厳格な検閲を実施いたしました。

プロンプトテンプレート自体は汎用的な構成であり、直接的な法的リスクを内包するものではありません。また、ネガティブプロンプトに`watermark, signature, text`が含まれている点は、意図しない知的財産権表示の混入を防ぐ上で非常に有効です。

しかしながら、プロンプト設計ガイドラインにおいて、AI生成画像の特性上、意図せず法的リスクを招く可能性のある記述（特に「参考事例」におけるスタイル模倣の示唆）が見受けられました。このため、チームが安全かつ倫理的にコンテンツを制作できるよう、**法的・倫理的リスクに関する厳守事項**を追記し、ガイドラインを強化いたしました。

これにより、本プロンプトテンプレートおよびガイドラインは、リーガル＆クオリティ基準を満たし、承認いたします。

---

PM殿の指示書を拝読いたしました。プロジェクト『Project_2026-07-10』の基盤確立フェーズにおいて、現時点では具体的な画像コンテンツの内容やデザインコンセプトが未確定であると理解しております。

しかしながら、「本日分の画像生成用英語プロンプトの高品質な呪文を設計してください」というご指示に対し、情報が揃い次第、即座に最高品質の画像を生成できるよう、**現段階で可能な限り汎用性が高く、かつ具体的な情報が入力された際に最大限の効果を発揮する「プロンプトの骨格（テンプレート）」と、その「設計ガイドライン」**を本日分の初稿として提出いたします。

この初稿では、ご指示いただいた『8.625 x 11.25 inch vertical layout with bleed, 300 DPI print-ready resolution』の厳格な技術要件と、余白の美（ミニマリズム）が担保されるよう、ミリ単位でのアスペクト比の調整と、デザインコンセプトへの具体的な組み込みを行いました。これにより、PM殿からの「キービジュアル/デザインコンセプトの方向性検討」の結果、および「具体的なページごとのコンテンツ制作指示」が出た際に、迅速かつ正確にプロンプトを構築できる状態を整えます。

---

### **本日分のプロンプト初稿：高品質画像生成用プロンプトテンプレートと設計ガイドライン**

#### **1. 高品質画像生成用英語プロンプトテンプレート**

以下のテンプレートは、あらゆる種類の画像生成に対応できるよう設計されており、特に「塗り絵の極細線」や「絵本のタッチ」といった具体的なスタイル指定を組み込むことを想定しています。`[ ]` 内のプレースホルダーに、PM殿からの指示に基づいた具体的な情報を入力することで、高品質なプロンプトが完成します。

```english
[Core Style: e.g., Ultra-fine line art for coloring book, intricate details, clean lines, black and white, no shading, OR Children's storybook illustration style, whimsical, soft colors, gentle textures, hand-drawn feel, warm lighting]
[Subject: e.g., A curious young girl, A majestic ancient tree, A futuristic city landscape]
[Action/Situation: e.g., exploring a magical forest, standing proudly on a hill, bustling with flying vehicles]
[Background/Environment: e.g., lush enchanted forest with glowing flora, a serene mountain vista at dawn, a vibrant cyberpunk street at night]
[Mood/Emotion: e.g., peaceful and adventurous, awe-inspiring and majestic, energetic and mysterious]
[Color Palette/Lighting: e.g., warm pastel tones, vibrant primary colors, soft natural light, dramatic backlighting, high contrast, monochromatic blue]
[Composition/Camera Angle: e.g., full shot, close-up, eye-level, wide angle, dynamic angle, isometric view]
--ar 23:30 (Strictly for 8.625 x 11.25 inch vertical layout with bleed)
--v [Model Version: e.g., 5.2, 6.0]
--style raw (Optional: for more literal interpretation)
--s [Stylize Value: e.g., 750, 250 - adjust for artistic freedom vs. prompt adherence]
--q [Quality Value: e.g., 2, 1 - adjust for rendering quality vs. speed]
```

**ネガティブプロンプト (Negative Prompt):**
以下のネガティブプロンプトは、一般的に生成される画像の品質を低下させる要素や、意図しない要素を除外するために常に含めることを推奨します。

```english
blurry, low resolution, deformed, bad anatomy, ugly, tiling, poorly drawn hands, poorly drawn feet, out of frame, extra limbs, disfigured, mutation, missing limbs, watermark, signature, text, error, cropped, jpeg artifacts, duplicate, monochrome, grayscale, realistic, photo, 3D render, bad art, poorly drawn, disfigured, out of frame, ugly, tiling, poorly drawn hands, poorly drawn feet, out of frame, extra limbs, disfigured, mutation, missing limbs, watermark, signature, text, error, cropped, jpeg artifacts, duplicate
```

#### **2. プロンプト設計ガイドライン**

PM殿からの指示書にある「キービジュアル/デザインコンセプトの方向性検討」の各項目が、上記のプロンプトテンプレートのどの部分に影響し、どのように具体化されるかを説明します。

1.  **キーワード（コンテンツの雰囲気や印象）:**
    *   **影響箇所:** `[Core Style]`, `[Mood/Emotion]`, `[Color Palette/Lighting]`
    *   **具体例:**
        *   「先進的」→ `[Core Style]` に "futuristic, sleek, minimalist"、`[Color Palette]` に "cool metallic tones, neon accents"
        *   「親しみやすい」→ `[Core Style]` に "friendly, approachable, cartoonish"、`[Mood/Emotion]` に "warm, inviting"
        *   「専門的」→ `[Core Style]` に "detailed, precise, technical illustration"、`[Color Palette]` に "muted, professional colors"
    *   **「塗り絵の極細線」「絵本のタッチ」の指定方法:**
        *   **塗り絵の極細線:** `Ultra-fine line art for coloring book, intricate details, clean lines, black and white, no shading, vector art style`
        *   **絵本のタッチ:** `Children's storybook illustration style, whimsical, soft colors, gentle textures, hand-drawn feel, warm lighting, watercolor effect`

2.  **参考事例（既存のデジタルコンテンツやWebサイトのURL）:**
    *   **影響箇所:** `[Core Style]`, `[Color Palette/Lighting]`, `[Composition/Camera Angle]`
    *   **具体例:** 参考事例のデザイン要素（色使い、イラストのスタイル、写真のトーン、レイアウトの雰囲気など）を分析し、それを表現するキーワードを抽出してプロンプトに落とし込みます。ただし、**特定の既存著作物（キャラクター、ロゴ、具体的な構図など）や、著名なブランド、製品名を直接プロンプトに含めることは厳禁とします。あくまで、そのデザインが持つ「雰囲気」や「一般的なスタイル」を抽象的なキーワードで表現することに留めてください。**

3.  **カラーパレット（案）:**
    *   **影響箇所:** `[Color Palette/Lighting]`
    *   **具体例:**
        *   メインカラー、サブカラー、アクセントカラーの具体的な色名やトーン（例: "deep ocean blue, soft coral pink, golden yellow accents"）を記述します。
        *   光の表現（例: "bright daylight, soft diffused light, dramatic chiaroscuro"）もここで指定します。

#### **3. 厳格な技術要件の遵守 (Strict Adherence to Technical Requirements)**

*   **出力サイズと解像度:**
    *   すべての画像は、**8.625 x 11.25 inch (縦長) のレイアウト**に厳密に適合するよう、アスペクト比 `--ar 23:30` を使用して生成されます。
    *   **300 DPIの印刷対応解像度**を確保するため、生成された画像は最終的に高解像度でエクスポートされ、必要に応じてアップスケーリング処理を行います。これはプロンプトの `--q` (Quality Value) 設定と、後工程での高解像度化ツールによって担保されます。
*   **裁ち落とし (Bleed) の考慮:**
    *   `--ar 23:30` で生成される画像は、裁ち落とし領域を含んだサイズとして扱います。デザイン要素（特に背景や装飾）は、裁ち落としを考慮して画像の端まで配置されるようにプロンプトで指示し、重要な要素（テキストや主要な被写体）は安全領域内に収まるように意識します。
*   **余白の美（ミニマリズム）の担保:**
    *   PM殿からの「キーワード」や「参考事例」において「ミニマル」「クリーン」「余白を活かした」といった指示があった場合、以下のプロンプト要素を積極的に活用します。
        *   `[Core Style]` に `minimalist design, clean aesthetic, ample negative space, sophisticated simplicity`
        *   `[Background/Environment]` に `clean, uncluttered background, subtle textures, solid color background`
        *   `[Composition/Camera Angle]` に `centered composition, ample white space around the subject, minimalist layout, sparse elements`
    *   これにより、視覚的なノイズを排除し、コンテンツの主要メッセージが際立つような、洗練されたレイアウトを追求します。

#### **4. 法的・倫理的リスクに関する厳守事項 (Strict Adherence to Legal and Ethical Guidelines)**

本プロンプトテンプレートおよびガイドラインを用いて生成される画像は、以下の事項を厳守すること。

*   **著作権・商標権の侵害の禁止:**
    *   特定の既存著作物（キャラクター、ロゴ、具体的な構図、著名なイラストレーターの極めて特徴的なスタイルなど）を直接プロンプトに含めたり、既存の著作物や商標に酷似する画像を生成するような指示は厳禁とする。
    *   あくまで、参考事例から抽出するデザイン要素は、その「雰囲気」や「一般的なスタイル」を抽象的なキーワードで表現することに留めること。
    *   特定のブランド名、製品名、企業名、またはそれらを想起させる固有名詞をプロンプトに直接含めることは禁止する。
    *   ネガティブプロンプトの `watermark, signature, text` は常に含め、意図しない著作権表示や商標の混入を防ぐこと。

*   **パブリシティ権・肖像権の侵害の禁止:**
    *   実在の人物や著名人を想起させるような描写、または特定の個人を特定できるような特徴（顔、服装など）をプロンプトに含めることは厳禁とする。

*   **公序良俗・倫理規定の遵守:**
    *   いかなる場合においても、公序良俗に反する内容、差別的な内容、暴力的な内容、性的な内容、または違法な内容を含んではならない。
    *   他者の名誉を毀損する、プライバシーを侵害する、または不快感を与える可能性のあるコンテンツの生成は厳禁とする。

**今後の進め方:**

PM殿からの「プロジェクト概要の再確認とドキュメント化」および「コンテンツ構造（目次・構成案）の作成と提出」が完了し、特に「キービジュアル/デザインコンセプトの方向性検討」において具体的なキーワード、参考事例、カラーパレットの方向性が決定され次第、このテンプレートとガイドラインを用いて、各ページやセクションに最適な高品質な画像生成プロンプトを設計いたします。

情報が揃い次第、迅速に次のフェーズへ移行できるよう、準備を整えております。