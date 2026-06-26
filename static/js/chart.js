// FORECAST_LABELS and FORECAST_PRICES are injected by Jinja2 in result.html

// ── Set today's date ──
const dateEl = document.getElementById('todayDate');
if (dateEl) {
  dateEl.textContent = new Date().toLocaleDateString('en', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });
}

// ── Compute daily % changes ──
const changes = FORECAST_PRICES.map((price, i) => {
  if (i === 0) return 0;
  return parseFloat(((price - FORECAST_PRICES[i - 1]) / FORECAST_PRICES[i - 1] * 100).toFixed(2));
});

// ── Common chart defaults ──
const gridColor  = 'rgba(0,0,0,0.05)';
const tickColor  = '#64748B';
const tickFont   = { size: 11, family: 'Inter, system-ui, sans-serif' };

// ── Line chart: 7-day price forecast ──
const fCtx = document.getElementById('forecastChart').getContext('2d');

// gradient fill under the line
const gradient = fCtx.createLinearGradient(0, 0, 0, 260);
gradient.addColorStop(0, 'rgba(37,99,235,0.18)');
gradient.addColorStop(1, 'rgba(37,99,235,0.01)');

new Chart(fCtx, {
  type: 'line',
  data: {
    labels: FORECAST_LABELS,
    datasets: [{
      label: 'Predicted Price (NPR)',
      data: FORECAST_PRICES,
      borderColor: '#2563EB',
      backgroundColor: gradient,
      borderWidth: 2.5,
      pointRadius: 5,
      pointHoverRadius: 7,
      pointBackgroundColor: '#fff',
      pointBorderColor: '#2563EB',
      pointBorderWidth: 2.5,
      tension: 0.38,
      fill: true
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#1E293B',
        titleFont: { size: 12, weight: '600', family: 'Inter, system-ui, sans-serif' },
        bodyFont:  { size: 13, family: 'Inter, system-ui, sans-serif' },
        padding: 10,
        cornerRadius: 8,
        callbacks: {
          label: ctx => ` NPR ${ctx.parsed.y.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
        }
      }
    },
    scales: {
      x: {
        grid: { color: gridColor },
        ticks: { font: tickFont, color: tickColor }
      },
      y: {
        grid: { color: gridColor },
        ticks: {
          font: tickFont,
          color: tickColor,
          callback: v => 'NPR ' + v.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })
        }
      }
    }
  }
});

// ── Bar chart: daily % change ──
const cCtx = document.getElementById('changeChart').getContext('2d');

new Chart(cCtx, {
  type: 'bar',
  data: {
    labels: FORECAST_LABELS,
    datasets: [{
      label: 'Change %',
      data: changes,
      backgroundColor: changes.map(c => c >= 0 ? 'rgba(5,150,105,0.75)' : 'rgba(220,38,38,0.75)'),
      borderColor:     changes.map(c => c >= 0 ? '#059669'              : '#DC2626'),
      borderWidth: 1,
      borderRadius: 5
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#1E293B',
        callbacks: {
          label: ctx => {
            if (ctx.dataIndex === 0) return ' Baseline day';
            return ` ${ctx.parsed.y >= 0 ? '+' : ''}${ctx.parsed.y.toFixed(2)}%`;
          }
        }
      }
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { font: tickFont, color: tickColor }
      },
      y: {
        grid: { color: gridColor },
        ticks: {
          font: tickFont,
          color: tickColor,
          callback: v => v.toFixed(1) + '%'
        },
        afterDataLimits: scale => {
          const ext = Math.max(Math.abs(scale.min), Math.abs(scale.max)) * 1.4 || 2;
          scale.min = -ext;
          scale.max =  ext;
        }
      }
    }
  }
});