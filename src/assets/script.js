const moonDataContainer = document.getElementById('moon-data');
const astrologicalInsightsContainer = document.getElementById('astrological-insights');

const phaseImages = {
  "Dark Moon": "dark_moon.svg",
  "Waxing Crescent": "waxing_crescent.svg",
  "First Quarter": "first_quarter.svg",
  "Waxing Gibbous": "waxing_gibbous.svg",
  "Full Moon": "full_moon.svg",
  "Waning Gibbous": "waning_gibbous.svg",
  "Last Quarter": "last_quarter.svg",
  "Waning Crescent": "waning_crescent.svg"
};

async function fetchMoonData() {
  try {
    const unixTime = Math.floor(Date.now() / 1000);
    const response = await fetch(`https://api.farmsense.net/v1/moonphases/?d=${unixTime}`);
    const data = await response.json();

    const apiResponse = await fetch('/data');
    const apiData = await apiResponse.json();

    if (data.length > 0 && data[0].Error === 0) {
      const moon = data[0];
      const phase = moon.Phase;
      const imageUrl = `assets/images/${phaseImages[phase]}`;

      moonDataContainer.innerHTML = `
        <img src="${imageUrl}" alt="${phase}" id="${(phase.replace(/ /g, '_'))}">
        <p><strong>Moon Name:</strong> ${moon.Moon.join(', ')}</p>
        <p><strong>Phase:</strong> ${moon.Phase}</p>
        <p><strong>Illumination:</strong> ${(moon.Illumination * 100).toFixed(1)}%</p>
        <p><strong>Zodiac Sign:</strong> ${apiData.zodiac_sign} ${apiData.degree}°</p>
        <p><strong> ${apiData.gate}</strong></p>
        <p><strong>Next Gate:</strong></p>
        <p>${apiData.next_gate}</p>
        <p>${apiData.next_gate_change_time.replace(/T/g, ' ')} UTC</p>
        
      `;
    } else {
      moonDataContainer.innerHTML = `<p>Error fetching moon data: ${data[0]?.ErrorMsg || 'Unknown error'}</p>`;
    }
  } catch (error) {
    moonDataContainer.innerHTML = `<p>Error fetching moon data. Please try again later.</p>`;
    console.error(error);
  }
}

fetchMoonData();
setInterval(fetchMoonData, 600000);