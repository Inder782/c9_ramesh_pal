// Mentorship Gallery Pause/Play Toggle Controller
const toggleBtn = document.getElementById('mentorship-toggle-btn');
const toggleText = document.getElementById('mentorship-toggle-text');
const reelTrack = document.getElementById('mentorship-reel-track');

let isPaused = false;

function setPausedState(paused: boolean) {
  isPaused = paused;
  if (reelTrack) {
    if (isPaused) {
      reelTrack.classList.add('is-paused');
    } else {
      reelTrack.classList.remove('is-paused');
    }
  }
  if (toggleBtn) {
    toggleBtn.setAttribute('aria-pressed', String(isPaused));
    toggleBtn.setAttribute('aria-label', isPaused ? 'Resume Gallery' : 'Pause Gallery');
    toggleBtn.setAttribute('title', isPaused ? 'Resume Gallery' : 'Pause Gallery');
    if (isPaused) {
      toggleBtn.classList.add('is-paused');
    } else {
      toggleBtn.classList.remove('is-paused');
    }
  }
  if (toggleText) {
    toggleText.textContent = isPaused ? 'Resume Gallery' : 'Pause Gallery';
  }
}

toggleBtn?.addEventListener('click', () => {
  setPausedState(!isPaused);
});

toggleBtn?.addEventListener('keydown', (e: KeyboardEvent) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    setPausedState(!isPaused);
  }
});
