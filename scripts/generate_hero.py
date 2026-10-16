import math
import os

def generate_mesh_dots():
    dots = []
    
    # 1. Left Mesh Ribbon: 8 layered continuous spline waves entering from left flank
    for k in range(8):
        pts_count = 45
        # Control points for line k
        p0 = (-40, 90 + k * 44)
        p1 = (140 + k * 18, 150 + k * 48)
        p2 = (340 + k * 14, 390 + k * 40)
        p3 = (530 + k * 10, 670 + k * 26)
        
        lead_gold = (k % 2 == 0)
        
        for i in range(pts_count):
            t = i / (pts_count - 1)
            x = (1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
            
            # Color alternating between Champagne Gold (#B89558) and Soft Sage (#B8CFC5)
            if lead_gold:
                col = '#B89558' if (i + k) % 3 != 0 else '#B8CFC5'
            else:
                col = '#B8CFC5' if (i + k) % 3 != 0 else '#B89558'
                
            # Opacity: dense & visible near edge (0.62), tapering gracefully toward center (0.07)
            base_op = 0.62 * (1.0 - 0.85 * (t ** 1.35))
            # Harmonic sine wave micro-variation for organic silk look
            base_op *= (0.88 + 0.12 * math.sin(i * 0.45))
            op = max(0.06, min(0.68, base_op))
            
            r = 1.65 - 0.55 * t
            dots.append(f'      <circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" opacity="{op:.2f}" />')

    # 2. Right Mesh Ribbon: 8 layered continuous spline waves entering from right flank
    for k in range(8):
        pts_count = 45
        p0 = (1480, 80 + k * 44)
        p1 = (1300 - k * 18, 140 + k * 48)
        p2 = (1100 - k * 14, 380 + k * 40)
        p3 = (910 - k * 10, 660 + k * 26)
        
        lead_gold = (k % 2 != 0)
        
        for i in range(pts_count):
            t = i / (pts_count - 1)
            x = (1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
            
            if lead_gold:
                col = '#B89558' if (i + k) % 3 != 0 else '#B8CFC5'
            else:
                col = '#B8CFC5' if (i + k) % 3 != 0 else '#B89558'
                
            base_op = 0.62 * (1.0 - 0.85 * (t ** 1.35))
            base_op *= (0.88 + 0.12 * math.sin(i * 0.45))
            op = max(0.06, min(0.68, base_op))
            
            r = 1.65 - 0.55 * t
            dots.append(f'      <circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" opacity="{op:.2f}" />')

    # 3. Lower Undulation Wave Field: 4 undulating horizontal wave contours across the lower apron
    for k in range(4):
        pts_count = 40
        base_y = 740 + k * 30
        for i in range(pts_count):
            t = i / (pts_count - 1)
            x = 80 + t * 1280
            # Double sine wave modulation
            y = base_y + 22 * math.sin(t * 2.8 * math.pi + k * 0.4) + 8 * math.cos(t * 4.2 * math.pi)
            
            col = '#B89558' if (i + k) % 2 == 0 else '#B8CFC5'
            edge_dist = min(t, 1-t) * 2
            op = (0.16 + 0.28 * edge_dist) * (0.85 if col == '#B8CFC5' else 0.95)
            r = 1.1 + 0.3 * edge_dist
            dots.append(f'      <circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" opacity="{op:.2f}" />')

    return '\n'.join(dots)

dots_markup = generate_mesh_dots()

hero_astro_content = """---
import config from '../data/config.json';
---

<section class="hero-section" id="home" aria-labelledby="hero-main-title">
  <!-- Micro-texture Archival Paper Grain -->
  <div class="hero-grain" aria-hidden="true"></div>

  <!-- Large Prominent Ambient Glowing Light Forms (Frosted Glass Illumination) -->
  <div class="hero-orb hero-orb-left-main" aria-hidden="true"></div>
  <div class="hero-orb hero-orb-left-lower" aria-hidden="true"></div>
  <div class="hero-orb hero-orb-right-main" aria-hidden="true"></div>
  <div class="hero-orb hero-orb-right-lower" aria-hidden="true"></div>

  <!-- Continuous Flowing Dotted Mesh Waves & Celestial Orbital Paths -->
  <div class="hero-mesh-wrapper" aria-hidden="true">
    <svg class="hero-mesh-svg" viewBox="0 0 1440 900" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <!-- Frosted Ambient Gold Node Glow -->
        <radialGradient id="heroNodeGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#B89558" stop-opacity="0.85" />
          <stop offset="40%" stop-color="#B89558" stop-opacity="0.30" />
          <stop offset="100%" stop-color="#B89558" stop-opacity="0" />
        </radialGradient>
      </defs>

      <!-- Continuous Hairline Orbital & Contour Curves -->
      <path d="M -40 180 C 180 240, 380 440, 540 700" stroke="#B89558" stroke-width="0.85" stroke-dasharray="3 5" opacity="0.35" />
      <path d="M -30 260 C 160 330, 350 510, 490 750" stroke="#B8CFC5" stroke-width="0.75" stroke-dasharray="2 6" opacity="0.38" />
      <path d="M 1480 170 C 1260 230, 1060 430, 900 690" stroke="#B89558" stroke-width="0.85" stroke-dasharray="3 5" opacity="0.35" />
      <path d="M 1470 250 C 1280 320, 1090 500, 950 740" stroke="#B8CFC5" stroke-width="0.75" stroke-dasharray="2 6" opacity="0.38" />
      <path d="M 100 140 C 400 60, 1040 60, 1340 140" stroke="#B89558" stroke-width="0.75" stroke-dasharray="3 7" opacity="0.28" />

      <!-- Illuminated Gold Node Points with Frosted Halos -->
      <!-- Node A: Left Ribbon -->
      <circle cx="260" cy="305" r="16" fill="url(#heroNodeGlow)" opacity="0.7" />
      <circle cx="260" cy="305" r="6" stroke="#B89558" stroke-width="0.8" opacity="0.55" />
      <circle cx="260" cy="305" r="2.5" fill="#B89558" />

      <!-- Node B: Right Ribbon -->
      <circle cx="1180" cy="295" r="16" fill="url(#heroNodeGlow)" opacity="0.7" />
      <circle cx="1180" cy="295" r="6" stroke="#B89558" stroke-width="0.8" opacity="0.55" />
      <circle cx="1180" cy="295" r="2.5" fill="#B89558" />

      <!-- Node C: Lower Left Wave -->
      <circle cx="410" cy="550" r="14" fill="url(#heroNodeGlow)" opacity="0.6" />
      <circle cx="410" cy="550" r="5" stroke="#B89558" stroke-width="0.75" opacity="0.5" />
      <circle cx="410" cy="550" r="2.2" fill="#B89558" />

      <!-- Node D: Lower Right Wave -->
      <circle cx="1030" cy="540" r="14" fill="url(#heroNodeGlow)" opacity="0.6" />
      <circle cx="1030" cy="540" r="5" stroke="#B89558" stroke-width="0.75" opacity="0.5" />
      <circle cx="1030" cy="540" r="2.2" fill="#B89558" />

      <!-- Flowing Dotted Mesh Wave Ribbons -->
__DOTS_MARKUP__
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

    <!-- Centered Editorial Headline with Custom Handwritten Signature Flourish -->
    <h1 class="hero-title" id="hero-main-title">
      <span class="title-line">Repeat a Pattern</span>
      <span class="title-line">Until It Becomes Your</span>
      <span class="title-line signature-wrapper">
        <span class="signature-word">Signature.</span>
        <!-- Custom Handwritten Organic SVG Flourish with Signature Loop & Trail -->
        <svg class="signature-flourish" aria-hidden="true" viewBox="0 0 348 38" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path 
            class="flourish-path" 
            d="M 6,24 C 50,28 105,29 165,25 C 215,21.5 258,16 288,14 C 304,13 314,16 310,22 C 305,28 284,27 292,18 C 298,11 324,8 342,7" 
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
     HERO SECTION: REFINED EDITORIAL LUXURY & GENERATIVE DESIGN
     Palette:
     - 70% Porcelain Ivory Canvas: #F7F6F2
     - 20% Midnight Navy UI & Type: #19304B
     - 10% Champagne Gold Accent: #B89558
     - Atmospheric Sage Tint: #B8CFC5
     - Supporting Copy Slate: #596879
     ========================================================= */

  .hero-section {
    position: relative;
    min-height: 100svh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #F7F6F2;
    /* Atmospheric background lighting: subtle sage and champagne radial glow */
    background-image: 
      radial-gradient(ellipse 65% 55% at 12% 25%, rgba(184, 207, 197, 0.38) 0%, transparent 62%),
      radial-gradient(ellipse 60% 50% at 88% 30%, rgba(184, 149, 88, 0.30) 0%, transparent 60%),
      radial-gradient(ellipse 70% 45% at 50% 92%, rgba(184, 207, 197, 0.24) 0%, transparent 65%),
      radial-gradient(circle at 50% 28%, rgba(247, 246, 242, 0.92) 0%, transparent 70%);
    padding: clamp(140px, 18svh, 190px) 24px clamp(80px, 12svh, 120px);
    overflow: hidden;
  }

  /* Micro-texture Archival Paper Grain */
  .hero-grain {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    opacity: 0.035;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    mix-blend-mode: multiply;
  }

  /* Large Prominent Ambient Glowing Light Forms (Frosted Glass Diffused Effect) */
  .hero-orb {
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
    z-index: 1;
  }

  /* Orb 1: Upper/Middle Left Edge - Pale sage interior, ivory highlight, champagne glow */
  .hero-orb-left-main {
    top: 6%;
    left: clamp(-220px, -14vw, -160px);
    width: clamp(520px, 48vw, 720px);
    height: clamp(520px, 48vw, 720px);
    background: radial-gradient(
      circle at 48% 44%,
      rgba(255, 253, 248, 0.75) 0%,
      rgba(184, 207, 197, 0.48) 25%,
      rgba(184, 149, 88, 0.32) 55%,
      rgba(184, 207, 197, 0.15) 75%,
      transparent 100%
    );
    filter: blur(52px);
  }

  /* Orb 2: Lower-Left Edge - Diffused sage and gold blending into the mesh */
  .hero-orb-left-lower {
    bottom: -110px;
    left: clamp(-90px, -6vw, -50px);
    width: clamp(440px, 42vw, 620px);
    height: clamp(440px, 42vw, 620px);
    background: radial-gradient(
      circle at 50% 50%,
      rgba(184, 207, 197, 0.46) 0%,
      rgba(184, 149, 88, 0.32) 48%,
      rgba(184, 207, 197, 0.12) 72%,
      transparent 100%
    );
    filter: blur(50px);
  }

  /* Orb 3: Upper-Right Flank - Muted gold center, pale ivory highlight, subtle sage tint */
  .hero-orb-right-main {
    top: 9%;
    right: clamp(-220px, -14vw, -160px);
    width: clamp(500px, 46vw, 690px);
    height: clamp(500px, 46vw, 690px);
    background: radial-gradient(
      circle at 52% 46%,
      rgba(255, 253, 248, 0.72) 0%,
      rgba(184, 149, 88, 0.46) 28%,
      rgba(184, 207, 197, 0.34) 58%,
      rgba(184, 149, 88, 0.14) 78%,
      transparent 100%
    );
    filter: blur(52px);
  }

  /* Orb 4: Lower-Right Edge - Warm gold and sage ambient illumination */
  .hero-orb-right-lower {
    bottom: -80px;
    right: clamp(10px, 3vw, 60px);
    width: clamp(400px, 38vw, 540px);
    height: clamp(400px, 38vw, 540px);
    background: radial-gradient(
      circle at 50% 50%,
      rgba(184, 149, 88, 0.36) 0%,
      rgba(184, 207, 197, 0.24) 52%,
      transparent 75%
    );
    filter: blur(52px);
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
    left: -4%;
    bottom: -15px;
    width: 108%;
    height: 28px;
    pointer-events: none;
    overflow: visible;
  }

  .flourish-path {
    stroke-dasharray: 420;
    stroke-dashoffset: 420;
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

    .hero-orb-left-main {
      width: 320px;
      height: 320px;
      left: -120px;
      filter: blur(40px);
      opacity: 0.8;
    }

    .hero-orb-right-main {
      width: 300px;
      height: 300px;
      right: -120px;
      filter: blur(40px);
      opacity: 0.8;
    }

    .hero-orb-left-lower,
    .hero-orb-right-lower {
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

final_astro = hero_astro_content.replace('__DOTS_MARKUP__', dots_markup)

target_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'components', 'Hero.astro')
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(final_astro)

print(f"Refined Hero.astro generated successfully! Total mesh dots: {dots_markup.count('<circle')}")
