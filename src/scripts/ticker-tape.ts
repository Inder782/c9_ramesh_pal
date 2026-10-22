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
      displayMode: "regular",
      locale: "in"
    });
    container.appendChild(script);
  }

  function initTickerControl() {
    loadTradingViewWidget();

    const wrapper = document.getElementById('ticker-wrapper');
    const toggleBtn = document.getElementById('ticker-toggle-btn');
    const btnText = document.getElementById('ticker-btn-text');
    const announcer = document.getElementById('ticker-status-announcer');
    const pausedOverlay = document.getElementById('ticker-paused-overlay');

    if (!wrapper || !toggleBtn) return;

    let isPaused = false;

    function setPaused(paused: boolean) {
      isPaused = paused;
      if (isPaused) {
        wrapper?.classList.add('ticker-paused');
        toggleBtn?.setAttribute('aria-pressed', 'true');
        toggleBtn?.setAttribute('aria-label', 'Resume scrolling stock ticker');
        toggleBtn?.setAttribute('title', 'Resume scrolling stock ticker');
        if (btnText) btnText.textContent = 'Resume';
        if (announcer) announcer.textContent = 'Stock ticker paused';
      } else {
        wrapper?.classList.remove('ticker-paused');
        toggleBtn?.setAttribute('aria-pressed', 'false');
        toggleBtn?.setAttribute('aria-label', 'Pause scrolling stock ticker');
        toggleBtn?.setAttribute('title', 'Pause scrolling stock ticker');
        if (btnText) btnText.textContent = 'Pause';
        if (announcer) announcer.textContent = 'Stock ticker is scrolling';
      }
    }

    toggleBtn.addEventListener('click', (e) => {
      e.preventDefault();
      setPaused(!isPaused);
    });

    if (pausedOverlay) {
      pausedOverlay.addEventListener('click', () => {
        setPaused(false);
        toggleBtn.focus();
      });
      pausedOverlay.addEventListener('keydown', (e: KeyboardEvent) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          setPaused(false);
          toggleBtn.focus();
        }
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
