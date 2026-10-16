import math
import os

def build_topography_svg():
    # 1. Left Mesh System (10 contour lines + 3 hairline guides + 4 transverse lines)
    left_contours = []
    # Main longitudinal contours
    for k in range(10):
        # Parametric control points for line k
        # Asymmetrical sweep from left edge downward to lower-center
        y0 = 70 + k * 44
        p0 = (-50, y0)
        p1 = (130 + k * 22, y0 + 60 + k * 8)
        p2 = (330 + k * 20, 360 + k * 40)
        p3 = (530 + k * 16, 660 + k * 24)
        
        d = f"M {p0[0]} {p0[1]} C {p1[0]} {p1[1]}, {p2[0]} {p2[1]}, {p3[0]} {p3[1]}"
        grad = "url(#contourSageToGold)" if k % 2 == 0 else "url(#contourGoldToSage)"
        op = 0.55 - k * 0.025
        
        # Dotted contour
        left_contours.append(
            f'      <path d="{d}" stroke="{grad}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="0.1 14" opacity="{op:.2f}" />'
        )
        # Hairline guide path on every 3rd contour
        if k in (1, 4, 7):
            left_contours.append(
                f'      <path d="{d}" stroke="{grad}" stroke-width="0.75" opacity="0.30" />'
            )

    # Left transverse cross-contours (4 lines cutting across the longitudinal flow)
    left_transverse = [
        "M 80 180 C 180 270, 260 380, 310 520",
        "M 140 230 C 240 330, 330 450, 390 600",
        "M 210 290 C 310 400, 410 530, 470 690",
        "M 280 360 C 390 480, 490 610, 560 770"
    ]
    for idx, d in enumerate(left_transverse):
        left_contours.append(
            f'      <path d="{d}" stroke="url(#contourSageToGold)" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="0.1 18" opacity="0.25" />'
        )

    # 2. Right Mesh System (10 contour lines + 3 hairline guides + 4 transverse lines)
    right_contours = []
    for k in range(10):
        # Asymmetrical control points: right side sweeps with slightly steeper angle
        y0 = 60 + k * 44
        p0 = (1490, y0)
        p1 = (1310 - k * 22, y0 + 55 + k * 8)
        p2 = (1110 - k * 20, 350 + k * 40)
        p3 = (910 - k * 16, 650 + k * 24)
        
        d = f"M {p0[0]} {p0[1]} C {p1[0]} {p1[1]}, {p2[0]} {p2[1]}, {p3[0]} {p3[1]}"
        grad = "url(#contourGoldToSage)" if k % 2 == 0 else "url(#contourSageToGold)"
        op = 0.55 - k * 0.025
        
        right_contours.append(
            f'      <path d="{d}" stroke="{grad}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="0.1 14" opacity="{op:.2f}" />'
        )
        if k in (2, 5, 8):
            right_contours.append(
                f'      <path d="{d}" stroke="{grad}" stroke-width="0.75" opacity="0.30" />'
            )

    # Right transverse cross-contours
    right_transverse = [
        "M 1360 170 C 1260 260, 1180 370, 1130 510",
        "M 1300 220 C 1200 320, 1110 440, 1050 590",
        "M 1230 280 C 1130 390, 1030 520, 970 680",
        "M 1160 350 C 1050 470, 950 600, 880 760"
    ]
    for idx, d in enumerate(right_transverse):
        right_contours.append(
            f'      <path d="{d}" stroke="url(#contourGoldToSage)" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="0.1 18" opacity="0.25" />'
        )

    # 3. Lower Mesh System (5 shallow undulating wave contours across the lower apron)
    lower_contours = []
    lower_paths = [
        "M 60 740 C 380 710, 720 780, 1060 720 S 1380 750, 1420 740",
        "M 40 770 C 360 740, 700 810, 1040 750 S 1360 780, 1440 770",
        "M 50 800 C 370 770, 710 840, 1050 780 S 1370 810, 1430 800",
        "M 30 830 C 350 800, 690 870, 1030 810 S 1350 840, 1450 830",
        "M 60 860 C 380 830, 720 900, 1060 840 S 1380 870, 1420 860"
    ]
    for idx, d in enumerate(lower_paths):
        grad = "url(#contourSageToGold)" if idx % 2 == 0 else "url(#contourGoldToSage)"
        op = 0.32 - idx * 0.04
        lower_contours.append(
            f'      <path d="{d}" stroke="{grad}" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="0.1 16" opacity="{op:.2f}" />'
        )

    # 4. Upper celestial connecting arc (whisper-thin hairline)
    celestial_arc = '      <path d="M 80 140 C 440 40, 1000 40, 1360 140" stroke="url(#contourSageToGold)" stroke-width="0.75" stroke-dasharray="3 7" opacity="0.26" />'

    all_paths = left_contours + right_contours + lower_contours + [celestial_arc]
    return '\n'.join(all_paths)

topography_markup = build_topography_svg()

hero_astro_content = """---
import config from '../data/config.json';
---

<section class="hero-section" id="home" aria-labelledby="hero-main-title">
  <!-- Micro-texture Archival Cotton Grain -->
  <div class="hero-grain" aria-hidden="true"></div>

  <!-- Organic Aurora: Large Asymmetrical Soft Light Forms (Frosted Glass Illumination) -->
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
          <stop offset="0%" stop-color="#B8CFC5" />
          <stop offset="55%" stop-color="#B89558" />
          <stop offset="100%" stop-color="#C5A86D" />
        </linearGradient>

        <linearGradient id="contourGoldToSage" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#B89558" />
          <stop offset="45%" stop-color="#C5A86D" />
          <stop offset="100%" stop-color="#B8CFC5" />
        </linearGradient>

        <!-- Frosted Ambient Gold Node Glow -->
        <radialGradient id="heroNodeGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#B89558" stop-opacity="0.85" />
          <stop offset="40%" stop-color="#B89558" stop-opacity="0.30" />
          <stop offset="100%" stop-color="#B89558" stop-opacity="0" />
        </radialGradient>

        <!-- Center Clearing Mask: Ensures crystal-clear legibility around central headline -->
        <radialGradient id="centerMaskGradient" cx="50%" cy="46%" r="58%">
          <stop offset="0%" stop-color="#000000" stop-opacity="0.04" />
          <stop offset="38%" stop-color="#ffffff" stop-opacity="0.32" />
          <stop offset="72%" stop-color="#ffffff" stop-opacity="0.90" />
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
      <circle cx="280" cy="290" r="16" fill="url(#heroNodeGlow)" opacity="0.75" />
      <circle cx="280" cy="290" r="6" stroke="#B89558" stroke-width="0.8" opacity="0.6" />
      <circle cx="280" cy="290" r="2.2" fill="#B89558" />

      <!-- Node B: Right Upper Flow (1180, 275) -->
      <circle cx="1180" cy="275" r="16" fill="url(#heroNodeGlow)" opacity="0.75" />
      <circle cx="1180" cy="275" r="6" stroke="#B89558" stroke-width="0.8" opacity="0.6" />
      <circle cx="1180" cy="275" r="2.2" fill="#B89558" />

      <!-- Node C: Left Lower Transition (420, 570) -->
      <circle cx="420" cy="570" r="14" fill="url(#heroNodeGlow)" opacity="0.6" />
      <circle cx="420" cy="570" r="5" stroke="#B89558" stroke-width="0.75" opacity="0.5" />
      <circle cx="420" cy="570" r="2.0" fill="#B89558" />

      <!-- Node D: Right Lower Transition (1040, 560) -->
      <circle cx="1040" cy="560" r="14" fill="url(#heroNodeGlow)" opacity="0.6" />
      <circle cx="1040" cy="560" r="5" stroke="#B89558" stroke-width="0.75" opacity="0.5" />
      <circle cx="1040" cy="560" r="2.0" fill="#B89558" />
    </svg>
  </div>

  <div class="container hero-content-container">
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
        <!-- Custom Handwritten Organic SVG Flourish Echoing Background Geometry -->
        <svg class="signature-flourish" aria-hidden="true" viewBox="0 0 344 28" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path 
            class="flourish-path" 
            d="M 6,19 C 52,23 110,24 168,20 C 214,17 252,13 282,12 C 298,11.5 312,14 308,18.5 C 304,22.5 290,21.5 298,15 C 304,10 322,7.5 338,7" 
            stroke="#B89558" 
            stroke-width="2.2" 
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
     HERO SECTION: ORGANIC AURORA × LIVING TOPOGRAPHY
     Color Palette:
     - 70% Porcelain Ivory Canvas: #F7F6F2
     - 20% Midnight Navy Type & CTA: #19304B
     - 10% Muted Champagne Gold Accent: #B89558
     - Atmospheric Soft Sage Tint: #B8CFC5
     - Supporting Copy Slate: #596879
     ========================================================= */

  .hero-section {
    position: relative;
    min-height: 100svh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #F7F6F2;
    /* Organic Aurora Multi-Zone Atmospheric Illumination */
    background-image: 
      /* Upper-left: pale champagne illumination fading into ivory */
      radial-gradient(ellipse 55% 45% at 8% 8%, rgba(184, 149, 88, 0.22) 0%, transparent 55%),
      /* Left-middle: soft sage-green atmospheric glow */
      radial-gradient(ellipse 60% 50% at 10% 45%, rgba(184, 207, 197, 0.34) 0%, transparent 58%),
      /* Lower-left: warmer gold haze blending into pale sage wave */
      radial-gradient(ellipse 50% 42% at 18% 88%, rgba(184, 149, 88, 0.25) 0%, rgba(184, 207, 197, 0.16) 42%, transparent 65%),
      /* Upper-right: very faint sage tint */
      radial-gradient(ellipse 45% 35% at 92% 12%, rgba(184, 207, 197, 0.20) 0%, transparent 50%),
      /* Lower-right: complementary champagne-and-sage illumination */
      radial-gradient(ellipse 55% 45% at 86% 75%, rgba(184, 149, 88, 0.26) 0%, rgba(184, 207, 197, 0.18) 45%, transparent 65%),
      /* Center: predominantly clean ivory with a very subtle ambient wash */
      radial-gradient(circle at 50% 38%, rgba(247, 246, 242, 0.94) 0%, rgba(247, 246, 242, 0.60) 45%, transparent 72%);
    padding: clamp(140px, 18svh, 190px) 24px clamp(80px, 12svh, 120px);
    overflow: hidden;
  }

  /* Micro-texture Archival Cotton Paper Grain */
  .hero-grain {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    opacity: 0.032;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    mix-blend-mode: multiply;
  }

  /* Organic Aurora: Large Asymmetrical Frosted Light Forms */
  .hero-aurora-form {
    position: absolute;
    pointer-events: none;
    z-index: 1;
  }

  /* Left-side form: Large, partially cropped along left edge */
  .hero-aurora-left {
    top: 8%;
    left: clamp(-220px, -15vw, -160px);
    width: clamp(540px, 50vw, 740px);
    height: clamp(540px, 50vw, 740px);
    border-radius: 44% 56% 58% 42% / 46% 50% 50% 54%;
    background: radial-gradient(
      ellipse 65% 55% at 54% 48%,
      rgba(255, 253, 248, 0.75) 0%,
      rgba(184, 207, 197, 0.46) 26%,
      rgba(184, 149, 88, 0.30) 56%,
      rgba(184, 207, 197, 0.14) 76%,
      transparent 100%
    );
    filter: blur(55px);
  }

  /* Lower-left: Diffused sage and gold blending into the mesh */
  .hero-aurora-left-lower {
    bottom: -90px;
    left: clamp(-80px, -5vw, -40px);
    width: clamp(440px, 42vw, 600px);
    height: clamp(440px, 42vw, 600px);
    border-radius: 50% 50% 45% 55% / 55% 45% 55% 45%;
    background: radial-gradient(
      circle at 50% 50%,
      rgba(184, 207, 197, 0.44) 0%,
      rgba(184, 149, 88, 0.30) 48%,
      rgba(184, 207, 197, 0.12) 72%,
      transparent 100%
    );
    filter: blur(50px);
  }

  /* Right-side form: Complementary form near right edge */
  .hero-aurora-right {
    top: 10%;
    right: clamp(-210px, -14vw, -150px);
    width: clamp(500px, 46vw, 680px);
    height: clamp(500px, 46vw, 680px);
    border-radius: 56% 44% 48% 52% / 50% 54% 46% 50%;
    background: radial-gradient(
      ellipse 62% 54% at 48% 50%,
      rgba(255, 253, 248, 0.70) 0%,
      rgba(184, 149, 88, 0.42) 28%,
      rgba(184, 207, 197, 0.32) 58%,
      rgba(184, 149, 88, 0.12) 78%,
      transparent 100%
    );
    filter: blur(55px);
  }

  /* Lower-right: Ambient warm illumination */
  .hero-aurora-right-lower {
    bottom: -70px;
    right: clamp(15px, 3vw, 60px);
    width: clamp(380px, 36vw, 520px);
    height: clamp(380px, 36vw, 520px);
    border-radius: 50%;
    background: radial-gradient(
      circle at 50% 50%,
      rgba(184, 149, 88, 0.34) 0%,
      rgba(184, 207, 197, 0.22) 50%,
      transparent 75%
    );
    filter: blur(52px);
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

  /* Central Content Composition */
  .hero-content-container {
    position: relative;
    z-index: 3;
    max-width: 960px;
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
    margin-bottom: clamp(24px, 4vh, 36px);
  }

  .eyebrow-rule {
    display: inline-block;
    width: 32px;
    height: 1px;
    background-color: #B89558;
    opacity: 0.85;
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

  .signature-word {
    font-family: 'Instrument Serif', 'DM Serif Display', Georgia, serif;
    font-style: italic;
    color: #B89558;
    padding-right: 0.05em;
  }

  /* Custom Handwritten Signature Flourish Underline */
  .signature-flourish {
    position: absolute;
    left: -3%;
    bottom: -15px;
    width: 106%;
    height: 24px;
    pointer-events: none;
    overflow: visible;
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
    padding: 0 36px;
    border-radius: 12px;
    border: 1px solid rgba(25, 48, 75, 0.2);
    box-shadow: 
      0 4px 14px rgba(25, 48, 75, 0.12),
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
      0 8px 24px rgba(25, 48, 75, 0.20),
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

  /* Mobile and Responsive Adaptations */
  @media (max-width: 768px) {
    .hero-section {
      padding-top: 130px;
      padding-bottom: 70px;
      min-height: auto;
    }

    .hero-aurora-left {
      width: 320px;
      height: 320px;
      left: -120px;
      filter: blur(40px);
      opacity: 0.8;
    }

    .hero-aurora-right {
      width: 300px;
      height: 300px;
      right: -120px;
      filter: blur(40px);
      opacity: 0.8;
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

print(f"Living Topography Hero.astro generated successfully! Total contour elements: {topography_markup.count('<path')}")
