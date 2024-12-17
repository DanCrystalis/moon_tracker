const moonDataContainer = document.getElementById('moon-data');

const phaseImages = {
  "Dark Moon": "dark_moon.svg",
  "Waxing Crescent": "waxing_crescent.svg",
  "1st Quarter": "1st_quarter.svg",
  "Waxing Gibbous": "waxing_gibbous.svg",
  "Full Moon": "full_moon.svg",
  "Waning Gibbous": "waning_gibbous.svg",
  "3rd Quarter": "last_quarter.svg",
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
        <p><strong>Moon Name:</strong><br/>${moon.Moon.join(', ')}</p>
        <p><strong>Phase:</strong><br/>${moon.Phase}</p>
        <p><strong>Illumination:</strong><br/>${(moon.Illumination * 100).toFixed(1)}%</p>
        <p><strong>Zodiac Sign:</strong><br/>${apiData.zodiac_sign} ${apiData.degree}°</p>
        <p><strong>${apiData.gate}<br/></strong></p>
        <br/><strong>Next Gate:</strong><br/>
      `;

if (apiData.next_10_gates.length > 0) {
  const firstGate = apiData.next_10_gates[0];
  moonDataContainer.innerHTML +=
    `${firstGate[1]}<br/>${firstGate[0].replace(/T/g, ' ').slice(0, 16)} UTC<br/>`;
}
      const nextGatesContainer = document.createElement('div');
      nextGatesContainer.id = 'nextGatesContainer';
      nextGatesContainer.style.display = 'none';

      nextGatesContainer.innerHTML += `<br/><strong>Next Nine Gates:</strong><br>`;

      apiData.next_10_gates.slice(1).forEach((gate, index) => {
        nextGatesContainer.innerHTML += `${gate[1]} - ${gate[0].replace(/T/g, ' ').slice(0, 16)} UTC`;
        if (index < apiData.next_10_gates.length - 1) {
          nextGatesContainer.innerHTML += `<br>`;
        }
      });

      moonDataContainer.appendChild(nextGatesContainer);

      const toggleButton = document.createElement('button');
      toggleButton.textContent = 'Show Next Nine Gates';
      toggleButton.addEventListener('click', () => {
        if (nextGatesContainer.style.display === 'none') {
          nextGatesContainer.style.display = 'block';
          toggleButton.textContent = 'Hide Next Nine Gates';
        } else {
          nextGatesContainer.style.display = 'none';
          toggleButton.textContent = 'Show Next Nine Gates';
        }
      });

      moonDataContainer.appendChild(toggleButton);

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