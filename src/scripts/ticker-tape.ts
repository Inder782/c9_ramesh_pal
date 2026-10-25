  function loadTradingViewWidget() {
    const container = document.getElementById('tv-ticker-container');
    if (!container || container.querySelector('script')) return;

    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js';
    script.async = true;
    script.innerHTML = JSON.stringify({
      symbols: [
        { proName: "BSE:SENSEX", title: "S&P BSE SENSEX" },
        { proName: "BSE:SBIN", title: "State Bank of India" },
        { proName: "BSE:RELIANCE", title: "Reliance" },
        { proName: "BSE:HDFCBANK", title: "HDFC Bank" },
        { proName: "BSE:TCS", title: "TCS" },
        { proName: "BSE:INFY", title: "Infosys" },
        { proName: "BSE:ICICIBANK", title: "ICICI Bank" },
        { proName: "BSE:LT", title: "L&T" },
        { proName: "BSE:BHARTIARTL", title: "Bharti Airtel" },
        { proName: "BSE:ITC", title: "ITC" }
      ],
      showSymbolLogo: true,
      colorTheme: "dark",
      isTransparent: true,
      displayMode: "adaptive",
      locale: "in"
    });
    container.appendChild(script);

    // Apply descriptive title and relative scalable sizing to TradingView iframe per WCAG 1.4.4 & 4.1.2
    const applyIframeAccessibility = () => {
      const iframes = container.querySelectorAll('iframe');
      iframes.forEach((iframe) => {
        if (iframe.getAttribute('title') !== 'Live market ticker') {
          iframe.setAttribute('title', 'Live market ticker');
          iframe.setAttribute('aria-label', 'Live market ticker showing BSE S&P Sensex and major equities');
        }
        iframe.style.minHeight = '3.75rem';
        iframe.style.height = '100%';
        iframe.style.width = '100%';
      });
    };

    const observer = new MutationObserver(() => {
      applyIframeAccessibility();
    });
    observer.observe(container, { childList: true, subtree: true });

    const pollTimer = setInterval(() => {
      if (container.querySelector('iframe')) {
        applyIframeAccessibility();
        clearInterval(pollTimer);
      }
    }, 100);
    setTimeout(() => clearInterval(pollTimer), 10000);
  }

  function initTickerControl() {
    loadTradingViewWidget();

    const wrapper = document.getElementById('ticker-wrapper');
    const toggleBtn = document.getElementById('ticker-toggle-btn');
    const btnText = document.getElementById('ticker-btn-text');
    const announcer = document.getElementById('ticker-status-announcer');
    const resumeOverlayBtn = document.getElementById('ticker-resume-overlay-btn');

    if (!wrapper || !toggleBtn) return;

    let isPaused = false;

    function setPaused(paused: boolean) {
      isPaused = paused;
      if (isPaused) {
        wrapper?.classList.add('ticker-paused');
        toggleBtn?.setAttribute('aria-pressed', 'true');
        toggleBtn?.setAttribute('aria-label', 'Play ticker');
        toggleBtn?.setAttribute('title', 'Play ticker');
        if (btnText) btnText.textContent = 'Play ticker';
        if (announcer) announcer.textContent = 'Stock ticker paused. All movement stopped.';
      } else {
        wrapper?.classList.remove('ticker-paused');
        toggleBtn?.setAttribute('aria-pressed', 'false');
        toggleBtn?.setAttribute('aria-label', 'Pause ticker');
        toggleBtn?.setAttribute('title', 'Pause ticker');
        if (btnText) btnText.textContent = 'Pause ticker';
        if (announcer) announcer.textContent = 'Stock ticker is scrolling.';
      }
    }

    toggleBtn.addEventListener('click', (e) => {
      e.preventDefault();
      setPaused(!isPaused);
    });

    toggleBtn.addEventListener('keydown', (e: KeyboardEvent) => {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
        setPaused(!isPaused);
      }
    });

    if (resumeOverlayBtn) {
      resumeOverlayBtn.addEventListener('click', () => {
        setPaused(false);
        toggleBtn.focus();
      });
    }

    // Support prefers-reduced-motion
    const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (motionQuery.matches) {
      setPaused(true);
    }
  }

  document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', initTickerControl)
    : initTickerControl();
