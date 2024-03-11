// Wait for the DOM to be fully loaded before executing the code
document.addEventListener('DOMContentLoaded', () => {

  // Define the configuration for MathJax
  window.MathJax = {
    tex: {
      // Configuration for inline and display math equations
      inlineMath: [['\\(', '\\)']],
      displayMath: [['\\[', '\\]']],
      processEscapes: true, // Enable processing of escaped characters
      processEnvironments: true // Enable processing of LaTeX environments
    },
    options: {
      // Configuration for ignoring and processing HTML classes
      ignoreHtmlClass: '.*|',
      processHtmlClass: 'arithmatex'
    }
  };

  // Call the MathJax typesetPromise method to render the math equations
  MathJax.typesetPromise()
    .catch(error => {
      // If there's an error during typesetting, log the error to the console
      console.error('MathJax failed to typeset: ', error);
    });
});
