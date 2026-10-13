---
name: frontend-design
description: >-
  Distinctive, agency-grade frontend visual design and anti-slop aesthetic
  direction. Grounds UI in subject matter, infers brief tone, eliminates AI
  clichés, and directs typography, bento layouts, haptic micro-interactions,
  and fluid motion physics.
---

# Frontend Design & Visual Direction

Engineers distinctive, agency-caliber digital experiences ($150k+ studio tier). Rejects templated defaults, purple AI mesh gradients, and cookie-cutter component cards. Enforces intentional typography, subject-grounded palettes, asymmetrical bento layouts, haptic micro-interactions, and fluid spring motion physics.

---

## When to Use This Skill

- Designing new landing pages, marketing sites, portfolios, or key product interfaces
- Reshaping an existing interface to feel expensive, modern, and bespoke
- Setting visual direction, color palettes, typographic pairings, and layout rhythm
- Auditing UI designs to eliminate generic AI aesthetic tells ("slop")

---

## Step 0: Brief Inference & The "Design Read"

Before writing code or selecting colors, **read the room**:
1. **Identify the Core Subject & Audience**: An analytics dashboard for Wall Street traders demands starkly different density and tone than an eco-conscious luxury perfume brand.
2. **Detect Vibe & Reference Signals**: Note user cues (*"Linear-clean", "editorial", "Apple-esque", "Awwwards-experimental", "brutalist"*).
3. **Declare the One-Line Design Read**:
   > *"Reading this as: [Page Type] for [Audience], with a [Vibe] aesthetic, leaning toward [Aesthetic Archetype]."*

### The Anti-Default Ban List (Strict Anti-Patterns)
If generated designs contain these, they read as generic AI slop:
- ❌ **Banned Defaults**: Purple radial mesh gradients over dark gray; Inter/Roboto default fonts; 3 identical equal-width feature cards; harsh `rgba(0,0,0,0.3)` drop shadows.
- ❌ **Banned AI Tells**: Tracked-out ALL CAPS eyebrows over every headline; `WORD — fragment` em-dash headers; naked `→` arrows on every button; accenting a random single word in italic terracotta.

---

## The Three Aesthetic Dials

Configure these dials based on the design read:
- **`DESIGN_VARIANCE: 8`** (1 = Strict Symmetry $\leftrightarrow$ 10 = Artsy Chaos)
- **`MOTION_INTENSITY: 6`** (1 = Static $\leftrightarrow$ 10 = Cinematic Physics)
- **`VISUAL_DENSITY: 4`** (1 = Airy Art Gallery $\leftrightarrow$ 10 = Cockpit Data)

| Aesthetic Target | Variance | Motion | Density |
|:-----------------|:--------:|:------:|:-------:|
| **Editorial / Luxury / Minimalist** | 5-6 | 3-4 | 2-3 |
| **B2B SaaS / Product Core** | 6-7 | 4-5 | 5-7 |
| **High-End Consumer / Apple-Tier** | 7-8 | 6-7 | 3-4 |
| **Experimental Studio / Awwwards** | 9-10 | 8-10 | 3-4 |

---

## Aesthetic & Layout Archetypes

### 1. Texture & Tone Archetypes
- **Ethereal Glass (Dark Tech / AI / Developer Tools)**:
  Deepest OLED black (`#050505`), pure white hairlines (`border-white/10`), heavy backdrop blur (`backdrop-blur-2xl`), geometric Grotesk typography (`Geist`, `Plus Jakarta Sans`).
- **Editorial Luxury (Studio / Lifestyle / Long-form)**:
  Warm creams (`#FDFBF7`), deep espresso text, high-contrast variable serifs (`PP Editorial New`, `Newsreader`), subtle paper texture/grain overlay (`opacity-[0.03]`).
- **Soft Structuralism (Consumer / Productivity)**:
  Pure white or silver-grey, crisp monochrome borders, massive bold headlines, ultra-soft ambient diffuse drop shadows.

### 2. Layout Archetypes (With Mobile Fallback)
- **The Asymmetrical Bento Grid**:
  Masonry-like CSS Grid of varying card proportions (`col-span-8` beside stacked `col-span-4` cards).
  *Mobile Fallback*: Automatically collapses to `grid-cols-1` with generous `gap-6` below `768px`.
- **The Z-Axis Cascade**:
  Elements stacked like physical machined cards, overlapping with varying depth of field and subtle rotations (`-2deg` or `+2deg`).
  *Mobile Fallback*: Remove rotations and negative margins on mobile to prevent touch target collisions.
- **The Editorial Split**:
  Massive headline typography on the left (`w-1/2`) with interactive staggered cards or horizontal scroll pills on the right.
  *Mobile Fallback*: Stack typography cleanly above content (`w-full`).

---

## Haptic Micro-Aesthetics

### 1. The Double-Bezel (Machined Hardware Architecture)
Never place a premium card flatly on the canvas. Treat it like a glass panel inside a machined aluminum enclosure:
- **Outer Shell**: Wrapper `div` with subtle tint (`bg-black/5` or `bg-white/5`), hairline ring (`ring-1 ring-white/10`), generous padding (`p-2`), and outer radius (`rounded-[2rem]`).
- **Inner Core**: Child container with distinct background, inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), and concentric calculated inner radius (`rounded-[calc(2rem-0.5rem)]`).

### 2. Nested "Island" Button Architecture
- Primary buttons should be pill-shaped (`rounded-full px-6 py-3`).
- **Button-in-Button Icon**: Trailing arrows or icons (`↗`) never sit naked next to text. Nest them in their own circular badge (`w-8 h-8 rounded-full bg-black/5 dark:bg-white/10 flex items-center justify-center`).

### 3. Macro-Whitespace & Typography Rhythm
- Generous section padding: double standard margins (`py-24` to `py-36`). Let the content breathe.
- Headline line-lengths kept under 70-80 characters for optimal readability.
- Clear visual hierarchy: Display headline $\rightarrow$ Subhead $\rightarrow$ Body.

---

## Fluid Motion Choreography

Reject standard `linear` and `ease-in-out` transitions. Use spring physics and custom cubic-beziers:
```css
/* Real-world mass and spring deceleration */
transition-all duration-700 ease-[cubic-bezier(0.32,0.72,0,1)]
```

- **Floating Island Navigation**: Detached floating glass pill (`mt-6 mx-auto w-max rounded-full backdrop-blur-xl`).
- **Orchestrated Reveals**: One cohesive page-load entrance or scroll-driven reveal lands far better than scattered hover animations on every element.
- **Respect User Accessibility**: Always honor `@media (prefers-reduced-motion: reduce)` by disabling non-essential transitions.

---

## Intentional Interface Copywriting

- **Words Are Design Elements**: Write from the end-user's mental model, not system architecture. (Users manage notifications, not webhook dispatchers).
- **Active Voice & Cohesive Labels**: CTAs state exact actions (*"Save changes"*, not *"Submit"*). A button labeled *"Publish"* triggers a toast saying *"Published"*.
- **Direct Error & Empty States**: Never apologize vaguely. Explain what occurred and the single direct action to fix it. Empty states are invitations to create.
