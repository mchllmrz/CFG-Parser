const viz = new Viz();

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

function runParse() {
  const input = document.getElementById('inputStr').value.trim();
  document.getElementById('output').textContent = '';
  document.getElementById('graph').innerHTML = '';
  document.getElementById('derivations').innerHTML = 'Parsing...';

  fetch('/parse', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input })
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
    } else {
      document.getElementById('output').textContent = `❌ ${data.error}`;
      document.getElementById('derivations').innerHTML = '';
      document.getElementById('graph').innerHTML = '';
    }
  })
  .catch(err => {
    document.getElementById('output').textContent = `⚠️ Network error: ${err.message}`;
    document.getElementById('derivations').innerHTML = '';
    document.getElementById('graph').innerHTML = '';
  });
}