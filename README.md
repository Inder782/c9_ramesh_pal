# Ramesh Pal Research — SEBI-Registered Research Analyst Platform

> **SEBI Registration:** `INH0000XXXXX` | **Type:** Individual  
> **Principal Analyst & Founder:** Ramesh Pal (Accredited Educator & Research Analyst)  
> **Philosophy:** *"Repeat a pattern until it becomes your signature."*  
> **Accessibility:** 100% WCAG 2.2 Level AA & IAAP CPACC Compliant (Zero Defects)

---

## 📐 Project Overview

**Ramesh Pal Research** is an institutional-grade, zero-defect web platform built on **Astro.js (v7)**. Designed for disciplined equity investors, the platform bridges the pedagogical rigor of an accredited educator with systematic equity market research:

1. **The Educator's Edge:** In education, competence is never an accident—it is the direct outcome of disciplined, structured repetition.
2. **Signature Pattern Framework:** Eliminating emotional gambling by isolating high-probability structural setups, respecting mathematical risk limits (1–2% max capital risk), and repeating execution with zero deviation.
3. **Institutional Trust:** Complete compliance architecture with 3-tier grievance escalation (Internal -> SEBI SCORES -> SMART ODR), SEBI investor charter, complaints data table, and statutory legal modals.

---

## 🎨 3-Color Palette & Design Tokens

Built strictly for mathematical contrast (WCAG 2.2 AA / AAA):

- **Color 1 (Canvas & Surfaces):** `#F8FAFC` (Architectural Off-White) / `#FFFFFF` (Card White)
- **Color 2 (Primary Ink & Structure):** `#0F172A` (Slate 900 — **17.85:1 contrast** on white)
- **Color 3 (Signature Academic Emerald):** `#065F46` / `#035940` (Forest/Emerald — **8.38:1 contrast** on white)

---

## ♿ WCAG 2.2 Level AA & IAAP Verification

The codebase includes an automated audit verification suite in `scripts/verify_all_wcag.py`:

```bash
# Build the static site
npm run build

# Run automated WCAG 2.2 AA compliance suite
python3 scripts/verify_all_wcag.py
```

### Verified Accessibility Standards:
- **Zero Generic ARIA Abuse (WCAG 4.1.2):** No unmapped ARIA labels on non-interactive containers.
- **Label-in-Name (WCAG 2.5.3):** 100% of visible link and button texts match their accessible names.
- **Decorative Media Hiding (WCAG 1.1.1):** 100% of SVGs and typographic entities wrapped in `aria-hidden="true"`.
- **Moving Content Control (WCAG 2.2.2):** Market ticker features keyboard-operable Pause / Resume toggle and respects `prefers-reduced-motion`.
- **Accessible Data Tables (WCAG 1.3.1):** All tables include semantic `<caption>`, `th scope="col"`, and `th scope="row"` wrapped inside a scrollable container.
- **Collision-Free Mobile Drawer:** Rendered outside fixed wrappers, locks body scroll, uses `inert` attribute.
- **RA Sahayak Accessibility Widget:** Integrated into global layout meeting Indian RPwD Act compliance.

---

## 🚀 Development & Build

```bash
# Start local dev server
npm run dev

# Compile static distribution
npm run build

# Preview build locally
npm run preview
```
