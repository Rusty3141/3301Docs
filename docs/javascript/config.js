window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

document$.subscribe(() => {
  MathJax.typesetPromise();
  const nodes = document.querySelectorAll('.timeago');
  const locale = nodes[0].getAttribute('locale');
  timeago.render(nodes, locale);

  var elements = document.getElementsByClassName("md-content");
  for (var i = 0; i < elements.length; i++) {
    lightGallery(elements[i], { selector: '.lightgallery-item', speed: 200, loop: false, hideBarsDelay: 2000 });
  }
});
