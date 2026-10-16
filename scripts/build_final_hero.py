import math
import os

def generate_vector_topography():
    left_contours = []
    # Left mesh: 12 flowing contour curves sweeping from left edge toward lower-center
    for k in range(12):
        y0 = 60 + k * 40
        p0 = (-40, y0)
        p1 = (140 + k * 18, y0 + 60 + k * 6)
        p2 = (340 + k * 16, 350 + k * 35)
        p3 = (540 + k * 12, 650 + k * 20)
        
        d = f"M {p0[0]} {p0[1]} C {p1[0]} {p1[1]}, {p2[0]} {p2[1]}, {p3[0]} {p3[1]}"
        grad = "url(#contourSageToGold)" if k % 2 == 0 else "url(#contourGoldToSage)"
        op = 0.68 - k * 0.02
        
        # Dotted contour
        left_contours.append(
            f'      <path d="{d}" stroke="{grad}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="0.1 14" opacity="{op:.2f}" />'
        )
        # Interspersed delicate hairline guide
        if k in (1, 4, 7, 10):
            left_contours.append(
                f'      <path d="{d}" stroke="{grad}" stroke-width="0.75" opacity="0.32" />'
            )

    # Left transverse cross-contours (4 delicate intersecting lines)
    left_transverse = [
        "M 80 160 C 180 250, 260 370, 310 510",
        "M 150 210 C 250 310, 340 440, 400 590",
        "M 230 270 C 330 380, 420 520, 480 680",
        "M 310 340 C 420 460, 510 600, 580 760"
    ]
    for d in left_transverse:
        left_contours.append(
            f'      <path d="{d}" stroke="url(#contourSageToGold)" stroke-width="1.6" stroke-linecap="round" stroke-dasharray="0.1 18" opacity="0.28" />'
        )

    # Right mesh: 12 flowing contour curves sweeping from upper-right toward lower-right
    right_contours = []
    for k in range(12):
        y0 = 50 + k * 40
        p0 = (1480, y0)
        p1 = (1300 - k * 18, y0 + 55 + k * 6)
        p2 = (1100 - k * 16, 340 + k * 35)
        p3 = (900 - k * 12, 640 + k * 20)
        
        d = f"M {p0[0]} {p0[1]} C {p1[0]} {p1[1]}, {p2[0]} {p2[1]}, {p3[0]} {p3[1]}"
        grad = "url(#contourGoldToSage)" if k % 2 == 0 else "url(#contourSageToGold)"
        op = 0.68 - k * 0.02
        
        right_contours.append(
            f'      <path d="{d}" stroke="{grad}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="0.1 14" opacity="{op:.2f}" />'
        )
        if k in (0, 3, 6, 9):
            right_contours.append(
                f'      <path d="{d}" stroke="{grad}" stroke-width="0.75" opacity="0.32" />'
            )

    # Right transverse cross-contours
    right_transverse = [
        "M 1360 150 C 1260 240, 1180 360, 1130 500",
        "M 1290 200 C 1190 300, 1100 430, 1040 580",
        "M 1210 260 C 1110 370, 1020 510, 960 670",
        "M 1130 330 C 1020 450, 930 590, 860 750"
    ]
    for d in right_transverse:
        right_contours.append(
            f'      <path d="{d}" stroke="url(#contourGoldToSage)" stroke-width="1.6" stroke-linecap="round" stroke-dasharray="0.1 18" opacity="0.28" />'
        )

    # Lower mesh: 5 undulating wave contours across the lower apron
    lower_contours = []
    lower_paths = [
        "M 40 730 C 360 690, 720 770, 1080 710 S 1400 740, 1440 730",
        "M 20 760 C 340 720, 700 800, 1060 740 S 1380 770, 1460 760",
        "M 30 790 C 350 750, 710 830, 1070 770 S 1390 800, 1450 790",
        "M 10 820 C 330 780, 690 860, 1050 800 S 1370 830, 1470 820",
        "M 40 850 C 360 810, 720 890, 1080 830 S 1400 860, 1440 850"
    ]
    for idx, d in enumerate(lower_paths):
        grad = "url(#contourSageToGold)" if idx % 2 == 0 else "url(#contourGoldToSage)"
        op = 0.44 - idx * 0.05
        lower_contours.append(
            f'      <path d="{d}" stroke="{grad}" stroke-width="1.9" stroke-linecap="round" stroke-dasharray="0.1 15" opacity="{op:.2f}" />'
        )

    # Orbital curves following orbs
    orbital_arcs = [
        # Orbital path around Orb A (left)
        '      <path d="M -20 180 C 120 130, 310 240, 360 380 S 310 540, 160 580" stroke="#B89558" stroke-width="0.85" stroke-dasharray="3 6" opacity="0.45" />',
        # Orbital path around Orb B (lower right)
        '      <path d="M 1460 520 C 1340 540, 1180 620, 1140 740 S 1220 860, 1380 880" stroke="#B89558" stroke-width="0.85" stroke-dasharray="3 6" opacity="0.45" />',
        # Upper connecting horizon arc
        '      <path d="M 80 130 C 440 45, 1000 45, 1360 130" stroke="#B8CFC5" stroke-width="0.75" stroke-dasharray="3 7" opacity="0.35" />'
    ]

    all_paths = left_contours + right_contours + lower_contours + orbital_arcs
    return '\n'.join(all_paths)

topography_markup = generate_vector_topography()

hero_astro_content = """---
import config from '../data/config.json';
---

<section class="hero-section" id="home" aria-labelledby="hero-main-title">
  <!-- Layer 1 & 2: Base Porcelain Ivory + Broad Aurora Radial Lighting -->
  <div class="hero-aurora-glow" aria-hidden="true"></div>

  <!-- Layer 3: Ultra-subtle Archival Paper Grain -->
  <div class="hero-paper-grain" aria-hidden="true"></div>

  <!-- Layer 4: Living Topography — 100% Vector Dotted Contour Mesh with Radial Center Clearing Mask -->
  <div class="hero-topography-wrapper" aria-hidden="true">
    <svg class="hero-topography-svg" viewBox="0 0 1440 900" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <!-- Gradients for Topographic Contours -->
        <linearGradient id="contourSageToGold" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#B8CFC5" />
          <stop offset="50%" stop-color="#B89558" />
          <stop offset="100%" stop-color="#D5E2DA" />
        </linearGradient>

        <linearGradient id="contourGoldToSage" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#B89558" />
          <stop offset="50%" stop-color="#D5E2DA" />
          <stop offset="100%" stop-color="#B8CFC5" />
        </linearGradient>

        <!-- Luminous Ambient Gold Node Glow -->
        <radialGradient id="goldNodeGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#B89558" stop-opacity="0.95" />
          <stop offset="35%" stop-color="#B89558" stop-opacity="0.40" />
          <stop offset="100%" stop-color="#B89558" stop-opacity="0" />
        </radialGradient>

        <!-- Radial Center-Clearing Mask: Fades mesh gracefully around central headline -->
        <radialGradient id="topographyCenterMask" cx="50%" cy="46%" r="56%">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="0.10" />
          <stop offset="32%" stop-color="#ffffff" stop-opacity="0.25" />
          <stop offset="68%" stop-color="#ffffff" stop-opacity="0.88" />
          <stop offset="100%" stop-color="#ffffff" stop-opacity="1.0" />
        </radialGradient>

        <mask id="topographyMask">
          <rect width="100%" height="100%" fill="url(#topographyCenterMask)" />
        </mask>
      </defs>

      <!-- Masked Topographic Contours (Zero pixelation, crisp vector fidelity) -->
      <g mask="url(#topographyMask)">
__TOPOGRAPHY_MARKUP__
      </g>

      <!-- Illuminated Gold Node Points at Key Topological Junctions -->
      <g class="hero-topological-node">
        <circle cx="280" cy="275" r="16" fill="url(#goldNodeGlow)" />
        <circle cx="280" cy="275" r="5.5" stroke="#B89558" stroke-width="0.8" opacity="0.65" />
        <circle cx="280" cy="275" r="2.2" fill="#B89558" />
      </g>
      <g class="hero-topological-node">
        <circle cx="1160" cy="265" r="16" fill="url(#goldNodeGlow)" />
        <circle cx="1160" cy="265" r="5.5" stroke="#B89558" stroke-width="0.8" opacity="0.65" />
        <circle cx="1160" cy="265" r="2.2" fill="#B89558" />
      </g>
      <g class="hero-topological-node">
        <circle cx="360" cy="380" r="14" fill="url(#goldNodeGlow)" />
        <circle cx="360" cy="380" r="5" stroke="#B89558" stroke-width="0.75" opacity="0.55" />
        <circle cx="360" cy="380" r="2.0" fill="#B89558" />
      </g>
      <g class="hero-topological-node">
        <circle cx="1140" cy="740" r="14" fill="url(#goldNodeGlow)" />
        <circle cx="1140" cy="740" r="5" stroke="#B89558" stroke-width="0.75" opacity="0.55" />
        <circle cx="1140" cy="740" r="2.0" fill="#B89558" />
      </g>
    </svg>
  </div>

  <!-- Layer 5: Three Distinct Luminous Orbs (Constructed with Translucent Highlights & Halos) -->
  <div class="hero-luminous-orbs" aria-hidden="true">
    <!-- Orb A: Large Sage Orb on the Left (Upper-Middle, partially cropped) -->
    <div class="luminous-orb orb-sage-left"></div>

    <!-- Orb B: Large Champagne Orb on Lower-Right (Partially cropped) -->
    <div class="luminous-orb orb-champagne-right"></div>

    <!-- Orb C: Smaller Sage Accent Orb (Upper-Right) -->
    <div class="luminous-orb orb-accent-upper"></div>
  </div>

  <!-- Layer 6: Foreground Content Composition Container with Staggered Entrance -->
  <div class="container hero-content-container">
    <!-- Refined SEBI Registration Eyebrow -->
    <div class="hero-eyebrow animate-fade-in" aria-label={`SEBI Registered Research Analyst ${config.sebiRegNo}`}>
      <span class="eyebrow-rule" aria-hidden="true"></span>
      <span class="eyebrow-text">
        SEBI REGISTERED RESEARCH ANALYST <span class="eyebrow-sep" aria-hidden="true">&middot;</span> {config.sebiRegNo}
      </span>
      <span class="eyebrow-rule" aria-hidden="true"></span>
    </div>

    <!-- Centered Editorial Headline with Staggered Line-by-Line Flow-In Animation -->
    <h1 class="hero-title" id="hero-main-title">
      <!-- Line 1 -->
      <span class="line-mask">
        <span class="line-reveal line-reveal-1">Repeat a Pattern</span>
      </span>
      
      <!-- Line 2 -->
      <span class="line-mask">
        <span class="line-reveal line-reveal-2">Until It Becomes Your</span>
      </span>
      
      <!-- Line 3 (Distinctive Editorial Italic Serif Signature) -->
      <span class="line-mask signature-mask">
        <span class="line-reveal line-reveal-3 signature-wrapper">
          <span class="signature-word">Signature.</span>
          <!-- Custom Hand-Drawn Signature Flourish with Layered Crisp Core & Visible Luminous Glow -->
          <svg class="signature-flourish" aria-hidden="true" viewBox="0 0 340 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <filter id="flourishGlowFilter" x="-20%" y="-40%" width="140%" height="180%">
                <feGaussianBlur stdDeviation="3.5" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
              </filter>
            </defs>
            <!-- Back Glow Path: Soft Luminous Halo -->
            <path 
              class="flourish-glow" 
              d="M 6,20 C 52,24 108,25 166,21 C 212,18 250,14 280,13 C 295,12.5 308,15 304,19.5 C 300,23.5 286,22.5 294,16 C 300,11 318,8.5 334,8" 
              stroke="#B89558" 
              stroke-width="7" 
              stroke-linecap="round" 
              stroke-linejoin="round" 
              opacity="0.42"
              filter="url(#flourishGlowFilter)"
            />
            <!-- Foreground Stroke: Clean, Crisp, Hand-Drawn Line -->
            <path 
              class="flourish-core" 
              d="M 6,20 C 52,24 108,25 166,21 C 212,18 250,14 280,13 C 295,12.5 308,15 304,19.5 C 300,23.5 286,22.5 294,16 C 300,11 318,8.5 334,8" 
              stroke="#B89558" 
              stroke-width="2.3" 
              stroke-linecap="round" 
              stroke-linejoin="round" 
            />
          </svg>
        </span>
      </span>
    </h1>

    <!-- Single Exact Supporting Statement (Strictly preserved) -->
    <p class="hero-support animate-support">
      Clarity. A deeper way of thinking about markets.
    </p>

    <!-- Primary Midnight Navy CTA -->
    <div class="hero-action animate-cta">
      <a href="#offerings" class="btn-hero-primary" aria-label="Explore Our Research">
        <span>Explore Our Research</span>
        <span class="cta-arrow" aria-hidden="true">&rarr;</span>
      </a>
    </div>
  </div>
</section>

<style>
  /* =========================================================
     HERO SECTION: FINAL MASTER POLISH
     Organic Aurora · Luminous Orbs · Living Topography · Glowing Signature
     Color System:
     - 70% Porcelain Ivory Canvas: #F7F6F2
     - 20% Midnight Navy Headline & Primary UI: #19304B
     - 10% Champagne Gold Signature Accent: #B89558
     - Atmospheric Soft Sage Tint: #B8CFC5
     - Translucent Pale Sage: #D5E2DA
     - Supporting Copy Slate: #596879
     ========================================================= */

  .hero-section {
    position: relative;
    min-height: 100svh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #F7F6F2;
    /* Layer 1 & 2: Broad Aurora Radial Lighting across Ivory Canvas */
    background-image: 
      radial-gradient(ellipse 65% 55% at 10% 15%, rgba(184, 149, 88, 0.20) 0%, transparent 60%),
      radial-gradient(ellipse 70% 60% at 12% 50%, rgba(184, 207, 197, 0.32) 0%, transparent 65%),
      radial-gradient(ellipse 55% 45% at 16% 88%, rgba(184, 149, 88, 0.22) 0%, rgba(184, 207, 197, 0.16) 42%, transparent 68%),
      radial-gradient(ellipse 50% 40% at 90% 15%, rgba(184, 207, 197, 0.22) 0%, transparent 55%),
      radial-gradient(ellipse 65% 55% at 88% 78%, rgba(184, 149, 88, 0.26) 0%, rgba(184, 207, 197, 0.18) 45%, transparent 68%),
      radial-gradient(circle at 50% 40%, rgba(247, 246, 242, 0.94) 0%, rgba(247, 246, 242, 0.60) 50%, transparent 75%);
    padding: clamp(140px, 18svh, 190px) 24px clamp(80px, 12svh, 120px);
    overflow: hidden;
  }

  /* Layer 3: Ultra-subtle Archival Paper Grain */
  .hero-paper-grain {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    opacity: 0.025;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    mix-blend-mode: multiply;
  }

  /* Layer 4: Living Topography Vector SVG Wrapper */
  .hero-topography-wrapper {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 2;
    overflow: hidden;
  }

  .hero-topography-svg {
    width: 100%;
    height: 100%;
    display: block;
  }

  /* Layer 5: Three Distinct Luminous Orbs */
  .hero-luminous-orbs {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 3;
    overflow: hidden;
  }

  .luminous-orb {
    position: absolute;
    border-radius: 50%;
    will-change: transform;
    animation: orbGentleDrift 18s ease-in-out infinite alternate;
  }

  /* Orb A: Large Sage Orb on Left (Upper-Middle, partially cropped) */
  .orb-sage-left {
    top: 14%;
    left: clamp(-180px, -11vw, -120px);
    width: clamp(340px, 32vw, 440px);
    height: clamp(340px, 32vw, 440px);
    background: radial-gradient(
      circle at 42% 38%,
      rgba(255, 253, 248, 0.85) 0%,
      rgba(213, 226, 218, 0.65) 25%,
      rgba(184, 207, 197, 0.45) 50%,
      rgba(184, 149, 88, 0.25) 75%,
      transparent 100%
    );
    box-shadow: 
      inset -8px -8px 24px rgba(184, 149, 88, 0.22),
      inset 6px 6px 20px rgba(255, 253, 248, 0.8),
      0 0 65px rgba(184, 207, 197, 0.35);
    filter: blur(8px);
  }

  .orb-sage-left::before {
    content: '';
    position: absolute;
    inset: -35px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(184, 207, 197, 0.32) 0%, rgba(184, 149, 88, 0.16) 52%, transparent 72%);
    filter: blur(35px);
  }

  /* Orb B: Large Champagne Orb on Lower-Right (Partially cropped) */
  .orb-champagne-right {
    bottom: 6%;
    right: clamp(-170px, -10vw, -110px);
    width: clamp(360px, 34vw, 460px);
    height: clamp(360px, 34vw, 460px);
    background: radial-gradient(
      circle at 42% 38%,
      rgba(255, 253, 248, 0.85) 0%,
      rgba(184, 149, 88, 0.55) 30%,
      rgba(184, 207, 197, 0.35) 60%,
      rgba(184, 149, 88, 0.15) 80%,
      transparent 100%
    );
    box-shadow: 
      inset -8px -8px 24px rgba(184, 207, 197, 0.25),
      inset 6px 6px 20px rgba(255, 253, 248, 0.8),
      0 0 70px rgba(184, 149, 88, 0.32);
    filter: blur(8px);
    animation-delay: -5s;
  }

  .orb-champagne-right::before {
    content: '';
    position: absolute;
    inset: -35px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(184, 149, 88, 0.35) 0%, rgba(184, 207, 197, 0.18) 55%, transparent 72%);
    filter: blur(40px);
  }

  /* Orb C: Smaller Sage Accent Orb (Upper-Right) */
  .orb-accent-upper {
    top: 12%;
    right: clamp(40px, 6vw, 120px);
    width: clamp(190px, 18vw, 240px);
    height: clamp(190px, 18vw, 240px);
    background: radial-gradient(
      circle at 38% 35%,
      rgba(255, 253, 248, 0.80) 0%,
      rgba(213, 226, 218, 0.55) 35%,
      rgba(184, 149, 88, 0.20) 70%,
      transparent 100%
    );
    box-shadow: 
      inset 4px 4px 14px rgba(255, 253, 248, 0.7),
      0 0 45px rgba(184, 207, 197, 0.28);
    filter: blur(6px);
    animation-delay: -9s;
  }

  @keyframes orbGentleDrift {
    0% {
      transform: translate(0, 0) scale(1);
    }
    50% {
      transform: translate(14px, -10px) scale(1.03);
    }
    100% {
      transform: translate(-10px, 12px) scale(0.98);
    }
  }

  /* Layer 6: Content Composition Container */
  .hero-content-container {
    position: relative;
    z-index: 4;
    max-width: 980px;
    margin: 0 auto;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* Refined SEBI Registration Eyebrow */
  .hero-eyebrow {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-bottom: clamp(24px, 4vh, 32px);
  }

  .eyebrow-rule {
    display: inline-block;
    width: 32px;
    height: 1.5px;
    background-color: #B89558;
    opacity: 0.85;
    border-radius: 2px;
  }

  .eyebrow-text {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: clamp(0.75rem, 0.85vw, 0.8125rem);
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #596879;
    white-space: nowrap;
  }

  .eyebrow-sep {
    display: inline-block;
    margin: 0 4px;
    color: #B89558;
    font-weight: 800;
  }

  /* Centered Editorial Headline: High-Contrast Instrument Serif */
  .hero-title {
    font-family: 'Instrument Serif', 'DM Serif Display', Georgia, serif;
    font-size: clamp(3.2rem, 5.7vw, 5.6rem);
    font-weight: 400;
    line-height: 1.04;
    letter-spacing: -0.035em;
    color: #19304B;
    margin: 0 0 clamp(22px, 3.2vh, 30px);
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* Staggered Flow-In Line Masking */
  .line-mask {
    display: block;
    overflow: hidden;
    padding: 2px 14px 6px;
  }

  .signature-mask {
    overflow: visible;
    padding-bottom: 14px;
  }

  .line-reveal {
    display: inline-block;
    opacity: 0;
    transform: translateY(115%) rotateX(-10deg);
    animation: textFlowIn 0.85s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    transform-origin: bottom center;
  }

  .line-reveal-1 {
    animation-delay: 0.15s;
  }

  .line-reveal-2 {
    animation-delay: 0.35s;
  }

  .line-reveal-3 {
    animation-delay: 0.55s;
  }

  @keyframes textFlowIn {
    0% {
      opacity: 0;
      transform: translateY(115%) rotateX(-10deg);
    }
    100% {
      opacity: 1;
      transform: translateY(0) rotateX(0deg);
    }
  }

  /* Signature Styling: Distinctive Champagne Gold Italic Serif */
  .signature-wrapper {
    position: relative;
    display: inline-block;
  }

  .signature-word {
    font-family: 'Instrument Serif', 'DM Serif Display', Georgia, serif;
    font-weight: 400;
    font-style: italic;
    color: #B89558;
    display: inline-block;
    padding-right: 0.05em;
  }

  /* Custom Hand-Drawn Signature Flourish with Layered Crisp Core & Visible Luminous Glow */
  .signature-flourish {
    position: absolute;
    left: -4%;
    bottom: -15px;
    width: 108%;
    height: 28px;
    pointer-events: none;
    overflow: visible;
  }

  .flourish-glow,
  .flourish-core {
    stroke-dasharray: 400;
    stroke-dashoffset: 400;
    animation: drawFlourish 1.1s cubic-bezier(0.16, 1, 0.3, 1) 0.82s forwards;
  }

  @keyframes drawFlourish {
    to {
      stroke-dashoffset: 0;
    }
  }

  /* Eyebrow entrance */
  .animate-fade-in {
    opacity: 0;
    transform: translateY(-12px);
    animation: simpleFadeIn 0.7s cubic-bezier(0.16, 1, 0.3, 1) 0.05s forwards;
  }

  /* Supporting Paragraph Entrance */
  .hero-support {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: clamp(1.125rem, 1.6vw, 1.25rem);
    font-weight: 400;
    line-height: 1.65;
    color: #596879;
    max-width: 620px;
    margin: 0 auto clamp(32px, 5vh, 42px);
    text-align: center;
    opacity: 0;
    transform: translateY(18px);
    animation: simpleFadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.95s forwards;
  }

  /* Primary CTA Entrance */
  .hero-action {
    display: flex;
    justify-content: center;
    width: 100%;
    opacity: 0;
    transform: translateY(18px);
    animation: simpleFadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) 1.10s forwards;
  }

  @keyframes simpleFadeIn {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Primary Midnight Navy CTA */
  .btn-hero-primary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    background-color: #19304B;
    color: #F7F6F2;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    min-height: 56px;
    padding: 0 38px;
    border-radius: 12px;
    border: 1px solid rgba(25, 48, 75, 0.22);
    box-shadow: 
      0 4px 14px rgba(25, 48, 75, 0.12),
      0 1px 3px rgba(25, 48, 75, 0.06);
    text-decoration: none;
    transition: 
      background-color 0.25s cubic-bezier(0.16, 1, 0.3, 1),
      transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
      box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .btn-hero-primary:hover {
    background-color: #122337;
    transform: translateY(-2px);
    box-shadow: 
      0 10px 28px rgba(25, 48, 75, 0.22),
      0 2px 6px rgba(25, 48, 75, 0.10);
    color: #FFFFFF;
  }

  .cta-arrow {
    display: inline-block;
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .btn-hero-primary:hover .cta-arrow {
    transform: translateX(4px);
  }

  .btn-hero-primary:focus-visible {
    outline: 3px solid #B89558;
    outline-offset: 3px;
  }

  /* Responsive Adjustments */
  @media (max-width: 768px) {
    .hero-section {
      padding-top: 130px;
      padding-bottom: 70px;
      min-height: auto;
    }

    .orb-sage-left {
      width: 260px;
      height: 260px;
      left: -100px;
      filter: blur(6px);
    }

    .orb-champagne-right {
      width: 280px;
      height: 280px;
      right: -100px;
      filter: blur(6px);
    }

    .orb-accent-upper {
      width: 140px;
      height: 140px;
      right: 20px;
      filter: blur(5px);
    }

    .hero-eyebrow {
      gap: 8px;
    }

    .eyebrow-rule {
      width: 18px;
    }

    .eyebrow-text {
      font-size: 0.6875rem;
      letter-spacing: 0.11em;
    }

    .hero-title {
      font-size: clamp(2.65rem, 9vw, 3.7rem);
      line-height: 1.08;
    }

    .line-mask {
      white-space: normal;
      padding: 2px 4px 6px;
    }

    .signature-flourish {
      bottom: -10px;
      height: 22px;
    }

    .hero-support {
      font-size: 1.0625rem;
      padding: 0 12px;
    }

    .btn-hero-primary {
      width: 100%;
      max-width: 320px;
    }
  }

  /* Accessibility: Prefers Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .luminous-orb {
      animation: none !important;
    }

    .animate-fade-in,
    .line-reveal,
    .hero-support,
    .hero-action {
      opacity: 1 !important;
      transform: none !important;
      animation: none !important;
    }

    .flourish-glow,
    .flourish-core {
      stroke-dashoffset: 0 !important;
      animation: none !important;
    }

    .btn-hero-primary,
    .cta-arrow {
      transition: none;
    }

    .btn-hero-primary:hover {
      transform: none;
    }

    .btn-hero-primary:hover .cta-arrow {
      transform: none;
    }
  }
</style>
"""

final_astro = hero_astro_content.replace('__TOPOGRAPHY_MARKUP__', topography_markup)

target_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'components', 'Hero.astro')
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(final_astro)

print(f"Final Master Hero.astro generated successfully! Vector elements: {topography_markup.count('<path')}")
