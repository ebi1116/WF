(() => {
  const nav = document.querySelector('#primaryNav');
  document.querySelectorAll('#primaryNav a').forEach((link) => {
    link.addEventListener('click', () => {
      if (nav?.classList.contains('show')) {
        bootstrap.Collapse.getOrCreateInstance(nav).hide();
      }
    });
  });

})();
