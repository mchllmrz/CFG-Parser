const viz = new Viz(); // Create a new instance of Viz.js to render graphs

//* Renders the parse tree using a DOT language string
function renderTree(dot) {
  viz.renderSVGElement(dot)
    .then(svg => {
      const container = document.getElementById('graph');
      container.innerHTML = '';
      svg.style.maxWidth = '100%';
      container.appendChild(svg);
    })
    .catch(err => {
      console.error(err);
      document.getElementById('graph').innerHTML =
        `<p style="color:red">Error rendering tree:</p><pre>${err.message}</pre><pre>${dot}</pre>`;
    });
}

// Function to handle the parsing of the input string
// This function is called when the user clicks the "Parse" button
function runParse() {
  //get the input string from the text area
  const input = document.getElementById('inputStr').value.trim();

  //clear previous results
  document.getElementById('output').textContent = '';
  document.getElementById('graph').innerHTML = '';
  document.getElementById('derivations').innerHTML = 'Parsing...';
  //send post request to the server with the input string
  fetch('/parse', { 
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input }) //send the input string as json
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      document.getElementById('output').textContent = '✅ Valid string!';
      renderTree(data.dot);

      const derivHTML = "<h3>Derivation Steps:</h3><pre>" +
        data.derivations.map((step, i) => (i === 0 ? step : "→ " + step)).join("\n") +
        "</pre>";
      document.getElementById('derivations').innerHTML = derivHTML;
    } else { // Handle parsing errors
      document.getElementById('output').textContent = `❌ ${data.error}`;
      document.getElementById('derivations').innerHTML = '';
      document.getElementById('graph').innerHTML = '';
    }
  })
  .catch(err => { // Handle network errors
    document.getElementById('output').textContent = `⚠️ Network error: ${err.message}`;
    document.getElementById('derivations').innerHTML = '';
    document.getElementById('graph').innerHTML = '';
  });
}