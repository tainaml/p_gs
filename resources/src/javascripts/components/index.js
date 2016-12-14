const moduleElements = document.querySelectorAll('[data-page]');

for (var i = 0; i < moduleElements.length; i++) {
  const el = moduleElements[i];
  const name = el.getAttribute('data-page');
  require.ensure([], function() {
    const module = require(`./${name}`)
    new module(el)
  })
}
