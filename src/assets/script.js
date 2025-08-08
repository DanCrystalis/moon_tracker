// DOM Elements
const currentMoonSection = document.getElementById('current-moon');
const gatesContent = document.getElementById('gates-content');
const updateTimeElement = document.getElementById('update-time');
const refreshBtn = document.getElementById('refresh-btn');
const loadingSpinner = document.getElementById('loading-spinner');

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

function showLoading() {
  loadingSpinner.style.display = 'block';
  currentMoonSection.innerHTML = `
    <h2>Current Moon</h2>
    <div class="loading-spinner" id="loading-spinner">
      <div class="spinner"></div>
      <p>Fetching moon data...</p>
    </div>
  `;
  
  // Also show loading state for gates section
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
      <div class="info-label">${label}</div>
      <div class="info-value">${value}</div>
    </div>
  `;
}

function createGateItem(gate, isNext = false) {
  const gateTime = formatDateTime(gate[0]);
  const gateName = gate[1];
  
  return `
    <div class="gate-item ${isNext ? 'next-gate' : ''}">
      <div class="gate-name">${gateName}</div>
      <div class="gate-time">${gateTime}</div>
    </div>
  `;
}

// Main data fetching function
async function fetchMoonData() {
  try {
    showLoading();
    
    // Fetch both moon phases and gate data
    const [moonResponse, apiResponse] = await Promise.all([
      fetch('/moonphases'),
      fetch('/data')
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

      // Update current moon section
      currentMoonSection.innerHTML = `
        <h2>Current Moon</h2>
        <div class="moon-phase-display">
          <img src="${imageUrl}" alt="${phase}" class="moon-phase-image" title="${phase}">
        </div>
        <div class="moon-info-grid">
          ${createInfoCard('Moon Name', moon.Moon.join(', '))}
          ${createInfoCard('Phase', phase)}
          ${createInfoCard('Illumination', `${(moon.Illumination * 100).toFixed(1)}%`)}
          ${createInfoCard('Position', `${apiData.gate} - ${apiData.zodiac_sign} ${apiData.degree}°`)}
        </div>
      `;

      // Update gates section
      if (apiData.next_10_gates && apiData.next_10_gates.length > 0) {
        const nextGate = apiData.next_10_gates[0];
        const remainingGates = apiData.next_10_gates.slice(1);
        
        gatesContent.innerHTML = `
          <div class="next-gate-section">
            <h3>Next Gate</h3>
            ${createGateItem(nextGate, true)}
          </div>
          ${remainingGates.length > 0 ? `
            <div class="upcoming-gates-section">
              <h3>Upcoming Gate Changes</h3>
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
    }
  } catch (error) {
    console.error('Error fetching moon data:', error);
    showError('Failed to fetch moon data. Please check your connection and try again.');
  }
}

// Event listeners
refreshBtn.addEventListener('click', () => {
  // Add visual feedback for refresh
  refreshBtn.style.transform = 'rotate(360deg)';
  refreshBtn.style.transition = 'transform 0.5s ease';
  
  fetchMoonData();
  
  // Reset the rotation after animation
  setTimeout(() => {
    refreshBtn.style.transform = 'rotate(0deg)';
  }, 500);
});

// Add some CSS for the new elements
const additionalStyles = `
  .retry-btn {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 10px 20px;
    color: #ffffff;
    cursor: pointer;
    margin-top: 15px;
    transition: all 0.3s ease;
  }
  
  .retry-btn:hover {
    background: rgba(255, 255, 255, 0.2);
  }
  
  .next-gate {
    border-left: 4px solid #4CAF50;
    background: rgba(76, 175, 80, 0.1);
  }
  
  .next-gate-section h3,
  .upcoming-gates-section h3 {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.8);
    margin: 20px 0 10px 0;
    padding-bottom: 5px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .no-gates-message {
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    padding: 40px 20px;
  }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// Initialize the app
fetchMoonData();

// Auto-refresh every 10 minutes
setInterval(fetchMoonData, 600000);
