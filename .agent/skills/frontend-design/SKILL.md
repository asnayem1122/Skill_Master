---
name: frontend-design
description: >-
  Distinctive, agency-grade frontend visual design and anti-slop aesthetic direction synthesized from Impeccable and Taste (247-site gallery study). Grounds UI in subject matter, infers brief tone, eliminates AI clichés, directs typography, bento layouts, haptic micro-interactions, fluid spring motion, and provides command verbs (shape, critique, polish, bolder, quieter, distill, harden, onboard) across 4 surface modes (Persuade, Operate, Read, Experience).
---

# Frontend Design & Visual Direction

Engineers distinctive, agency-caliber digital experiences ($150k+ studio tier). Synthesizes the art direction principles of **Taste** (distilled from 247 award-winning gallery sites) and the surface execution playbooks of **Impeccable**. Rejects generic AI clichés, purple mesh gradients, and cookie-cutter component cards. Enforces intentional typography, subject-grounded palettes, asymmetrical bento layouts, machined double-bezel surfaces, haptic micro-interactions, and fluid spring physics.

---

## 1. Step 0: The Design Read & Mode Selection

Before writing markup or selecting colors, **read the room**:

1. **Surface Mode Selection**: Determine what visitor success looks like (see [references/design-modes.md](references/design-modes.md)):
   - **Persuade**: Landing pages, marketing, campaigns. High ambition, bold typography, authentic imagery, strong POV.
   - **Operate**: App dashboards, tools, admin, settings. Scanability, native affordances, quiet borders, zero vanity metrics.
   - **Read**: Documentation, changelogs, articles. High legibility, 45–75 char lines, effortless comprehension.
   - **Experience**: Portfolios, showcases, galleries. The artifact leads; interface chrome recedes.

2. **The 3 Aesthetic Dials**:
   - `DESIGN_VARIANCE: 1-10` (1 = Strict Symmetry $\leftrightarrow$ 10 = Artsy Chaos)
   - `MOTION_INTENSITY: 1-10` (1 = Static $\leftrightarrow$ 10 = Cinematic Spring Physics)
   - `VISUAL_DENSITY: 1-10` (1 = Airy Luxury Gallery $\leftrightarrow$ 10 = High-Density Cockpit)

3. **Declare the Design Read**:
   > *"Reading this as: [Page Type] in [Mode] mode for [Audience], with [Tone] vibe, Variance: [X], Motion: [Y], Density: [Z]."*

---

## 2. The Anti-Slop House Rules (Taste 247-Site Standards)

Every interface generated must strictly adhere to the Anti-Slop standards (see [references/anti-slop-rules.md](references/anti-slop-rules.md)):

- ❌ **No Multi-Line Headline Bloat**: Headlines must fit within **2 lines or fewer** at all viewports (desktop, tablet, mobile). If 3+ lines wrap, cut words first, widen container second, adjust font size last.
- ❌ **No Eyebrow Chips**: Eliminate floating pill tags (`New · v2.0`) sitting above headers. Fold vital context into the headline or supporting sentence.
- ❌ **No Monospace Outside Code**: Never use monospace fonts for subtitles, labels, or card tags. Use tabular figures (`tabular-nums`) only for numerical alignment.
- ❌ **No Index Numbering**: Never slap `01 / 02 / 03` or `(001)` on feature cards. Show progression via spatial rhythm or semantic `<ol>`.
- ❌ **No Hairline Blueprint Grids**: Never drape 1px crosshairs, blueprint lines, or decorative grid boxes across the page. Boundaries are formed by whitespace and tonal shifts.
- ❌ **No Background Gradients or Glowing Cards**: No purple radial mesh gradients; no glowing box shadows. Surfaces separate by subtle tonal steps (`bg-black/5` to `bg-black/10`). Shadows are reserved exclusively for floating dialogs and dropdown menus.
- ❌ **No Cliché Assistant Palettes**: Reject generic yellow-cream grounds with terracotta/rust accents, or violet-on-dark-gray. Palettes must be derived from the subject's authentic materials, physical surroundings, or brand truth.
- ❌ **No Identical 3-Card Rows**: Avoid three identical cards with icons in colored rounded squares. Use asymmetrical Bento grids or staggered editorial splits.
- ❌ **Two Typefaces Maximum**: One display face (high-contrast serif or geometric grotesque) and one text face (or a single variable family across both).

---

## 3. Impeccable Action Verbs & Command Playbooks

When asked to refine, review, or shape an interface, invoke the specific command playbook:

| Action Verb | Intent & Execution Strategy |
| :--- | :--- |
| `shape` | **Plan UX/UI Before Code**: Map user journey, section hierarchy, and content claims before writing markup. |
| `critique` | **Heuristic UX Review**: Audit visual hierarchy, contrast ratios, cognitive load, and touch targets. |
| `polish` | **Final Quality Pass**: Align paddings to an 8pt grid, tighten typography leading, and smooth edge transitions. |
| `bolder` | **Amplify Timid UI**: Increase display headline scale, boost color saturation, and sharpen layout contrast. |
| `quieter` | **De-escalate Overstimulating UI**: Remove competing badges, soften high-contrast borders, and introduce breathing room. |
| `distill` | **Ruthless Simplification**: Strip redundant secondary text, remove nested containers, and collapse unnecessary steps. |
| `harden` | **Production Resilience**: Handle empty states, loading skeletons, error boundaries, truncation, and i18n overflow. |
| `onboard` | **First-Run Activation**: Design memorable empty states, interactive walkthroughs, and clear primary calls to action. |
| `typeset` | **Typography Mastery**: Calibrate optical tracking (`-0.02em` on display), leading (`0.95–1.1`), and font pairing. |
| `layout` | **Spatial Architecture**: Implement asymmetrical Bento grids (`col-span-8` + `col-span-4`) with clean mobile fallbacks. |

---

## 4. Haptic Micro-Aesthetics & Surfaces

### 1. The Machined Double-Bezel
Never drop a flat card onto a canvas. Treat surfaces like glass panels enclosed in machined aluminum:
- **Outer Frame**: Container with subtle tonal tint (`bg-black/[0.03] dark:bg-white/[0.05]`), hairline ring (`ring-1 ring-black/5 dark:ring-white/10`), generous padding (`p-2`), and outer radius (`rounded-[2rem]`).
- **Inner Panel**: Child element with solid surface, subtle inner specular highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), and calculated concentric inner radius (`rounded-[calc(2rem-0.5rem)]`).

### 2. Nested "Island" Action Buttons
- Primary buttons should be pill-shaped (`rounded-full px-6 py-3`).
- Trailing icons (`↗`) must never float bare next to text: nest them inside an inner circular badge (`w-8 h-8 rounded-full bg-black/5 dark:bg-white/10 flex items-center justify-center`).

### 3. Fluid Spring Motion Physics
Avoid robotic `linear` or standard `ease-in-out` transitions:
```css
/* Authentic physical mass and spring deceleration */
transition-all duration-700 ease-[cubic-bezier(0.32,0.72,0,1)]
```
- Respect user preferences: Always wrap non-essential motion in `@media (prefers-reduced-motion: reduce)`.

---

## 5. Authentic Content & Imagery Protocol

- **Never Use Placeholder Slop**: Avoid lorem ipsum numbers ("+1,234%") and generic AI robot illustrations.
- **Real Archival Collections**: Search open archives (Wikimedia Commons, The Met, Art Institute of Chicago, Openverse) for authentic engravings, maps, and photography.
- **Code-Drawn Artifacts**: When photography is unavailable, render authentic interface fragments using HTML/CSS tagged with `data-ui`.

---

## 6. Real-Browser Verification Gate

Before declaring any UI task complete, inspect the rendered output across 3 responsive breakpoints:
1. **Desktop (1440px)**: Verify poster-like fullness, equal outer margins, and balanced negative space.
2. **Tablet (768px)**: Verify Bento grid collapses gracefully to 2 columns with preserved visual rhythm.
3. **Mobile (390px)**: Verify single-column linear flow, touch targets $\ge 44\text{px}$, and zero horizontal scroll overflow.
