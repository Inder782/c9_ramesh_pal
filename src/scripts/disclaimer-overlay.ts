  const overlay = document.getElementById('onboarding-overlay');
  const btn = document.getElementById('onboarding-btn');

  if (overlay && btn) {
    const trapFocus = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        e.preventDefault();
        btn.focus();
      }
    };

    if (!window.location.search.includes('bypass_disclaimer')) {
      if (!sessionStorage.getItem('rameshpal-disclaimer-acknowledged')) {
        overlay.classList.add('show');
        document.body.style.overflow = 'hidden';
        document.addEventListener('keydown', trapFocus);
        setTimeout(() => btn.focus(), 100);
      }
    }
    
    btn.addEventListener('click', () => {
      sessionStorage.setItem('rameshpal-disclaimer-acknowledged', 'true');
      overlay.classList.remove('show');
      document.body.style.overflow = '';
      document.removeEventListener('keydown', trapFocus);
      
      const skipLink = document.querySelector('.skip-link') as HTMLElement | null;
      if (skipLink) {
        skipLink.focus();
      }
    });
  }
