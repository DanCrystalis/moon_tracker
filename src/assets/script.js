// DOM Elements
const currentMoonSection = document.getElementById('current-moon');
const gatesContent = document.getElementById('gates-content');
const updateTimeElement = document.getElementById('update-time');
const refreshBtn = document.getElementById('refresh-btn');
const loadingSpinner = document.getElementById('loading-spinner');
const gateCountInput = document.getElementById('gate-count');

// Moon phase image mapping
const phaseImages = {
  "Dark Moon": "dark_moon.svg",
  "Waxing Crescent": "waxing_crescent.svg",
  "1st Quarter": "1st_quarter.svg",
  "Waxing Gibbous": "waxing_gibbous.svg",
  "Full Moon": "full_moon.svg",
  "Waning Gibbous": "waning_gibbous.svg",
  "3rd Quarter": "third_quarter.svg",
  "Waning Crescent": "waning_crescent.svg"
};

// Inline hint icon (SVG)
const HINT_ICON_SVG = `
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
    <path fill="#ffffffb3" d="M6.5 13.75h7v-1h-7zm0-3h11v-1h-11zm0-3h11v-1h-11zM12 21l-2.29-3.5H4.615q-.666 0-1.14-.475T3 15.886V4.615q0-.666.475-1.14T4.615 3h14.77q.666 0 1.14.475T21 4.615v11.27q0 .666-.475 1.14t-1.14.475H14.29zm0-1.811l1.754-2.689h5.63q.27 0 .443-.173t.173-.442V4.615q0-.269-.173-.442T19.385 4H4.615q-.269 0-.442.173T4 4.616v11.269q0 .269.173.442t.443.173h5.63zm0-8.939"/>
  </svg>
`;

// Utility functions
function formatDateTime(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZoneName: 'short'
  });
}

function updateLastUpdatedTime() {
  const now = new Date();
  updateTimeElement.textContent = now.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
}

function setFavicon(href, type = 'image/svg+xml') {
  let link = document.querySelector('link[rel="icon"]');
  if (!link) {
    link = document.createElement('link');
    link.rel = 'icon';
    document.head.appendChild(link);
  }
  link.type = type;
  const cacheBuster = (href.includes('?') ? '&' : '?') + 'v=' + Date.now();
  link.href = href + cacheBuster;
}

function showLoading() {
  loadingSpinner.style.display = 'block';
  currentMoonSection.innerHTML = `
    <h2>Current Moon</h2>
    <div class="loading-spinner" id="loading-spinner">
      <div class="spinner"></div>
      <p>Fetching moon data...</p>
    </div>
  `;
  
  gatesContent.innerHTML = `
    <div class="loading-spinner" id="loading-spinner">
      <div class="spinner"></div>
      <p>Updating gates...</p>
    </div>
  `;
}

function showError(message) {
  currentMoonSection.innerHTML = `
    <div class="error-message">
      <h3>⚠️ Error</h3>
      <p>${message}</p>
      <button onclick="fetchMoonData()" class="retry-btn">Retry</button>
    </div>
  `;
}

function createInfoCard(label, value) {
  return `
    <div class="info-card">
      <div class="info-label">${label}${label === 'Position' ? ` ${HINT_ICON_SVG}` : ''}</div>
      <div class="info-value">${value}</div>
    </div>
  `;
}

function createGateItem(gate, isNext = false) {
  const gateTime = formatDateTime(gate[0]);
  const gateName = gate[1];
  
  return `
    <div class="gate-item ${isNext ? 'next-gate' : ''}">
      <div class="gate-name">${gateName} ${HINT_ICON_SVG}</div>
      <div class="gate-time">${gateTime}</div>
    </div>
  `;
}

// Main data fetching function
function getDesiredGateCount() {
  const stored = localStorage.getItem('gateCount');
  const parsed = parseInt(stored, 10);
  if (!isNaN(parsed)) {
    return Math.max(1, Math.min(128, parsed));
  }
  return 32;
}

function setDesiredGateCount(value) {
  const clamped = Math.max(1, Math.min(128, parseInt(value, 10) || 32));
  localStorage.setItem('gateCount', String(clamped));
  if (gateCountInput) gateCountInput.value = String(clamped);
  return clamped;
}

async function fetchMoonData() {
  try {
    showLoading();
    
    // Fetch both moon phases and gate data
    const desiredCount = getDesiredGateCount();
    const [moonResponse, apiResponse] = await Promise.all([
      fetch('/moonphases'),
      fetch(`/data?count=${desiredCount}`)
    ]);

    if (!moonResponse.ok || !apiResponse.ok) {
      throw new Error('Failed to fetch data from server');
    }

    const moonData = await moonResponse.json();
    const apiData = await apiResponse.json();

    if (moonData.length > 0 && moonData[0].Error === 0) {
      const moon = moonData[0];
      const phase = moon.Phase;
      const imageUrl = `assets/images/${phaseImages[phase]}`;

      // Update favicon to match current moon phase
      setFavicon(imageUrl, 'image/svg+xml');

      // Update current moon section
      currentMoonSection.innerHTML = `
        <h2>Current Moon</h2>
        <div class="moon-phase-display">
          <img src="${imageUrl}" alt="${phase}" class="moon-phase-image" title="${phase}">
        </div>
        <div class="moon-info-grid">
          ${createInfoCard('Position', `${apiData.gate} - ${apiData.zodiac_sign} ${apiData.degree}'`)}
          ${createInfoCard('Moon Name', moon.Moon.join(', '))}
          ${createInfoCard('Phase', phase)}
          ${createInfoCard('Illumination', `${(moon.Illumination * 100).toFixed(1)}%`)}
        </div>
      `;

      // Update gates section
      const gates = apiData.next_gates || [];
      if (gates.length > 0) {
        const nextGate = gates[0];
        const remainingGates = gates.slice(1);
        
        gatesContent.innerHTML = `
          <div class="next-gate-section">
            <h3>Next Gate</h3>
            ${createGateItem(nextGate, true)}
          </div>
          ${remainingGates.length > 0 ? `
            <div class="upcoming-gates-section">
              <div class="upcoming-header">
                <h3>Upcoming Gate Changes</h3>
              </div>
              ${remainingGates.map(gate => createGateItem(gate)).join('')}
            </div>
          ` : ''}
        `;
      } else {
        gatesContent.innerHTML = `
          <div class="no-gates-message">
            <p>No upcoming gates available</p>
          </div>
        `;
      }

      updateLastUpdatedTime();
    } else {
      showError(moonData[0]?.ErrorMsg || 'Unknown error occurred while fetching moon data');
      setFavicon('assets/images/favicon.ico', 'image/x-icon');
    }
  } catch (error) {
    console.error('Error fetching moon data:', error);
    showError('Failed to fetch moon data. Please check your connection and try again.');
    setFavicon('assets/images/favicon.ico', 'image/x-icon');
  }
}

// Event listeners
refreshBtn.addEventListener('click', () => {
  refreshBtn.style.transform = 'rotate(360deg)';
  refreshBtn.style.transition = 'transform 1s ease';
  
  fetchMoonData();
  
  setTimeout(() => {
    refreshBtn.style.transform = 'rotate(0deg)';
  }, 800);
});

// Initialize gate count input
if (gateCountInput) {
  // Set initial value from localStorage or default
  gateCountInput.value = String(getDesiredGateCount());
  gateCountInput.addEventListener('change', () => {
    const clamped = setDesiredGateCount(gateCountInput.value);
    if (gateCountInput.value !== String(clamped)) {
      gateCountInput.value = String(clamped);
    }
    fetchMoonData();
  });
}

// Tooltip Manager
const Tooltip = (() => {
  let tooltipEl = null;
  let showTimer = null;
  let hideTimer = null;
  let gatesIndex = null; // Map gate name -> tooltip text
  let currentTargetEl = null; // Track the element that opened the tooltip

  function ensureEl() {
    if (!tooltipEl) {
      tooltipEl = document.createElement('div');
      tooltipEl.className = 'tooltip';
      tooltipEl.setAttribute('role', 'tooltip');
      tooltipEl.setAttribute('id', 'app-tooltip');
      document.body.appendChild(tooltipEl);
    }
    return tooltipEl;
  }

  async function loadGatesIndex() {
    if (gatesIndex) return gatesIndex;
    try {
      const res = await fetch('/gates');
      const data = await res.json();
      gatesIndex = new Map();
      data.forEach(g => {
        if (g && g.name && typeof g.tooltip === 'string') {
          gatesIndex.set(String(g.name).trim(), g.tooltip.trim());
        }
      });
      return gatesIndex;
    } catch (e) {
      gatesIndex = new Map();
      return gatesIndex;
    }
  }

  function positionTooltip(targetRect) {
    const el = ensureEl();
    const margin = 8;

    // Choose placement based on available space in viewport
    const spaceAbove = targetRect.top;
    const spaceBelow = window.innerHeight - targetRect.bottom;
    const placeBelow = el.offsetHeight + 10 > spaceAbove && spaceBelow >= spaceAbove;

    let top;
    if (placeBelow) {
      top = Math.min(window.innerHeight - el.offsetHeight - margin, targetRect.bottom + 10);
      el.setAttribute('data-placement', 'bottom');
    } else {
      top = Math.max(margin, targetRect.top - el.offsetHeight - 10);
      el.removeAttribute('data-placement');
    }

    let left = Math.max(
      margin,
      Math.min(
        window.innerWidth - el.offsetWidth - margin,
        targetRect.left + (targetRect.width - el.offsetWidth) / 2
      )
    );

    // Arrow position within the tooltip
    const arrowLeft = Math.max(
      14,
      Math.min(el.offsetWidth - 14, targetRect.left + targetRect.width / 2 - left - 6)
    );
    el.style.setProperty('--arrow-left', `${arrowLeft}px`);

    // Clamp within viewport
    el.style.top = `${Math.max(margin, Math.min(window.innerHeight - el.offsetHeight - margin, top))}px`;
    el.style.left = `${left}px`;
  }

  function getGateTooltipForElement(el) {
    // For .gate-item, the name text is inside .gate-name
    const gateNameEl = el.querySelector('.gate-name');
    const nameText = gateNameEl ? gateNameEl.textContent.trim() : '';
    if (nameText && gatesIndex && gatesIndex.has(nameText)) {
      return gatesIndex.get(nameText);
    }
    return null;
  }

  function getInfoCardTooltipForElement(el) {
    const label = el.querySelector('.info-label')?.textContent?.trim();
    if (label === 'Position') {
      // Expect format like: "Gate 17 - Aries 3°12'"
      const valueText = el.querySelector('.info-value')?.textContent?.trim() || '';
      const gateName = valueText.split(' - ')[0];
      if (gateName && gatesIndex && gatesIndex.has(gateName)) {
        return gatesIndex.get(gateName);
      }
    }
    return null;
  }

  async function show(targetEl, contentProducer) {
    clearTimeout(hideTimer);
    clearTimeout(showTimer);
    await loadGatesIndex();

    showTimer = setTimeout(() => {
      const el = ensureEl();
      const content = contentProducer();
      if (!content) return;
      el.textContent = content;
      el.setAttribute('data-show', 'true');
      // Measure and position after setting content
      requestAnimationFrame(() => {
        positionTooltip(targetEl.getBoundingClientRect());
      });
      const describedbyId = 'app-tooltip';
      targetEl.setAttribute('aria-describedby', describedbyId);
      currentTargetEl = targetEl;
    }, 150);
  }

  function hide(targetEl) {
    clearTimeout(showTimer);
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => {
      if (!tooltipEl) return;
      tooltipEl.removeAttribute('data-show');
      const elToClear = targetEl || currentTargetEl;
      elToClear?.removeAttribute('aria-describedby');
      if (!targetEl || elToClear === currentTargetEl) currentTargetEl = null;
    }, 0);
  }

  function attach(el, contentProducer) {
    if (!el) return;
    el.addEventListener('mouseenter', () => show(el, contentProducer));
    el.addEventListener('mouseleave', () => hide(el));
    el.addEventListener('focus', () => show(el, contentProducer));
    el.addEventListener('blur', () => hide(el));
    // Mobile tap
    el.addEventListener('touchstart', (e) => {
      e.stopPropagation();
      show(el, contentProducer);
    }, { passive: true });
  }

  // Dismiss on outside tap for mobile
  document.addEventListener('touchstart', () => hide(null), { passive: true });
  // Dismiss on scroll (viewport)
  window.addEventListener('scroll', () => hide(null), { passive: true });
  // Dismiss when the gates list scrolls (independent scroller)
  gatesContent?.addEventListener('scroll', () => hide(null), { passive: true });

  return { attach, getGateTooltipForElement, getInfoCardTooltipForElement };
})();

function wireTooltips() {
  // Gate items
  document.querySelectorAll('.gate-item').forEach(item => {
    item.setAttribute('tabindex', '0');
    Tooltip.attach(item, () => Tooltip.getGateTooltipForElement(item));
  });

  // Info cards
  document.querySelectorAll('.info-card').forEach(card => {
    card.setAttribute('tabindex', '0');
    Tooltip.attach(card, () => Tooltip.getInfoCardTooltipForElement(card));
  });
}

// Initialize the app
fetchMoonData().then(() => wireTooltips());

// Rewire tooltips after each data refresh
const originalFetchMoonData = fetchMoonData;
fetchMoonData = async function () {
  await originalFetchMoonData();
  wireTooltips();
}

// Auto-refresh every 10 minutes
setInterval(() => {
  fetchMoonData();
}, 600000);
