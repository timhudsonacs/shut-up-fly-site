const finder = document.querySelector('#game-finder');
if (finder) {
  const mood = finder.querySelector('#game-mood');
  const software = finder.querySelector('#game-os');
  const cards = [...document.querySelectorAll('.guide-card')];
  const status = document.querySelector('#finder-status');
  const empty = document.querySelector('#finder-empty');
  const update = () => {
    let count = 0;
    for (const card of cards) {
      const moodFits = mood.value === 'all' || card.dataset.moods.split(' ').includes(mood.value);
      const softwareFits = software.value === 'unknown' || Number(card.dataset.minOs) <= Number(software.value);
      card.hidden = !(moodFits && softwareFits);
      if (!card.hidden) count++;
    }
    status.textContent = `${count} ${count === 1 ? 'game matches' : 'games match'} your choices. Check each App Store listing for your device.`;
    empty.hidden = count !== 0;
  };
  document.querySelectorAll('a[href^="#guide-"]').forEach(link => {
    link.addEventListener('click', () => {
      const target = document.querySelector(link.getAttribute('href'));
      if (target?.hidden) {
        finder.reset();
        update();
      }
    });
  });
  finder.hidden = false;
  finder.addEventListener('change', update);
  finder.addEventListener('reset', () => setTimeout(update, 0));
}
