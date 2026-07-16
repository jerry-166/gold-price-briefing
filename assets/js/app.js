/* ===== 每日金价资讯 · 应用逻辑 ===== */

// ===== State =====
let state = {
  manifest: null,
  currentBriefing: null,
  chartInstance: null,
  kbFilter: '全部',
};

// ===== Helpers =====
function chgClass(n) {
  if (n > 0) return 'up';
  if (n < 0) return 'down';
  return 'flat';
}
function chgArrow(n) {
  if (n > 0) return '↑';
  if (n < 0) return '↓';
  return '→';
}
function fmtPct(n) {
  return (n >= 0 ? '+' : '') + n.toFixed(2) + '%';
}
async function fetchJSON(url) {
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${url}`);
  return resp.json();
}

// ===== Data Loading =====
async function loadManifest() {
  try {
    state.manifest = await fetchJSON('manifest.json');
  } catch (e) {
    console.info('fetch manifest failed, using embedded fallback:', e.message);
    state.manifest = window.__SAMPLE_MANIFEST__ || { briefings: [] };
  }
  return state.manifest;
}

async function loadBriefing(date) {
  try {
    state.currentBriefing = await fetchJSON(`daily/${date}.json`);
  } catch (e) {
    console.info('fetch briefing failed, using embedded fallback:', e.message);
    state.currentBriefing = window.__SAMPLE_BRIEFING__ || null;
  }
  return state.currentBriefing;
}

async function loadLatestBriefing() {
  await loadManifest();
  const briefings = state.manifest.briefings || [];
  if (briefings.length === 0) {
    renderEmptyHome();
    return;
  }
  const latest = briefings[briefings.length - 1];
  await loadBriefing(latest.date);
  renderHome();
}

// ===== Render: Home =====
function renderHome() {
  const b = state.currentBriefing;
  if (!b) { renderEmptyHome(); return; }

  // Header
  document.getElementById('header-date').textContent = `${b.date} ${b.weekday || ''}`;

  // Price Hero
  const heroPrice = b.prices.find(p => p.hero) || b.prices[0];
  const heroEl = document.getElementById('price-hero');
  const heroCls = chgClass(heroPrice.change);
  heroEl.innerHTML = `
    <div class="hero-label">${heroPrice.label}</div>
    <div class="hero-value">${heroPrice.value}<span class="hero-unit">${heroPrice.unit || ''}</span></div>
    <div class="hero-change ${heroCls}">${chgArrow(heroPrice.change)} ${fmtPct(heroPrice.change)}</div>
    <div class="price-mini-grid">
      ${b.prices.filter(p => p !== heroPrice).map(p => `
        <div class="price-mini">
          <div class="pm-label">${p.label}</div>
          <div class="pm-value">${p.value}</div>
          <div class="pm-change text-${chgClass(p.change)}">${chgArrow(p.change)} ${fmtPct(p.change)}</div>
        </div>
      `).join('')}
    </div>
  `;

  // News
  document.getElementById('news-list').innerHTML = (b.news || []).map(n => `
    <div class="news-item">
      <span class="news-tag ${n.tagType || 'fed'}">${n.tag}</span>
      <div class="news-title">${n.title}</div>
      <div class="news-explain">${n.explain}</div>
    </div>
  `).join('') || '<div class="empty-state"><div class="empty-icon">📰</div>今日暂无重大新闻</div>';

  // Trend
  const t = b.trend || {};
  document.getElementById('trend-grid').innerHTML = `
    <div class="trend-box">
      <div class="tb-period">本周</div>
      <div class="tb-icon text-${chgClass(t.shortVal || 0)}">${chgArrow(t.shortVal || 0)}</div>
      <div class="tb-text text-${chgClass(t.shortVal || 0)}">${t.short || '—'}</div>
    </div>
    <div class="trend-box">
      <div class="tb-period">本月</div>
      <div class="tb-icon text-${chgClass(t.midVal || 0)}">${chgArrow(t.midVal || 0)}</div>
      <div class="tb-text text-${chgClass(t.midVal || 0)}">${t.mid || '—'}</div>
    </div>
    <div class="trend-box">
      <div class="tb-period">本季</div>
      <div class="tb-icon text-${chgClass(t.longVal || 0)}">${chgArrow(t.longVal || 0)}</div>
      <div class="tb-text text-${chgClass(t.longVal || 0)}">${t.long || '—'}</div>
    </div>
  `;

  // Advice
  const actionMap = { hold: 'hold', buy: 'buy', watch: 'watch' };
  const actionLabels = { hold: '建议：持有', buy: '建议：可加仓', watch: '建议：观望' };
  const aCls = actionMap[t.action] || 'hold';
  document.getElementById('advice-box').innerHTML = `
    <div class="advice-card ${aCls}">
      <svg class="advice-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <div class="advice-text">
        <strong>${actionLabels[t.action] || '建议：持有'}</strong>
        ${t.advice || ''}
      </div>
    </div>
  `;

  // Teaching
  const teach = b.teach || {};
  document.getElementById('teach-box').innerHTML = `
    <div class="teach-card">
      <span class="teach-badge">知识</span>
      <div class="teach-title">${teach.title || '今日学一招'}</div>
      <div class="teach-body">${teach.body || ''}</div>
    </div>
  `;
}

function renderEmptyHome() {
  document.getElementById('price-hero').innerHTML = `
    <div class="empty-state" style="padding:20px">
      <div class="empty-icon">📊</div>
      <p>暂无早报数据</p>
      <p style="font-size:0.75rem;margin-top:4px">系统每天早上9点自动更新</p>
    </div>
  `;
  document.getElementById('news-list').innerHTML = '';
  document.getElementById('trend-grid').innerHTML = '';
  document.getElementById('advice-box').innerHTML = '';
  document.getElementById('teach-box').innerHTML = '';
}

// ===== Render: Knowledge =====
function renderKnowledge() {
  const b = state.currentBriefing;
  const kbItems = (b && b.knowledge) || [];

  if (kbItems.length === 0) {
    document.getElementById('kb-filters').innerHTML = '';
    document.getElementById('kb-list').innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">📚</div>
        <p>知识库正在建设中</p>
        <p style="font-size:0.75rem;margin-top:4px">每天学一招，慢慢积累</p>
      </div>
    `;
    return;
  }

  // Categories
  const cats = ['全部', ...new Set(kbItems.map(k => k.cat))];
  document.getElementById('kb-filters').innerHTML = cats.map(c => `
    <button class="kb-chip ${c === state.kbFilter ? 'active' : ''}" data-cat="${c}">${c}</button>
  `).join('');

  document.querySelectorAll('.kb-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      state.kbFilter = chip.dataset.cat;
      renderKnowledge();
    });
  });

  // Items
  const filtered = state.kbFilter === '全部' ? kbItems : kbItems.filter(k => k.cat === state.kbFilter);
  document.getElementById('kb-list').innerHTML = filtered.map((k, i) => `
    <button class="kb-card" data-idx="${i}">
      <div class="kb-cat">${k.cat}</div>
      <h3>${k.title}</h3>
      <p class="kb-summary">${k.summary}</p>
      <div class="kb-detail">${k.detail}</div>
      <span class="kb-toggle">点击展开 ▾</span>
    </button>
  `).join('');

  document.querySelectorAll('.kb-card').forEach(card => {
    card.addEventListener('click', () => {
      const open = card.classList.toggle('open');
      card.querySelector('.kb-toggle').textContent = open ? '点击收起 ▴' : '点击展开 ▾';
    });
  });
}

// ===== Render: Chart =====
function renderChart() {
  const b = state.currentBriefing;
  const chart = (b && b.chart) || null;

  if (!chart) {
    document.getElementById('chart-wrap').innerHTML = `
      <div class="empty-state" style="padding:30px">
        <div class="empty-icon">📈</div>
        <p>暂无走势数据</p>
      </div>
    `;
    document.getElementById('event-list').innerHTML = '';
    return;
  }

  // Stats
  const vals = chart.values;
  const first = vals[0], last = vals[vals.length - 1];
  const pct = ((last - first) / first) * 100;
  const rangeEl = document.getElementById('chart-range-chg');
  rangeEl.textContent = fmtPct(pct);
  rangeEl.className = 'cm-val text-' + chgClass(pct);
  document.getElementById('chart-latest').textContent = last.toFixed(1) + ' ¥/克';

  // Events
  document.getElementById('event-list').innerHTML = (chart.events || []).map(e => `
    <div class="event-item">
      <span class="event-dot"></span>
      <div>
        <div class="event-date">${e.date}</div>
        <div class="event-text">${e.text}</div>
      </div>
    </div>
  `).join('') || '';

  // Chart
  if (state.chartInstance) { state.chartInstance.destroy(); state.chartInstance = null; }

  const ctx = document.getElementById('gold-chart').getContext('2d');
  const eventIdxs = (chart.events || []).map(e => e.index);
  const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const gridColor = isDark ? 'oklch(0.28 0.006 250)' : 'oklch(0.92 0.003 250)';
  const tickColor = isDark ? 'oklch(0.65 0.008 250)' : 'oklch(0.50 0.01 250)';

  state.chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: chart.labels,
      datasets: [{
        label: '国内金价 ¥/克',
        data: vals,
        borderColor: 'oklch(0.75 0.15 75)',
        backgroundColor: 'oklch(0.75 0.15 75 / 0.08)',
        borderWidth: 2,
        fill: true,
        tension: 0.3,
        pointRadius: vals.map((_, i) => eventIdxs.includes(i) ? 5 : 0),
        pointHoverRadius: 6,
        pointBackgroundColor: vals.map((_, i) => eventIdxs.includes(i) ? 'oklch(0.75 0.15 75)' : 'transparent'),
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: isDark ? 'oklch(0.20 0.006 250)' : 'oklch(0.18 0.01 250)',
          titleFont: { size: 11 },
          bodyFont: { size: 12, family: 'var(--font-mono)' },
          padding: 10,
          cornerRadius: 8,
          displayColors: false,
          callbacks: {
            label: (ctx) => {
              let txt = ctx.parsed.y.toFixed(1) + ' ¥/克';
              (chart.events || []).forEach(e => {
                if (e.index === ctx.dataIndex) txt += ' · ' + e.text;
              });
              return txt;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { maxRotation: 0, autoSkip: true, maxTicksLimit: 6, color: tickColor, font: { size: 10 } },
          border: { display: false }
        },
        y: {
          grid: { color: gridColor },
          ticks: { color: tickColor, font: { size: 10, family: 'var(--font-mono)' } },
          border: { display: false }
        }
      }
    }
  });
}

// ===== Render: Archive =====
function renderArchive() {
  const briefings = (state.manifest && state.manifest.briefings) || [];
  if (briefings.length === 0) {
    document.getElementById('archive-list').innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">📅</div>
        <p>暂无历史早报</p>
      </div>
    `;
    return;
  }
  const reversed = [...briefings].reverse();
  document.getElementById('archive-list').innerHTML = reversed.map(b => `
    <div class="archive-item" data-date="${b.date}">
      <div>
        <div class="archive-date">${b.date}</div>
        <div class="archive-title">${b.title || '今日金价早报'}</div>
      </div>
      <span class="archive-arrow">›</span>
    </div>
  `).join('');

  document.querySelectorAll('.archive-item').forEach(item => {
    item.addEventListener('click', async () => {
      await loadBriefing(item.dataset.date);
      showPage('home');
    });
  });
}

// ===== Navigation =====
const pages = ['home', 'knowledge', 'chart', 'about', 'archive'];
let chartRendered = false;

function showPage(name) {
  if (!pages.includes(name)) name = 'home';
  pages.forEach(p => {
    const el = document.getElementById('page-' + p);
    if (el) el.classList.toggle('active', p === name);
  });
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.page === name);
  });

  if (name === 'knowledge') renderKnowledge();
  if (name === 'chart') {
    requestAnimationFrame(() => { renderChart(); chartRendered = true; });
  }
  if (name === 'archive') renderArchive();

  window.scrollTo(0, 0);
}

// ===== Init =====
async function init() {
  // Nav events
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => showPage(btn.dataset.page));
  });

  // Load data
  await loadLatestBriefing();

  // Update header date if no briefing
  if (!state.currentBriefing) {
    const now = new Date();
    document.getElementById('header-date').textContent =
      `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
  }
}

// Start
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
