import math
import os

curves = [
    # Left flank waves
    (18, (-20, 160), (120, 190), (280, 360), (420, 520), 1.5, True),
    (18, (-30, 220), (100, 260), (250, 420), (380, 590), 1.4, False),
    (18, (-20, 290), (110, 340), (240, 490), (360, 660), 1.3, True),
    (18, (-40, 370), (90, 420), (220, 570), (340, 730), 1.2, False),
    (16, (-20, 460), (80, 510), (200, 650), (320, 800), 1.3, True),
    (14, (-30, 560), (70, 610), (180, 730), (290, 860), 1.2, False),
    
    # Right flank waves
    (18, (1460, 150), (1320, 190), (1160, 370), (1020, 530), 1.5, True),
    (18, (1470, 210), (1340, 260), (1190, 430), (1060, 600), 1.4, False),
    (18, (1460, 280), (1330, 340), (1200, 500), (1080, 670), 1.3, True),
    (18, (1480, 360), (1350, 420), (1220, 580), (1100, 740), 1.2, False),
    (16, (1460, 450), (1360, 510), (1240, 660), (1120, 810), 1.3, True),
    (14, (1470, 550), (1370, 610), (1260, 740), (1150, 870), 1.2, False),

    # Lower undulating base
    (24, (200, 820), (450, 750), (990, 870), (1240, 790), 1.2, False),
    (22, (260, 860), (520, 790), (920, 910), (1180, 830), 1.1, True),
]

dots_svg = []
for pts_count, start, ctrl1, ctrl2, end, r_base, is_gold_lead in curves:
    for i in range(pts_count):
        t = i / (pts_count - 1)
        x = (1-t)**3 * start[0] + 3*(1-t)**2*t * ctrl1[0] + 3*(1-t)*t**2 * ctrl2[0] + t**3 * end[0]
        y = (1-t)**3 * start[1] + 3*(1-t)**2*t * ctrl1[1] + 3*(1-t)*t**2 * ctrl2[1] + t**3 * end[1]
        
        if is_gold_lead:
            col = '#B89558' if i % 3 != 0 else '#B8CFC5'
        else:
            col = '#B8CFC5' if i % 3 != 0 else '#B89558'
            
        r = r_base + 0.3 * math.sin(t * math.pi)
        edge_dist = min(t, 1-t) * 2
        op = (0.22 + 0.34 * edge_dist) * (0.85 if col == '#B8CFC5' else 0.95)
        dots_svg.append(f'      <circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" opacity="{op:.2f}" />')

dots_block = '\n'.join(dots_svg)

template = """---
import config from '../data/config.json';
---

<section class="hero-section" id="home" aria-labelledby="hero-main-title">
  <!-- Micro-texture Paper Grain -->
  <div class="hero-grain" aria-hidden="true"></div>

  <!-- Translucent Ambient Glowing Orbs -->
  <div class="hero-orb hero-orb-a" aria-hidden="true"></div>
  <div class="hero-orb hero-orb-b" aria-hidden="true"></div>
  <div class="hero-orb hero-orb-c" aria-hidden="true"></div>
  <div class="hero-orb hero-orb-d" aria-hidden="true"></div>

  <!-- Generative Dotted Mesh Waves & Orbital Curves -->
  <div class="hero-mesh-wrapper" aria-hidden="true">
    <svg class="hero-mesh-svg" viewBox="0 0 1440 900" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <radialGradient id="heroNodeGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#B89558" stop-opacity="0.75" />
          <stop offset="50%" stop-color="#B89558" stop-opacity="0.20" />
          <stop offset="100%" stop-color="#B89558" stop-opacity="0" />
        </radialGradient>
      </defs>

      <!-- Delicate Orbital Paths -->
      <path d="M -60 340 C 200 220, 420 360, 540 520" stroke="#B89558" stroke-width="0.85" stroke-dasharray="3 5" opacity="0.32" />
      <path d="M 900 520 C 1020 360, 1240 240, 1500 320" stroke="#B89558" stroke-width="0.85" stroke-dasharray="3 5" opacity="0.32" />
      <path d="M 120 180 C 380 110, 1060 110, 1320 180" stroke="#B8CFC5" stroke-width="0.75" stroke-dasharray="2 6" opacity="0.38" />

      <!-- Illuminated Gold Node Points -->
      <circle cx="330" cy="285" r="14" fill="url(#heroNodeGlow)" />
      <circle cx="330" cy="285" r="6" stroke="#B89558" stroke-width="0.75" opacity="0.5" />
      <circle cx="330" cy="285" r="2.5" fill="#B89558" />

      <circle cx="1110" cy="305" r="14" fill="url(#heroNodeGlow)" />
      <circle cx="1110" cy="305" r="6" stroke="#B89558" stroke-width="0.75" opacity="0.5" />
      <circle cx="1110" cy="305" r="2.5" fill="#B89558" />

      <circle cx="210" cy="620" r="12" fill="url(#heroNodeGlow)" />
      <circle cx="210" cy="620" r="5" stroke="#B89558" stroke-width="0.75" opacity="0.45" />
      <circle cx="210" cy="620" r="2" fill="#B89558" />

      <circle cx="1230" cy="590" r="12" fill="url(#heroNodeGlow)" />
      <circle cx="1230" cy="590" r="5" stroke="#B89558" stroke-width="0.75" opacity="0.45" />
      <circle cx="1230" cy="590" r="2" fill="#B89558" />

      <!-- Flowing Dotted Mesh Field -->
__DOTS_BLOCK__
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

    <!-- Centered Editorial Headline with Signature Flourish -->
    <h1 class="hero-title" id="hero-main-title">
      <span class="title-line">Repeat a Pattern</span>
      <span class="title-line">Until It Becomes Your</span>
      <span class="title-line signature-wrapper">
        <span class="signature-word">Signature.</span>
        <svg class="signature-flourish" aria-hidden="true" viewBox="0 0 280 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path class="flourish-path" d="M 4,15 C 42,19 98,20 162,16 C 206,13 246,9 276,6" stroke="#B89558" stroke-width="2.75" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </span>
    </h1>

    <!-- Single Refined Supporting Statement -->
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
     HERO SECTION: EDITORIAL LUXURY & GENERATIVE DESIGN
     Palette:
     - 70% Porcelain Ivory: #F7F6F2
     - 20% Midnight Navy: #19304B
     - 10% Champagne Gold: #B89558
     - Atmospheric Sage: #B8CFC5
     - Supporting Slate: #596879
     ========================================================= */

  .hero-section {
    position: relative;
    min-height: 100svh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #F7F6F2;
    padding: clamp(140px, 18svh, 190px) 24px clamp(80px, 12svh, 120px);
    overflow: hidden;
  }

  /* Micro-texture Grain Overlay */
  .hero-grain {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    opacity: 0.035;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    mix-blend-mode: multiply;
  }

  /* 4 Ambient Glowing Orbs */
  .hero-orb {
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
    z-index: 1;
  }

  .hero-orb-a {
    top: 4%;
    left: -8%;
    width: clamp(380px, 42vw, 560px);
    height: clamp(380px, 42vw, 560px);
    background: radial-gradient(circle at 45% 45%, rgba(184, 149, 88, 0.22) 0%, rgba(184, 207, 197, 0.14) 50%, transparent 72%);
    filter: blur(85px);
  }

  .hero-orb-b {
    bottom: 2%;
    left: 4%;
    width: clamp(340px, 38vw, 480px);
    height: clamp(340px, 38vw, 480px);
    background: radial-gradient(circle at 50% 50%, rgba(184, 207, 197, 0.24) 0%, rgba(184, 149, 88, 0.12) 55%, transparent 70%);
    filter: blur(90px);
  }

  .hero-orb-c {
    top: 6%;
    right: -6%;
    width: clamp(360px, 40vw, 520px);
    height: clamp(360px, 40vw, 520px);
    background: radial-gradient(circle at 55% 45%, rgba(184, 207, 197, 0.22) 0%, rgba(184, 149, 88, 0.14) 50%, transparent 72%);
    filter: blur(85px);
  }

  .hero-orb-d {
    bottom: 4%;
    right: 5%;
    width: clamp(320px, 36vw, 460px);
    height: clamp(320px, 36vw, 460px);
    background: radial-gradient(circle at 50% 50%, rgba(184, 149, 88, 0.20) 0%, rgba(184, 207, 197, 0.15) 50%, transparent 70%);
    filter: blur(80px);
  }

  /* Generative Mesh Wrapper */
  .hero-mesh-wrapper {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 2;
    overflow: hidden;
  }

  .hero-mesh-svg {
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
    font-family: 'Instrument Serif', Georgia, serif;
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
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    color: #B89558;
    padding-right: 0.05em;
  }

  /* Hand-Drawn SVG Signature Flourish Underline */
  .signature-flourish {
    position: absolute;
    left: -4%;
    bottom: -14px;
    width: 108%;
    height: 24px;
    pointer-events: none;
    overflow: visible;
  }

  .flourish-path {
    stroke-dasharray: 290;
    stroke-dashoffset: 290;
    animation: drawFlourish 1.1s cubic-bezier(0.22, 1, 0.36, 1) 0.35s forwards;
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
      bottom: -10px;
      height: 18px;
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

final_content = template.replace('__DOTS_BLOCK__', dots_block)

target_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'components', 'Hero.astro')
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f"Successfully generated {target_path}")
