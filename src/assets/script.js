const moonPhaseDataContainer = document.getElementById('moon-phase-data');
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
async function fetchMoonPhaseData() {
  try {
    const unixTime = Math.floor(Date.now() / 1000);
    const response = await fetch(`https://api.farmsense.net/v1/moonphases/?d=${unixTime}`);
    const data = await response.json();

    const apiResponse = await fetch('/data');
    const apiData = await apiResponse.json();

    if (data.length > 0 && data[0].Error === 0) {
      const moon = data[0];
      const phase = moon.Phase;
     
      // Update the moon data container with the moon's data and gate
      const imageUrl = `assets/images/${phaseImages[phase] || "new_moon.png"}`;
      moonPhaseDataContainer.innerHTML = `
        <p><strong>Moon Name:</strong> ${moon.Moon.join(', ')}</p>
        <p><strong>Phase:</strong> ${moon.Phase}</p>
        <p><strong>Illumination:</strong> ${(moon.Illumination * 100).toFixed(1)}%</p>
        <p><strong>Zodiac Sign:</strong> ${apiData.zodiac_sign} ${apiData.degree}°</p>
        <img src="${imageUrl}" alt="${phase}">
      `;
    } else {
      moonPhaseDataContainer.innerHTML = `<p>Error fetching moon data: ${data[0]?.ErrorMsg || 'Unknown error'}</p>`;
    }
  } catch (error) {
    moonPhaseDataContainer.innerHTML = `<p>Error fetching moon data. Please try again later.</p>`;
    console.error(error);
  }
}

// Initialize
fetchMoonPhaseData();
loadJournalEntries();
journalForm.addEventListener('submit', saveJournalEntry);
setInterval(fetchMoonPhaseData, 600000);