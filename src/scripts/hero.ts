  function initHeroInteractivePointer() {
    // Only enable interactive pointer spotlight on devices that support hover (desktop / fine pointer)
    // Completely disable on mobile / touch devices to guarantee maximum battery & fluid performance
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      return;
    }

    const hero = document.getElementById('home');
    if (!hero) return;

    let rafId = null;
    let targetX = 0;
    let targetY = 0;

    const handlePointerMove = (e) => {
      const rect = hero.getBoundingClientRect();
      targetX = e.clientX - rect.left;
      targetY = e.clientY - rect.top;
      hero.style.setProperty('--mouse-active', '1');

      if (!rafId) {
        rafId = requestAnimationFrame(() => {
          hero.style.setProperty('--mouse-x', `${targetX}px`);
          hero.style.setProperty('--mouse-y', `${targetY}px`);
          rafId = null;
        });
      }
    };

    const handlePointerLeave = () => {
      hero.style.setProperty('--mouse-active', '0.65');
    };

    hero.addEventListener('pointermove', handlePointerMove, { passive: true });
    hero.addEventListener('pointerleave', handlePointerLeave, { passive: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHeroInteractivePointer);
  } else {
    initHeroInteractivePointer();
  }
  document.addEventListener('astro:page-load', initHeroInteractivePointer);
