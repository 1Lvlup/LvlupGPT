document.addEventListener('DOMContentLoaded', () => {
  window.MathJax = {
    tex: {
      inlineMath: [['\\(', '\\)']],
      displayMath: [['\\[', '\\]']],
      processEscapes: true,
      processEnvironments: true
    },
    options: {
      ignoreHtmlClass: '.*|',
      processHtmlClass: 'arithmatex'
    }
  };

  MathJax.typesetPromise().catch(error => {
    console.error('MathJax failed to typeset: ', error);
  });
});
