# Anti-Slop House Rules & Tells Registry

Distilled from the study of 247 curated gallery websites (Awwwards Sites of the Day, One Page Love) and agency design standards. These non-negotiable rules eliminate generic AI tells ("slop") and elevate frontend design to studio caliber ($150k+ tier).

---

## 1. The Core Anti-Slop House Rules Matrix

| Rule | Banned AI Pattern (Slop) | Mandated Solution |
| :--- | :--- | :--- |
| **Headlines: Two Lines Max** | 3-4 line wrapped paragraphs posing as headlines | Cut words. Widen the measure. Keep headline to ≤2 lines at all viewport widths (median ~32 chars / 5 words). |
| **Single Strong Title** | Untitled sections or vague "Welcome" hero | Exactly one `h1` on the first screen answering what the product/subject is in plain terms. Every section has an explicit heading. |
| **Equal Outer Margins** | Lopsided layouts where all text is crammed on the left and the right half is empty | Balance asymmetry inside the grid: if text is on the left, the right must hold a picture, list, figure, or interactive element. |
| **No Eyebrow Badges** | Floating pill chips (`New · v2.0`) above every single header | Eliminate the eyebrow. Weave necessary context into the headline or the immediate supporting sentence. |
| **No Monospace Outside Code** | Decorative monospace fonts on subtitles, dates, or metadata labels | Use the text typeface. Use tabular figures (`font-variant-numeric: tabular-nums`) only where numbers align. |
| **No Index Numbering** | Pretentious `01 / 02 / 03` or `(001)` numbering on feature cards | Show sequence through spatial rhythm, visual hierarchy, or natural semantic lists (`<ol>`). |
| **No Hairline Grids & Crosshairs** | 1px borders everywhere, sci-fi crosshairs, crop marks, and blueprint frames | Use whitespace, subtle tone steps between background surfaces, or filled shapes to define boundaries. |
| **No Background Mesh Gradients** | Purple/violet radial mesh gradients over dark gray backgrounds | Use flat, intentional background colors or authentic photography. Gradients only for subtle photo scrims under text. |
| **No Shadows on Resting Elements** | Harsh drop shadows (`rgba(0,0,0,0.3)`) and glowing card borders | Surfaces separated by subtle tonal steps. Shadows belong only on elements that truly float (menus, modal dialogs). |
| **No Assistant Palette** | Cliché "AI palette" (warm yellow cream ground with terracotta/rust accent, or violet/indigo) | Palette derived directly from the subject matter (materials, street architecture, authentic branding). |
| **No Tracked-Out Uppercase Labels** | Tiny uppercase letter-spaced labels (`SECTION TITLE`) | Sentence case at a readable size (14–16px). |
| **No Identical Icon Feature Cards** | 3 identical cards with an icon in a colored rounded square | Asymmetrical Bento grids, staggered editorial splits, or domain-specific UI fragments. |
| **No Fake Glass & Blur Panels** | `backdrop-blur-xl` over dark backgrounds on every panel | Clean solid surfaces, machined double-bezel enclosures, or purposeful floating navigation bars. |
| **No Styled Accent Words** | Randomly styling one word in a headline (italic, serif, terracotta) | One face, one color. The vocabulary carries the emphasis, not typographic costume. |
| **Two Typefaces Ceiling** | 3+ mismatched Google fonts | One family for both display and body, or at most two (e.g., editorial display serif + geometric grotesk). |

---

## 2. Real-World Imagery Protocol

Never design around missing assets or use cheesy AI stock illustrations:
1. **Order of Preference**:
   - *Client/Project Assets*: Real product UI screenshots, actual photographs.
   - *Open Archival Collections*: Search Wikimedia Commons, Openverse, The Met, and the Art Institute of Chicago for authentic historical maps, engravings, architectural photographs, and vintage illustrations.
   - *Drawn in Code*: Authentic UI fragments built with HTML/CSS (`data-ui` attributes) or custom SVGs representing physical schematics.
   - *Type and Color Alone*: When no honest picture exists, let bold typographic scale and rich flat color carry the section.
2. **The Floor for Visual Richness**:
   - A complete landing page should carry at least 4 to 8 authentic visual artifacts.
   - Every image must carry an honest caption or footer credit. Never present an archival image as the client's own product.

---

## 3. Real-Browser Inspection & Verification Gate

Inspect rendered output across 3 standard viewports:
- **Desktop (1440px)**: Check for poster-like fullness, balanced outer margins, and proper whitespace rhythm.
- **Tablet (768px)**: Verify Bento grid collapse to 2 columns and readable typographic measure.
- **Mobile (390px)**: Verify single-column flow, touch-target sizing (min 44px), thumb-accessible controls, and zero horizontal overflow.
