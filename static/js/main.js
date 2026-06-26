// Set today's date pill
const el = document.getElementById('todayDate');
if (el) {
  el.textContent = new Date().toLocaleDateString('en', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });
}

// Quick-pick chip handler
function pickSymbol(sym) {
  const input = document.getElementById('symbolInput');
  if (input) {
    input.value = sym;
    input.focus();
  }
}