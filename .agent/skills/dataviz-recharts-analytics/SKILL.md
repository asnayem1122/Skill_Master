---
name: dataviz-recharts-analytics
description: >-
  Provides implementation patterns, SVG styling techniques, and responsive container configurations for Recharts visualizations in Next.js and Tailwind CSS applications. Use this skill when creating or debugging financial curves, compound accumulation charts, cash inflow vs outflow bar charts, category distribution pies/donuts, or confidence interval envelopes.
---

# Recharts & Financial Data Visualization in Next.js

This skill provides best practices, color mapping, and container sizing techniques for implementing Recharts in modern Next.js and Tailwind CSS dashboards.

---

## 1. Crucial Rule: SVG Class Incompatibilities

Recharts renders pure SVG elements (`<path>`, `<rect>`, `<circle>`). Tailwind CSS classes placed inside Recharts components (like `fill="fill-upay-yellow"` or `stroke="stroke-navy-900"`) are frequently ignored by Recharts SVG renderers or produce hydration mismatches.

### Always Use Explicit Hex Attributes & Embedded SVG Gradients
```tsx
<defs>
  <linearGradient id="upayGoldGlow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="5%" stopColor="#FFC709" stopOpacity={0.45} />
    <stop offset="95%" stopColor="#FFC709" stopOpacity={0.0} />
  </linearGradient>
</defs>
<Area
  type="monotone"
  dataKey="future_value"
  stroke="#FFC709"
  strokeWidth={3}
  fillOpacity={1}
  fill="url(#upayGoldGlow)"
/>
```

---

## 2. Solving `width(0) and height(0)` Container Warnings

In Vitest tests and dynamic CSS Grid layouts, `<ResponsiveContainer width="100%" height={220}>` can throw:
`The width(0) and height(0) of chart should be greater than 0...`

### Resolution Pattern
1. Wrap the chart in a container with a fixed or constrained height: `className="w-full h-56 min-w-0"`.
2. Provide `minWidth={0}` to `<ResponsiveContainer>`:
```tsx
<div className="w-full h-56 min-w-0">
  <ResponsiveContainer width="100%" height="100%" minWidth={0}>
    <AreaChart data={data}>
      {/* Chart items */}
    </AreaChart>
  </ResponsiveContainer>
</div>
```

---

## 3. Financial Visualizations Palette

| Series Role | Hex Code | Visual Styling |
| :--- | :--- | :--- |
| **Inflow / Salary / Deposits** | `#0A1C3C` | Deep Navy Blue bars or solid area lines |
| **Compound Return / Wealth** | `#FFC709` | Vibrant Upay Yellow line with gradient glow underfill |
| **Contributed Principal** | `#0F2B5C` | Navy dashed line (`strokeDasharray="4 4"`) |
| **Outflows / Expenses** | `#E11D48` | Rose bars or indicator dots |
| **Grid Lines** | `#E2E8F0` or `#1E293B` | `strokeDasharray="3 3" opacity={0.3}` |
| **Axis Labels** | `#64748B` | Slate-500, `fontSize={11}` |

---

## 4. Custom BDT Currency Tooltip
```tsx
export function BdtChartTooltip({ active, payload, label }: any) {
  if (!active || !payload || !payload.length) return null;
  return (
    <div className="rounded-xl border border-navy-800 bg-navy-950/95 p-3 shadow-xl backdrop-blur-md">
      <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">{label}</p>
      {payload.map((item: any, i: number) => (
        <p key={i} className="text-xs font-bold" style={{ color: item.color }}>
          {item.name}: ৳{Number(item.value).toLocaleString('en-BD')}
        </p>
      ))}
    </div>
  );
}
```
