  function setupPricingInteractions() {
    // 1. Tab Switching (Advisory vs Courses)
    const btnAdvisory = document.getElementById('tab-btn-advisory');
    const btnCourses = document.getElementById('tab-btn-courses');
    const panelAdvisory = document.getElementById('panel-advisory');
    const panelCourses = document.getElementById('panel-courses');

    if (btnAdvisory && btnCourses && panelAdvisory && panelCourses) {
      function switchTab(target) {
        if (target === 'courses') {
          btnAdvisory.classList.remove('active');
          btnAdvisory.setAttribute('aria-selected', 'false');
          btnCourses.classList.add('active');
          btnCourses.setAttribute('aria-selected', 'true');
          panelAdvisory.classList.remove('active-panel');
          panelAdvisory.classList.add('hidden-panel');
          panelCourses.classList.remove('hidden-panel');
          panelCourses.classList.add('active-panel');
        } else {
          btnCourses.classList.remove('active');
          btnCourses.setAttribute('aria-selected', 'false');
          btnAdvisory.classList.add('active');
          btnAdvisory.setAttribute('aria-selected', 'true');
          panelCourses.classList.remove('active-panel');
          panelCourses.classList.add('hidden-panel');
          panelAdvisory.classList.remove('hidden-panel');
          panelAdvisory.classList.add('active-panel');
        }
      }

      btnAdvisory.addEventListener('click', () => switchTab('advisory'));
      btnCourses.addEventListener('click', () => switchTab('courses'));
    }

    // 2. Global Billing Duration Switcher (Weekly / Monthly / Quarterly)
    const billingPills = document.querySelectorAll('.billing-pill');
    const priceNumbers = document.querySelectorAll('.price-number');
    const pricePeriods = document.querySelectorAll('.price-period');
    const priceNotes = document.querySelectorAll('.price-note');

    billingPills.forEach((pill) => {
      pill.addEventListener('click', () => {
        const cycle = pill.getAttribute('data-cycle');
        if (!cycle) return;

        billingPills.forEach((p) => {
          p.classList.remove('active');
          p.setAttribute('aria-checked', 'false');
        });
        pill.classList.add('active');
        pill.setAttribute('aria-checked', 'true');

        priceNumbers.forEach((el) => {
          const val = el.getAttribute(`data-price-${cycle}`);
          if (val) {
            el.style.opacity = '0.3';
            setTimeout(() => {
              el.textContent = val;
              el.style.opacity = '1';
            }, 120);
          }
        });

        pricePeriods.forEach((el) => {
          const cycleVal = el.getAttribute(`data-period-${cycle}`);
          if (cycleVal) el.textContent = cycleVal;
        });

        priceNotes.forEach((el) => {
          const noteVal = el.getAttribute(`data-note-${cycle}`);
          if (noteVal) el.textContent = noteVal;
        });
      });
    });

    // 3. Track Station Subtle Hover Highlight
    const stations = document.querySelectorAll('.track-station');
    stations.forEach((st) => {
      st.addEventListener('mouseenter', () => {
        stations.forEach((s) => s.classList.remove('is-active'));
        st.classList.add('is-active');
      });
    });

    // 4. Mobile Advisory Ticker: Instant Tap/Touch to Pause & Release to Resume
    const advisoryStripEl = document.getElementById('advisory-strip');
    if (advisoryStripEl) {
      const pauseFlow = () => advisoryStripEl.classList.add('is-paused');
      const resumeFlow = () => advisoryStripEl.classList.remove('is-paused');

      advisoryStripEl.addEventListener('touchstart', pauseFlow, { passive: true });
      advisoryStripEl.addEventListener('touchend', resumeFlow, { passive: true });
      advisoryStripEl.addEventListener('touchcancel', resumeFlow, { passive: true });
      advisoryStripEl.addEventListener('mouseenter', pauseFlow);
      advisoryStripEl.addEventListener('mouseleave', resumeFlow);
    }
  }

  document.addEventListener('DOMContentLoaded', setupPricingInteractions);
  setupPricingInteractions();
