import math
import os

def build_topography_svg():
    # 1. Left Mesh System (12 contours: combination of dotted and solid hairline waves + 5 transverse lines)
    left_elements = []
    
    for k in range(12):
        y0 = 50 + k * 42
        p0 = (-60, y0)
        p1 = (140 + k * 20, y0 + 65 + k * 6)
        p2 = (350 + k * 18, 350 + k * 36)
        p3 = (560 + k * 14, 650 + k * 22)
        
        d = f"M {p0[0]} {p0[1]} C {p1[0]} {p1[1]}, {p2[0]} {p2[1]}, {p3[0]} {p3[1]}"
        grad = "url(#contourSageToGold)" if k % 2 == 0 else "url(#contourGoldToSage)"
        
        # Primary dotted contour: bold, crisp dots
        op = 0.72 - k * 0.025
        left_elements.append(
            f'      <path d="{d}" stroke="{grad}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="0.1 13" opacity="{op:.2f}" />'
        )
        
        # Companion fine hairline for true 3D contour appearance
        if k % 2 == 1:
            left_elements.append(
                f'      <path d="{d}" stroke="{grad}" stroke-width="0.85" opacity="0.38" />'
            )

    # Left transverse cross-contours (5 intersecting lines creating mathematical wireframe)
    left_transverse = [
        "M 60 140 C 160 240, 250 360, 310 510",
        "M 120 190 C 220 300, 320 430, 390 590",
        "M 190 250 C 300 370, 400 510, 470 680",
        "M 260 320 C 380 450, 480 590, 560 760",
        "M 340 400 C 460 540, 560 680, 640 840"
    ]
    for idx, d in enumerate(left_transverse):
        left_elements.append(
            f'      <path d="{d}" stroke="url(#contourSageToGold)" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="0.1 16" opacity="0.35" />'
        )

    # 2. Right Mesh System (12 contours: dotted + solid hairlines + 5 transverse lines)
    right_elements = []
    for k in range(12):
        y0 = 40 + k * 42
        p0 = (1500, y0)
        p1 = (1300 - k * 20, y0 + 60 + k * 6)
        p2 = (1090 - k * 18, 340 + k * 36)
        p3 = (880 - k * 14, 640 + k * 22)
        
        d = f"M {p0[0]} {p0[1]} C {p1[0]} {p1[1]}, {p2[0]} {p2[1]}, {p3[0]} {p3[1]}"
        grad = "url(#contourGoldToSage)" if k % 2 == 0 else "url(#contourSageToGold)"
        op = 0.72 - k * 0.025
        
        right_elements.append(
            f'      <path d="{d}" stroke="{grad}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="0.1 13" opacity="{op:.2f}" />'
        )
        if k % 2 == 0:
            right_elements.append(
                f'      <path d="{d}" stroke="{grad}" stroke-width="0.85" opacity="0.38" />'
            )

    # Right transverse cross-contours
    right_transverse = [
        "M 1380 130 C 1280 230, 1190 350, 1130 500",
        "M 1320 180 C 1220 290, 1120 420, 1050 580",
        "M 1250 240 C 1140 360, 1040 500, 970 670",
        "M 1180 310 C 1060 440, 960 580, 880 750",
        "M 1100 390 C 980 530, 880 670, 800 830"
    ]
    for idx, d in enumerate(right_transverse):
        right_elements.append(
            f'      <path d="{d}" stroke="url(#contourGoldToSage)" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="0.1 16" opacity="0.35" />'
        )

    # 3. Lower Mesh System (6 undulating harmonic wave contours across the lower apron)
    lower_elements = []
    lower_paths = [
        "M 40 720 C 360 680, 720 760, 1080 700 S 1400 730, 1440 720",
        "M 20 750 C 340 710, 700 790, 1060 730 S 1380 760, 1460 750",
        "M 30 780 C 350 740, 710 820, 1070 760 S 1390 790, 1450 780",
        "M 10 810 C 330 770, 690 850, 1050 790 S 1370 820, 1470 810",
        "M 40 840 C 360 800, 720 880, 1080 820 S 1400 850, 1440 840",
        "M 20 870 C 340 830, 700 910, 1060 850 S 1380 880, 1460 870"
    ]
    for idx, d in enumerate(lower_paths):
        grad = "url(#contourSageToGold)" if idx % 2 == 0 else "url(#contourGoldToSage)"
        op = 0.48 - idx * 0.05
        lower_elements.append(
            f'      <path d="{d}" stroke="{grad}" stroke-width="2.0" stroke-linecap="round" stroke-dasharray="0.1 15" opacity="{op:.2f}" />'
        )
        if idx in (0, 2):
            lower_elements.append(
                f'      <path d="{d}" stroke="{grad}" stroke-width="0.8" opacity="0.30" />'
            )

    # 4. Upper celestial connecting arcs
    celestial_arcs = [
        '      <path d="M 60 120 C 420 20, 1020 20, 1380 120" stroke="url(#contourSageToGold)" stroke-width="0.85" stroke-dasharray="4 8" opacity="0.40" />',
        '      <path d="M 120 160 C 460 70, 980 70, 1320 160" stroke="url(#contourGoldToSage)" stroke-width="0.75" stroke-dasharray="3 6" opacity="0.35" />'
    ]

    all_paths = left_elements + right_elements + lower_elements + celestial_arcs
    return '\n'.join(all_paths)

topography_markup = build_topography_svg()

hero_astro_content = """---
import config from '../data/config.json';
---

<section class="hero-section" id="home" aria-labelledby="hero-main-title">
  <!-- Precision Architectural Dot Grid Texture -->
  <div class="hero-dot-grid" aria-hidden="true"></div>

  <!-- Micro-texture Archival Cotton Paper Grain -->
  <div class="hero-grain" aria-hidden="true"></div>

  <!-- Organic Aurora: Large Asymmetrical Soft Light Forms with Ambient Motion -->
  <div class="hero-aurora-form hero-aurora-left" aria-hidden="true"></div>
  <div class="hero-aurora-form hero-aurora-left-lower" aria-hidden="true"></div>
  <div class="hero-aurora-form hero-aurora-right" aria-hidden="true"></div>
  <div class="hero-aurora-form hero-aurora-right-lower" aria-hidden="true"></div>

  <!-- Living Topography: Mathematical Contour Mesh with Radial Center Clearing Mask -->
  <div class="hero-topography-wrapper" aria-hidden="true">
    <svg class="hero-topography-svg" viewBox="0 0 1440 900" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <!-- Gradients for Topographic Contours -->
        <linearGradient id="contourSageToGold" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#9EBFB1" />
          <stop offset="50%" stop-color="#B89558" />
          <stop offset="100%" stop-color="#D4AF37" />
        </linearGradient>

        <linearGradient id="contourGoldToSage" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#D4AF37" />
          <stop offset="50%" stop-color="#B89558" />
          <stop offset="100%" stop-color="#9EBFB1" />
        </linearGradient>

        <!-- Luminous Ambient Gold Node Glow -->
        <radialGradient id="heroNodeGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#D4AF37" stop-opacity="0.95" />
          <stop offset="35%" stop-color="#B89558" stop-opacity="0.45" />
          <stop offset="70%" stop-color="#B89558" stop-opacity="0.15" />
          <stop offset="100%" stop-color="#B89558" stop-opacity="0" />
        </radialGradient>

        <!-- Center Mask: Subtle falloff keeping text 100% readable while maintaining rich mesh structure -->
        <radialGradient id="centerMaskGradient" cx="50%" cy="45%" r="58%">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="0.22" />
          <stop offset="35%" stop-color="#ffffff" stop-opacity="0.45" />
          <stop offset="70%" stop-color="#ffffff" stop-opacity="0.92" />
          <stop offset="100%" stop-color="#ffffff" stop-opacity="1.0" />
        </radialGradient>

        <mask id="topographyClearCenterMask">
          <rect width="100%" height="100%" fill="url(#centerMaskGradient)" />
        </mask>
      </defs>

      <!-- Masked Topographic Contour Field -->
      <g mask="url(#topographyClearCenterMask)">
__TOPOGRAPHY_MARKUP__
      </g>

      <!-- Illuminated Gold Node Points with Frosted Halos at Key Topological Junctions -->
      <!-- Node A: Left Upper Flow (280, 290) -->
      <g class="hero-node-group">
        <circle cx="280" cy="290" r="18" fill="url(#heroNodeGlow)" class="node-glow" />
        <circle cx="280" cy="290" r="6.5" stroke="#B89558" stroke-width="0.9" opacity="0.75" />
        <circle cx="280" cy="290" r="2.5" fill="#B89558" />
      </g>

      <!-- Node B: Right Upper Flow (1180, 275) -->
      <g class="hero-node-group">
        <circle cx="1180" cy="275" r="18" fill="url(#heroNodeGlow)" class="node-glow" />
        <circle cx="1180" cy="275" r="6.5" stroke="#B89558" stroke-width="0.9" opacity="0.75" />
        <circle cx="1180" cy="275" r="2.5" fill="#B89558" />
      </g>

      <!-- Node C: Left Lower Transition (420, 570) -->
      <g class="hero-node-group">
        <circle cx="420" cy="570" r="15" fill="url(#heroNodeGlow)" class="node-glow" />
        <circle cx="420" cy="570" r="5.5" stroke="#B89558" stroke-width="0.8" opacity="0.65" />
        <circle cx="420" cy="570" r="2.2" fill="#B89558" />
      </g>

      <!-- Node D: Right Lower Transition (1040, 560) -->
      <g class="hero-node-group">
        <circle cx="1040" cy="560" r="15" fill="url(#heroNodeGlow)" class="node-glow" />
        <circle cx="1040" cy="560" r="5.5" stroke="#B89558" stroke-width="0.8" opacity="0.65" />
        <circle cx="1040" cy="560" r="2.2" fill="#B89558" />
      </g>
    </svg>
  </div>

  <div class="container hero-content-container">
    <!-- Architectural Corner Frame Accents (Crosshairs) -->
    <div class="corner-crosshair top-left" aria-hidden="true">+</div>
    <div class="corner-crosshair top-right" aria-hidden="true">+</div>
    <div class="corner-crosshair bottom-left" aria-hidden="true">+</div>
    <div class="corner-crosshair bottom-right" aria-hidden="true">+</div>

    <!-- Refined SEBI Registration Eyebrow -->
    <div class="hero-eyebrow" aria-label={`SEBI Registered Research Analyst ${config.sebiRegNo}`}>
      <span class="eyebrow-rule" aria-hidden="true"></span>
      <span class="eyebrow-text">
        SEBI REGISTERED RESEARCH ANALYST <span class="eyebrow-sep" aria-hidden="true">&middot;</span> {config.sebiRegNo}
      </span>
      <span class="eyebrow-rule" aria-hidden="true"></span>
    </div>

    <!-- Centered Editorial Headline with Custom Signature Flourish -->
    <h1 class="hero-title" id="hero-main-title">
      <span class="title-line">Repeat a Pattern</span>
      <span class="title-line">Until It Becomes Your</span>
      <span class="title-line signature-wrapper">
        <span class="signature-word">Signature.</span>
        <!-- Custom Handwritten Organic SVG Flourish with Gold Glow Drop Shadow -->
        <svg class="signature-flourish" aria-hidden="true" viewBox="0 0 344 28" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path 
            class="flourish-path" 
            d="M 6,19 C 52,23 110,24 168,20 C 214,17 252,13 282,12 C 298,11.5 312,14 308,18.5 C 304,22.5 290,21.5 298,15 C 304,10 322,7.5 338,7" 
            stroke="#B89558" 
            stroke-width="2.4" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
          />
        </svg>
      </span>
    </h1>

    <!-- Single Exact Supporting Statement (Strictly preserved) -->
    <p class="hero-support">
      Clarity. A deeper way of thinking about markets.
    </p>

    <!-- Single Midnight Navy Primary CTA -->
    <div class="hero-action">
      <a href="#offerings" class="btn-hero-primary" aria-label="Explore Our Research">
        <span>Explore Our Research</span>
        <span class="cta-arrow" aria-hidden="true">&rarr;</span>
      </a>
    </div>
  </div>
</section>

<style>
  /* =========================================================
     HERO SECTION: WOW FACTOR ARCHITECTURAL CANVAS & TOPOGRAPHY
     Palette:
     - 70% Porcelain Ivory Canvas: #F7F6F2
     - 20% Midnight Navy Type & Primary CTA: #19304B
     - 10% Champagne Gold Accent: #B89558 / #D4AF37
     - Atmospheric Sage Tint: #9EBFB1 / #B8CFC5
     - Supporting Copy Slate: #596879
     ========================================================= */

  .hero-section {
    position: relative;
    min-height: 100svh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #F7F6F2;
    /* Rich Atmospheric Multi-Zone Illumination */
    background-image: 
      radial-gradient(ellipse 60% 50% at 8% 12%, rgba(184, 149, 88, 0.28) 0%, transparent 58%),
      radial-gradient(ellipse 65% 55% at 10% 48%, rgba(158, 191, 177, 0.42) 0%, transparent 62%),
      radial-gradient(ellipse 55% 45% at 16% 88%, rgba(184, 149, 88, 0.32) 0%, rgba(158, 191, 177, 0.22) 40%, transparent 65%),
      radial-gradient(ellipse 50% 40% at 92% 14%, rgba(158, 191, 177, 0.28) 0%, transparent 55%),
      radial-gradient(ellipse 60% 50% at 88% 76%, rgba(184, 149, 88, 0.32) 0%, rgba(158, 191, 177, 0.24) 45%, transparent 65%),
      radial-gradient(circle at 50% 40%, rgba(247, 246, 242, 0.90) 0%, rgba(247, 246, 242, 0.55) 50%, transparent 75%);
    padding: clamp(140px, 18svh, 190px) 24px clamp(80px, 12svh, 120px);
    overflow: hidden;
  }

  /* Precision Architectural Dot Grid Texture */
  .hero-dot-grid {
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, rgba(25, 48, 75, 0.13) 1.25px, transparent 1.25px);
    background-size: 28px 28px;
    mask-image: radial-gradient(ellipse 85% 75% at 50% 48%, #000 45%, rgba(0, 0, 0, 0.4) 75%, transparent 100%);
    -webkit-mask-image: radial-gradient(ellipse 85% 75% at 50% 48%, #000 45%, rgba(0, 0, 0, 0.4) 75%, transparent 100%);
    pointer-events: none;
    z-index: 1;
  }

  /* Micro-texture Archival Cotton Paper Grain */
  .hero-grain {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    opacity: 0.035;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    mix-blend-mode: multiply;
  }

  /* Organic Aurora: Large Luminous Light Forms with Subtle Ambient Float */
  .hero-aurora-form {
    position: absolute;
    pointer-events: none;
    z-index: 1;
    animation: auroraFloat 14s ease-in-out infinite alternate;
  }

  /* Left-side form: Luminous sage interior, ivory core, champagne perimeter */
  .hero-aurora-left {
    top: 6%;
    left: clamp(-200px, -12vw, -140px);
    width: clamp(560px, 52vw, 780px);
    height: clamp(560px, 52vw, 780px);
    border-radius: 46% 54% 56% 44% / 48% 52% 48% 52%;
    background: radial-gradient(
      ellipse 65% 55% at 54% 48%,
      rgba(255, 253, 248, 0.85) 0%,
      rgba(158, 191, 177, 0.55) 26%,
      rgba(184, 149, 88, 0.38) 56%,
      rgba(158, 191, 177, 0.16) 78%,
      transparent 100%
    );
    filter: blur(52px);
  }

  /* Lower-left: Rich diffused sage and gold blending into lower wave */
  .hero-aurora-left-lower {
    bottom: -90px;
    left: clamp(-70px, -4vw, -30px);
    width: clamp(460px, 44vw, 640px);
    height: clamp(460px, 44vw, 640px);
    border-radius: 52% 48% 46% 54% / 54% 46% 54% 46%;
    background: radial-gradient(
      circle at 50% 50%,
      rgba(158, 191, 177, 0.52) 0%,
      rgba(184, 149, 88, 0.38) 48%,
      rgba(158, 191, 177, 0.16) 74%,
      transparent 100%
    );
    filter: blur(48px);
    animation-delay: -5s;
  }

  /* Right-side form: Warm champagne-gold luminous core, subtle sage tint */
  .hero-aurora-right {
    top: 8%;
    right: clamp(-190px, -12vw, -130px);
    width: clamp(520px, 48vw, 720px);
    height: clamp(520px, 48vw, 720px);
    border-radius: 54% 46% 48% 52% / 50% 54% 46% 50%;
    background: radial-gradient(
      ellipse 62% 54% at 48% 50%,
      rgba(255, 253, 248, 0.80) 0%,
      rgba(184, 149, 88, 0.52) 28%,
      rgba(158, 191, 177, 0.38) 58%,
      rgba(184, 149, 88, 0.15) 78%,
      transparent 100%
    );
    filter: blur(50px);
    animation-delay: -3s;
  }

  /* Lower-right: Ambient warm gold illumination */
  .hero-aurora-right-lower {
    bottom: -60px;
    right: clamp(20px, 4vw, 70px);
    width: clamp(420px, 38vw, 560px);
    height: clamp(420px, 38vw, 560px);
    border-radius: 50%;
    background: radial-gradient(
      circle at 50% 50%,
      rgba(184, 149, 88, 0.42) 0%,
      rgba(158, 191, 177, 0.28) 50%,
      transparent 75%
    );
    filter: blur(48px);
    animation-delay: -8s;
  }

  @keyframes auroraFloat {
    0% {
      transform: translate(0, 0) scale(1);
    }
    50% {
      transform: translate(18px, -12px) scale(1.04);
    }
    100% {
      transform: translate(-10px, 14px) scale(0.98);
    }
  }

  /* Living Topography Wrapper */
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

  .node-glow {
    animation: nodePulse 3.5s ease-in-out infinite alternate;
  }

  @keyframes nodePulse {
    0% {
      transform: scale(0.9);
      opacity: 0.65;
    }
    100% {
      transform: scale(1.15);
      opacity: 0.95;
    }
  }

  /* Central Content Composition Container */
  .hero-content-container {
    position: relative;
    z-index: 3;
    max-width: 960px;
    margin: 0 auto;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: clamp(24px, 4vw, 40px) clamp(20px, 4vw, 48px);
  }

  /* Architectural Crosshairs (+) at Framing Corners */
  .corner-crosshair {
    position: absolute;
    font-family: monospace;
    font-size: 14px;
    font-weight: 300;
    color: #B89558;
    opacity: 0.45;
    pointer-events: none;
    line-height: 1;
  }

  .corner-crosshair.top-left { top: 0; left: 0; }
  .corner-crosshair.top-right { top: 0; right: 0; }
  .corner-crosshair.bottom-left { bottom: 0; left: 0; }
  .corner-crosshair.bottom-right { bottom: 0; right: 0; }

  /* Refined SEBI Registration Eyebrow */
  .hero-eyebrow {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-bottom: clamp(24px, 4vh, 34px);
  }

  .eyebrow-rule {
    display: inline-block;
    width: 36px;
    height: 1px;
    background-color: #B89558;
    opacity: 0.9;
  }

  .eyebrow-text {
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: clamp(0.75rem, 0.85vw, 0.8125rem);
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #596879;
    white-space: nowrap;
  }

  .eyebrow-sep {
    display: inline-block;
    margin: 0 4px;
    color: #B89558;
    font-weight: 700;
  }

  /* Centered Editorial Headline */
  .hero-title {
    font-family: 'Instrument Serif', 'DM Serif Display', Georgia, serif;
    font-size: clamp(3.2rem, 5.8vw, 5.75rem);
    font-weight: 400;
    line-height: 1.04;
    letter-spacing: -0.04em;
    color: #19304B;
    margin: 0 0 clamp(20px, 3vh, 28px);
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .title-line {
    display: block;
    white-space: nowrap;
  }

  .signature-wrapper {
    position: relative;
    display: inline-block;
    margin-top: 2px;
  }

  /* High-end Metallic Champagne Gold Italic Serif */
  .signature-word {
    font-family: 'Instrument Serif', 'DM Serif Display', Georgia, serif;
    font-style: italic;
    background: linear-gradient(135deg, #B89558 0%, #D4AF37 45%, #9E7B3B 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-right: 0.05em;
    display: inline-block;
  }

  /* Custom Handwritten Signature Flourish with Ambient Gold Glow */
  .signature-flourish {
    position: absolute;
    left: -3%;
    bottom: -15px;
    width: 106%;
    height: 24px;
    pointer-events: none;
    overflow: visible;
    filter: drop-shadow(0 2px 8px rgba(184, 149, 88, 0.40));
  }

  .flourish-path {
    stroke-dasharray: 400;
    stroke-dashoffset: 400;
    animation: drawFlourish 1.25s cubic-bezier(0.22, 1, 0.36, 1) 0.35s forwards;
  }

  @keyframes drawFlourish {
    to {
      stroke-dashoffset: 0;
    }
  }

  /* Supporting Paragraph */
  .hero-support {
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: clamp(1.125rem, 1.6vw, 1.25rem);
    font-weight: 400;
    line-height: 1.65;
    color: #596879;
    max-width: 620px;
    margin: 0 auto clamp(32px, 5vh, 44px);
    text-align: center;
  }

  /* Midnight Navy Primary CTA */
  .hero-action {
    display: flex;
    justify-content: center;
    width: 100%;
  }

  .btn-hero-primary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    background-color: #19304B;
    color: #F7F6F2;
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    min-height: 56px;
    padding: 0 38px;
    border-radius: 12px;
    border: 1px solid rgba(25, 48, 75, 0.25);
    box-shadow: 
      0 4px 14px rgba(25, 48, 75, 0.14),
      0 1px 3px rgba(25, 48, 75, 0.08);
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
      0 10px 28px rgba(25, 48, 75, 0.24),
      0 2px 6px rgba(25, 48, 75, 0.12);
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

  /* Mobile and Responsive Adaptations */
  @media (max-width: 768px) {
    .hero-section {
      padding-top: 130px;
      padding-bottom: 70px;
      min-height: auto;
    }

    .hero-dot-grid {
      background-size: 22px 22px;
    }

    .corner-crosshair {
      display: none;
    }

    .hero-aurora-left {
      width: 340px;
      height: 340px;
      left: -120px;
      filter: blur(42px);
      opacity: 0.85;
    }

    .hero-aurora-right {
      width: 320px;
      height: 320px;
      right: -120px;
      filter: blur(42px);
      opacity: 0.85;
    }

    .hero-aurora-left-lower,
    .hero-aurora-right-lower {
      display: none;
    }

    .hero-eyebrow {
      gap: 8px;
    }

    .eyebrow-rule {
      width: 20px;
    }

    .eyebrow-text {
      font-size: 0.6875rem;
      letter-spacing: 0.12em;
    }

    .hero-title {
      font-size: clamp(2.35rem, 8.5vw, 3.2rem);
      line-height: 1.08;
    }

    .title-line {
      white-space: normal;
    }

    .signature-flourish {
      bottom: -11px;
      height: 20px;
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
    .hero-aurora-form,
    .node-glow {
      animation: none;
    }

    .flourish-path {
      stroke-dashoffset: 0;
      animation: none;
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

print(f"WOW Factor Hero.astro generated successfully! Total vector elements: {topography_markup.count('<path')}")
