// High-Precision Sliding Pill & Contrast Synchronizer
  const navList = document.getElementById('main-nav-list');
  const slidingPill = document.getElementById('sliding-pill');
  const links = document.querySelectorAll<HTMLAnchorElement>('.desktop-nav .nav-link');

  let currentActiveSectionLink: HTMLElement | null = document.querySelector('.desktop-nav .nav-link.pill-active') || links[0] || null;
  let isHovering = false;

  function movePillTo(element: HTMLElement) {
    if (!slidingPill || !navList) return;
    const navRect = navList.getBoundingClientRect();
    const linkRect = element.getBoundingClientRect();

    slidingPill.style.width = `${linkRect.width}px`;
    slidingPill.style.transform = `translateX(${linkRect.left - navRect.left - 4}px)`;
    slidingPill.style.opacity = '1';
  }

  // Highlights a target link: moves the pill, turns target text white, all other links revert to crisp Slate 900
  function highlightLink(target: HTMLElement | null) {
    if (!target) return;
    links.forEach(l => l.classList.remove('pill-active'));
    target.classList.add('pill-active');
    movePillTo(target);
  }

  // Updates the persistent active section (from scroll or click)
  function setActiveSection(target: HTMLElement | null) {
    if (!target) return;
    currentActiveSectionLink = target;
    links.forEach(l => l.classList.remove('section-active'));
    target.classList.add('section-active');
    if (!isHovering) {
      highlightLink(target);
    }
  }

  // Initialize
  if (currentActiveSectionLink) {
    setActiveSection(currentActiveSectionLink);
    // Microtask to ensure layout is computed
    setTimeout(() => {
      if (currentActiveSectionLink) highlightLink(currentActiveSectionLink);
    }, 50);
  }

  links.forEach(link => {
    link.addEventListener('mouseenter', () => {
      isHovering = true;
      highlightLink(link);
    });

    link.addEventListener('focus', () => {
      isHovering = true;
      highlightLink(link);
    });

    link.addEventListener('click', () => {
      setActiveSection(link);
      highlightLink(link);
    });
  });

  if (navList) {
    navList.addEventListener('mouseleave', () => {
      isHovering = false;
      if (currentActiveSectionLink) {
        highlightLink(currentActiveSectionLink);
      }
    });
  }

  // Resize handler to recalculate pill geometry
  window.addEventListener('resize', () => {
    const target = isHovering 
      ? document.querySelector<HTMLElement>('.desktop-nav .nav-link.pill-active') 
      : currentActiveSectionLink;
    if (target) movePillTo(target);
  }, { passive: true });

  // Dynamic theme switching based on position on the page & Active section scroll spy
  const headerEl = document.getElementById('main-header');
  const heroEl = document.getElementById('home');
  const navSectionIds = ['home', 'about', 'offerings', 'compliance', 'regulatory'];

  let cachedHeroBottom = 600;
  let cachedNavSections: Array<{ id: string; top: number; bottom: number; link: HTMLAnchorElement }> = [];
  let isCurrentlyOnHero = true;
  let scrollTicking = false;

  function measureLayout() {
    if (heroEl) {
      const heroRect = heroEl.getBoundingClientRect();
      cachedHeroBottom = heroRect.top + window.scrollY + heroEl.offsetHeight - 80;
    }

    cachedNavSections = [];
    navSectionIds.forEach(id => {
      const el = document.getElementById(id);
      const link = document.querySelector<HTMLAnchorElement>(`.desktop-nav .nav-link[href="#${id}"]`);
      if (el && link) {
        const rect = el.getBoundingClientRect();
        const top = rect.top + window.scrollY;
        cachedNavSections.push({
          id,
          top,
          bottom: top + el.offsetHeight,
          link
        });
      }
    });

    cachedNavSections.sort((a, b) => a.top - b.top);
  }

  // Initial measurement & resize handler
  measureLayout();
  window.addEventListener('resize', measureLayout, { passive: true });

  function onScrollFrame() {
    const scrollY = window.scrollY;

    // Theme check with minimal DOM mutation
    const shouldBeOnHero = scrollY < cachedHeroBottom;
    if (shouldBeOnHero !== isCurrentlyOnHero) {
      isCurrentlyOnHero = shouldBeOnHero;
      if (headerEl) {
        if (isCurrentlyOnHero) {
          headerEl.classList.add('is-on-hero');
        } else {
          headerEl.classList.remove('is-on-hero');
        }
      }
    }

    // Active section scroll spy: high precision, backwards traversal
    let matchedLink: HTMLAnchorElement | null = null;

    if (scrollY < 220) {
      matchedLink = document.querySelector<HTMLAnchorElement>('.desktop-nav .nav-link[href="#home"]');
    } else {
      const scrollPos = scrollY + 160;
      for (let i = cachedNavSections.length - 1; i >= 0; i--) {
        const sec = cachedNavSections[i];
        if (scrollPos >= sec.top) {
          matchedLink = sec.link;
          break;
        }
      }
      if (!matchedLink && cachedNavSections.length > 0) {
        matchedLink = cachedNavSections[0].link;
      }
    }

    if (matchedLink && matchedLink !== currentActiveSectionLink) {
      setActiveSection(matchedLink);
    }

    scrollTicking = false;
  }

  // High-performance scroll listener: 0 layout thrashing, 60/120fps sync
  window.addEventListener('scroll', () => {
    if (!scrollTicking) {
      scrollTicking = true;
      requestAnimationFrame(onScrollFrame);
    }
  }, { passive: true });

  // Accessible Mobile Drawer Logic
  const toggleBtn = document.getElementById('nav-toggle');
  const drawer = document.getElementById('mobile-nav-drawer');
  const backdrop = document.getElementById('drawer-backdrop');
  const closeBtn = document.getElementById('drawer-close');
  const drawerLinks = document.querySelectorAll('.drawer-link');

  function openDrawer() {
    if (!drawer || !backdrop || !toggleBtn) return;
    drawer.classList.add('active');
    backdrop.classList.add('active');
    drawer.removeAttribute('inert');
    drawer.setAttribute('aria-hidden', 'false');
    toggleBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    closeBtn?.focus();
  }

  function closeDrawer() {
    if (!drawer || !backdrop || !toggleBtn) return;
    drawer.classList.remove('active');
    backdrop.classList.remove('active');
    drawer.setAttribute('inert', '');
    drawer.setAttribute('aria-hidden', 'true');
    toggleBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    toggleBtn.focus();
  }

  toggleBtn?.addEventListener('click', openDrawer);
  closeBtn?.addEventListener('click', closeDrawer);
  backdrop?.addEventListener('click', closeDrawer);

  drawerLinks.forEach(l => {
    l.addEventListener('click', closeDrawer);
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer?.classList.contains('active')) {
      closeDrawer();
    }
  });
