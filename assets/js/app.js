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
    <div class="hero-label">${heroPrice.label}${heroPrice.note ? `<span style="font-size:0.6rem;color:var(--fg-subtle);font-weight:400;margin-left:4px">(${heroPrice.note})</span>` : ''}</div>
    <div class="hero-value">${heroPrice.value}<span class="hero-unit">${heroPrice.unit || ''}</span></div>
    <div class="hero-change ${heroCls}">${chgArrow(heroPrice.change)} ${fmtPct(heroPrice.change)}</div>
    ${heroPrice.source ? `<div class="source-tag">${heroPrice.source}</div>` : ''}
    <div class="price-mini-grid">
      ${b.prices.filter(p => p !== heroPrice).map(p => `
        <div class="price-mini">
          <div class="pm-label">${p.label}</div>
          <div class="pm-value">${p.value}${p.unit ? `<span style="font-size:0.6rem;color:var(--fg-subtle)">${p.unit}</span>` : ''}</div>
          <div class="pm-change text-${chgClass(p.change)}">${chgArrow(p.change)} ${fmtPct(p.change)}</div>
          ${p.source ? `<div class="source-tag">${p.source}</div>` : ''}
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
      ${n.source ? `
        <div class="news-source">
          <span class="news-source-name">📰 ${n.source}</span>
          ${n.url ? `<a class="source-link" href="${n.url}" target="_blank" rel="noopener">查看原文 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></a>` : ''}
        </div>
      ` : ''}
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
      ${teach.source ? `<div class="teach-source">📚 参考：${teach.source}</div>` : ''}
    </div>
  `;

  // Data Sources Footer
  const meta = b._meta;
  if (meta && meta.dataSources) {
    const srcFooter = document.createElement('div');
    srcFooter.className = 'source-footer';
    srcFooter.innerHTML = `
      <div class="source-footer-title">📡 数据来源</div>
      <div class="source-footer-list">
        ${meta.dataSources.map(s => `
          ${s.url ? `<a class="source-footer-item" href="${s.url}" target="_blank" rel="noopener">${s.name}</a>` : `<span class="source-footer-item">${s.name}</span>`}
        `).join('')}
      </div>
    `;
    document.getElementById('page-home').appendChild(srcFooter);
  }
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
// Cache aggregated knowledge across all briefings
let allKnowledgeCache = null;

async function renderKnowledge() {
  // Aggregate knowledge from all briefings (cached after first load)
  if (!allKnowledgeCache) {
    const briefings = (state.manifest && state.manifest.briefings) || [];
    const kbMap = new Map();
    
    // Collect from all briefings (reverse chronological)
    for (const entry of briefings) {
      let briefing;
      if (entry.date === state.currentBriefing?.date && state.currentBriefing?.knowledge) {
        briefing = state.currentBriefing;
      } else {
        try {
          briefing = await fetchJSON(`daily/${entry.date}.json`);
        } catch (e) { continue; }
      }
      const items = briefing?.knowledge || [];
      for (const item of items) {
        // Deduplicate by title
        if (!kbMap.has(item.title)) {
          kbMap.set(item.title, item);
        }
      }
      // Also include today's teach card (every day's 今日学一招) as a knowledge entry
      const teach = briefing?.teach;
      if (teach && teach.title) {
        const teachKey = `[今日学一招] ${teach.title}`;
        if (!kbMap.has(teachKey)) {
          // Strip HTML tags from body for summary
          const plainBody = String(teach.body || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
          kbMap.set(teachKey, {
            cat: '今日学一招',
            title: teach.title,
            summary: plainBody.length > 50 ? plainBody.slice(0, 50) + '…' : plainBody,
            detail: teach.body,
            source: teach.source || '每日金价早报',
            _date: entry.date
          });
        }
      }
    }
    allKnowledgeCache = Array.from(kbMap.values());
    // Sort: items with date first (newest first), then undated
    allKnowledgeCache.sort((a, b) => {
      const da = a._date || '';
      const db = b._date || '';
      if (da && !db) return -1;
      if (!da && db) return 1;
      return db.localeCompare(da);
    });
  }

  const kbItems = allKnowledgeCache;

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
      ${k.source ? `<div class="kb-source">📚 ${k.source}</div>` : ''}
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

  // Chart source
  const chartSrc = chart.source;
  if (chartSrc) {
    const chartCard = document.getElementById('chart-wrap');
    let srcEl = chartCard.querySelector('.chart-source');
    if (!srcEl) {
      srcEl = document.createElement('div');
      srcEl.className = 'chart-source';
      chartCard.appendChild(srcEl);
    }
    srcEl.textContent = '📡 ' + chartSrc;
  }

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

// ===== Render: Logs =====
let logData = [];
let activeLogIdx = -1;

const TYPE_LABELS = {
  'morning_briefing': '早报',
  'inspection_am': '巡检·上午',
  'inspection_pm': '巡检·下午',
  'inspection_night': '巡检·晚间',
  'inspection': '巡检'
};

const STATUS_LABELS = {
  'success': '✓ 成功',
  'partial': '⚠ 部分',
  'failed': '✗ 失败',
  'no_action': '○ 无动作'
};

async function fetchLogs() {
  logData = [];

  // Load from logs/manifest.json
  try {
    const resp = await fetch('logs/manifest.json');
    if (resp.ok) {
      const m = await resp.json();
      for (const entry of (m.logs || [])) {
        try {
          const r = await fetch(`logs/${entry.date}-${entry.type}.json`);
          if (r.ok) {
            const l = await r.json();
            l._filename = `logs/${entry.date}-${entry.type}.json`;
            if (!logData.find(ex => ex.date === l.date && ex.type === l.type)) {
              logData.push(l);
            }
          }
        } catch (e) {}
      }
    }
  } catch (e) {}

  // Sort by date desc, then by type
  logData.sort((a, b) => {
    if (a.date !== b.date) return b.date.localeCompare(a.date);
    return (a.timestamp || '').localeCompare(b.timestamp || '');
  });
}

let logTypeFilter = 'all';

function renderLogs() {
  fetchLogs().then(() => {
    if (logData.length === 0) {
      document.getElementById('log-filters').innerHTML = '';
      document.getElementById('log-sidebar').innerHTML = `
        <div class="empty-state" style="padding:30px">
          <div class="empty-icon">📋</div>
          <p>暂无运行日志</p>
          <p style="font-size:0.75rem;margin-top:4px">自动化运行后日志会自动生成</p>
        </div>`;
      document.getElementById('log-content').innerHTML = '<div class="log-empty-hint">← 点击左侧日志条目查看详细执行过程</div>';
      return;
    }

    // Filters
    const types = ['all', ...new Set(logData.map(l => l.type))];
    document.getElementById('log-filters').innerHTML = types.map(t => {
      const label = t === 'all' ? '全部' : (TYPE_LABELS[t] || t);
      const active = t === logTypeFilter;
      return `<button class="kb-chip ${active ? 'active' : ''}" data-type="${t}">${label}</button>`;
    }).join('');

    document.querySelectorAll('#log-filters .kb-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        logTypeFilter = chip.dataset.type;
        activeLogIdx = -1;
        document.getElementById('log-content').innerHTML = '<div class="log-empty-hint">← 点击左侧日志条目查看详细执行过程</div>';
        renderLogs();
      });
    });

    // Filter
    const filtered = logTypeFilter === 'all' ? logData : logData.filter(l => l.type === logTypeFilter);

    // List
    document.getElementById('log-sidebar').innerHTML = filtered.map((l, i) => {
      const stCls = l.status || 'success';
      const typeLabel = TYPE_LABELS[l.type] || l.type;
      const s = l.summary_stats || l.summary || {};
      const stLabel = STATUS_LABELS[stCls] || stCls;
      return `
        <div class="log-entry ${i === activeLogIdx ? 'active' : ''}" data-idx="${i}">
          <div class="log-left">
            <span class="log-status ${stCls}"></span>
            <div>
              <div style="display:flex;align-items:center;gap:6px">
                <span class="log-date">${l.date}</span>
                <span class="log-type">${typeLabel}</span>
                <span style="font-size:0.65rem;color:var(--fg-subtle)">${stLabel}</span>
              </div>
              <div class="log-summary">${l.summary || ''}</div>
            </div>
          </div>
          <span class="log-arrow">›</span>
        </div>`;
    }).join('');

    // Click handler
    document.querySelectorAll('.log-entry').forEach(entry => {
      entry.addEventListener('click', () => {
        const idx = parseInt(entry.dataset.idx);
        // Toggle: click same to close
        if (activeLogIdx === idx) {
          activeLogIdx = -1;
          entry.classList.remove('active');
          document.getElementById('log-content').innerHTML = '<div class="log-empty-hint">← 点击左侧日志条目查看详细执行过程</div>';
          document.getElementById('log-content').classList.remove('show');
          return;
        }
        activeLogIdx = idx;
        document.getElementById('log-content').classList.add('show');
        document.querySelectorAll('.log-entry').forEach(e => e.classList.remove('active'));
        entry.classList.add('active');
        renderLogDetail(filtered[idx]);
      });
    });
  });
}

function renderLogDetail(l) {
  if (!l) return;
  const stCls = l.status || 'success';
  const stLabel = STATUS_LABELS[stCls] || l.status;
  const s = l.summary_stats || l.summary || {};
  const typeLabel = TYPE_LABELS[l.type] || l.type;

  document.getElementById('log-content').innerHTML = `
    <div class="log-run-header">
      <div>
        <span class="log-run-title">${l.date} · ${typeLabel}</span>
        <span style="margin-left:8px;font-size:0.68rem;color:var(--fg-subtle)">${stLabel}</span>
      </div>
      <div style="display:flex;align-items:center;gap:8px">
        <div class="log-run-time">${l.timestamp || ''}</div>
        <button class="log-close-btn" onclick="closeLogDetail()">收起 ✕</button>
      </div>
    </div>
    <div class="step-list">
      ${(l.steps || []).map((step) => {
        const outputs = step.outputs || [];
        return `
        <div class="step-item ${step.status}">
          <div class="step-num">${step.step}</div>
          <div class="step-info">
            <div class="step-header">
              <span class="step-name">${step.name}</span>
              <span class="step-duration">${(step.duration_ms / 1000).toFixed(1)}s</span>
            </div>
            <div class="step-meta">
              <span>🔧 ${step.tool || '—'}</span>
              ${step.source ? `<span>📡 ${step.source}</span>` : ''}
            </div>
            <div class="step-result">${step.result_summary || ''}</div>
            ${step.query ? `<div class="step-query">查询: ${step.query}</div>` : ''}
            ${outputs.length > 0 ? `
              <div class="step-outputs">
                ${outputs.map((o, oi) => `
                  <div class="step-output-block">
                    <div class="step-output-label">${o.label || '产物'}</div>
                    <div class="step-output-body">${o.type === 'json' || o.label.includes('JSON') ? '<pre style="white-space:pre;line-height:1.5;margin:0;font-size:0.63rem">' + o.content + '</pre>' : o.content}</div>
                  </div>
                `).join('')}
              </div>
            ` : ''}
          </div>
        </div>`;
      }).join('')}
    </div>
    <div class="log-summary-box">
      <div class="log-summary-item">总计 <strong>${s.total_steps || 0}</strong> 步</div>
      <div class="log-summary-item" style="color:var(--down)">成功 <strong>${s.success_steps || 0}</strong></div>
      ${s.failed_steps > 0 ? `<div class="log-summary-item" style="color:var(--up)">失败 <strong>${s.failed_steps}</strong></div>` : ''}
      <div class="log-summary-item">耗时 <strong>${((s.total_duration_ms || 0) / 1000).toFixed(1)}s</strong></div>
      ${s.email_sent ? '<div class="log-summary-item">📧 邮件已发</div>' : ''}
      ${s.git_pushed ? '<div class="log-summary-item">🚀 已推送</div>' : ''}
    </div>
  `;
}

function closeLogDetail() {
  activeLogIdx = -1;
  document.querySelectorAll('.log-entry').forEach(e => e.classList.remove('active'));
  document.getElementById('log-content').innerHTML = '<div class="log-empty-hint">← 点击左侧日志条目查看详细执行过程</div>';
  // Hide on mobile
  document.getElementById('log-content').classList.remove('show');
}
window.closeLogDetail = closeLogDetail;

// ===== Navigation =====
const pages = ['home', 'knowledge', 'chart', 'about', 'archive', 'logs'];
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
  if (name === 'logs') renderLogs();

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
