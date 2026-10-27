const video = document.querySelector('.splash-video');
const replay = document.querySelector('.splash-replay');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

if (video && replay) {
  const showStill = () => {
    video.pause();
    video.hidden = true;
  };
  const play = async () => {
    video.currentTime = 0;
    video.hidden = false;
    try {
      await video.play();
    } catch {
      showStill();
    }
  };
  video.addEventListener('playing', () => { video.hidden = false; });
  video.addEventListener('ended', showStill);
  video.addEventListener('error', showStill);
  video.querySelector('source')?.addEventListener('error', showStill);
  replay.hidden = false;
  replay.addEventListener('click', play);
  reducedMotion.addEventListener('change', () => {
    if (reducedMotion.matches) showStill();
  });
  if (!reducedMotion.matches) void play();
}
