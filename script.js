const moonDataContainer = document.getElementById('moon-data');
const journalForm = document.getElementById('journal-form');
const journalEntries = document.getElementById('journal-entries');
const journalPhase = document.getElementById('journal-phase');
const astrologicalInsightsContainer = document.getElementById('astrological-insights');

// Mapping moon phases to image file names
const phaseImages = {
  "New Moon": "new_moon.svg",
  "Waxing Crescent": "waxing_crescent.svg",
  "First Quarter": "first_quarter.svg",
  "Waxing Gibbous": "waxing_gibbous.svg",
  "Full Moon": "full_moon.svg",
  "Waning Gibbous": "waning_gibbous.svg",
  "Last Quarter": "last_quarter.svg",
  "Waning Crescent": "waning_crescent.svg"
};

// Load saved journal entries from localStorage
function loadJournalEntries() {
  const savedEntries = JSON.parse(localStorage.getItem('moonJournal')) || [];
  journalEntries.innerHTML = savedEntries.map(entry => `
    <li>
      <strong>Date:</strong> ${entry.date}<br>
      <strong>Phase:</strong> ${entry.phase}<br>
      <strong>Mood:</strong> ${entry.mood}<br>
      <strong>Activities:</strong> ${entry.activities}<br>
      <strong>Reflections:</strong> ${entry.reflections}<br>
      <strong>Goals:</strong> ${entry.goals}
    </li>
  `).join('');
}

// Save a new journal entry
function saveJournalEntry(event) {
  event.preventDefault();

  const entry = {
    date: document.getElementById('journal-date').value,
    phase: document.getElementById('journal-phase').value,
    mood: document.getElementById('journal-mood').value,
    activities: document.getElementById('journal-activities').value,
    reflections: document.getElementById('journal-reflections').value,
    goals: document.getElementById('journal-goals').value
  };

  const savedEntries = JSON.parse(localStorage.getItem('moonJournal')) || [];
  savedEntries.push(entry);
  localStorage.setItem('moonJournal', JSON.stringify(savedEntries));
  loadJournalEntries();
  journalForm.reset();
}

// Fetch moon data and set the journal phase
async function fetchMoonData() {
  try {
    const unixTime = Math.floor(Date.now() / 1000);
    const response = await fetch(`https://api.farmsense.net/v1/moonphases/?d=${unixTime}`);
    const data = await response.json();

    if (data.length > 0 && data[0].Error === 0) {
      const moon = data[0];
      const phase = moon.Phase;

      // Update the moon data container with the moon's data and gate
      const imageUrl = `images/${phaseImages[phase] || "new_moon.png"}`;
      moonDataContainer.innerHTML = `
        <p><strong>Moon Name:</strong> ${moon.Moon.join(', ')}</p>
        <p><strong>Phase:</strong> ${moon.Phase}</p>
        <p><strong>Illumination:</strong> ${(moon.Illumination * 100).toFixed(1)}%</p>
        <p><strong>Distance:</strong> ${moon.Distance.toFixed(1)} km</p>
        <img src="${imageUrl}" alt="${phase}">
      `;
    } else {
      moonDataContainer.innerHTML = `<p>Error fetching moon data: ${data[0]?.ErrorMsg || 'Unknown error'}</p>`;
    }
  } catch (error) {
    moonDataContainer.innerHTML = `<p>Error fetching moon data. Please try again later.</p>`;
    console.error(error);
  }
}

// Fetch moon data from the generated JSON file
async function fetchAstrologicalInsights() {
  try {
    const response = await fetch('moon_data.json');
    const data = await response.json();

    astrologicalInsightsContainer.innerHTML = `
      <h2>Astrological Insights ✨</h2>
      <p><strong>Zodiac Sign:</strong> ${data.zodiac_sign}</p>
     <p><strong>Degree:</strong> ${data.degree}°</p>
    `;
  } catch (error) {
    console.error("Error fetching astrological insights:", error);
    astrologicalInsightsContainer.innerHTML = `<p>Error: Unable to retrieve astrological insights.</p>`;
  }
}
/*async function fetchAstrologicalInsights() {
  try {
    const moonData = JSON.parse(localStorage.getItem('moon_data'));
    if (!moonData) {
      throw new Error('Moon data not found');
    }

    astrologicalInsightsContainer.innerHTML = `
      <h2>Astrological Insights ✨</h2>
      <p><strong>Zodiac Sign:</strong> ${moonData.zodiac_sign}</p>
      <p><strong>Degree:</strong> ${moonData.degree}°</p>
    `;
  } catch (error) {
    console.error("Error fetching astrological insights:", error);
    astrologicalInsightsContainer.innerHTML = `<p>Error: Unable to retrieve astrological insights.</p>`;
  }
}*/


// Initialize
fetchAstrologicalInsights();
fetchMoonData();
loadJournalEntries();
journalForm.addEventListener('submit', saveJournalEntry);
setInterval(fetchMoonData, 600000);