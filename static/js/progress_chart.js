let chart = null;

// Chart elements
const exerciseSelect = document.getElementById("exerciseSelect");
const statSelect = document.getElementById("statSelect");
const yearSelect = document.getElementById("yearSelect");

const loadingState = document.getElementById("loadingState");
const emptyState = document.getElementById("emptyState");

const statBest = document.getElementById("statBest");
const statBestDate = document.getElementById("statBestDate");
const statAvg = document.getElementById("statAvg");
const statCount = document.getElementById("statCount");
const statLatest = document.getElementById("statLatest");
const statLatestDate = document.getElementById("statLatestDate");

const chartTitle = document.getElementById("chartTitle");
const chartSubtitle = document.getElementById("chartSubtitle");

const statAvgLabel = document.getElementById("statAvgLabel");
const statBestLabel = document.getElementById("statBestLabel");

const statLabelMap = {
  weight: "Best weight",
  reps: "Best reps",
  distance: "Best km",
  duration: "Best time",
  heart_rate: "Best heart rate",
};

const statAvgLabelMap = {
  weight: "Average weight",
  reps: "Average reps",
  distance: "Average km",
  duration: "Average time",
  heart_rate: "Average heart rate",
};
// -------------------------------
//  Populate dropdowns on load
// -------------------------------
async function init() {
  await loadExercises();
  loadStats();
  loadYears();
  updateChart();
}
async function loadExercises() {
  const res = await fetch("/view-progress/exercises");
  const data = await res.json();

  exerciseSelect.innerHTML = "";

  const strengthGroup = document.createElement("optgroup");
  strengthGroup.label = "Strength";

  data.strength.forEach((ex) => {
    const opt = document.createElement("option");
    opt.value = ex.id;
    opt.dataset.type = "strength";
    opt.textContent = ex.name;
    strengthGroup.appendChild(opt);
  });

  const cardioGroup = document.createElement("optgroup");
  cardioGroup.label = "Cardio";

  data.cardio.forEach((ex) => {
    const opt = document.createElement("option");
    opt.value = ex.id;
    opt.dataset.type = "cardio";
    opt.textContent = ex.name;
    cardioGroup.appendChild(opt);
  });

  exerciseSelect.appendChild(strengthGroup);
  exerciseSelect.appendChild(cardioGroup);

  const firstOption = exerciseSelect.querySelector("option");
  if (firstOption) firstOption.selected = true;
}

function loadStats() {
  const type = exerciseSelect.selectedOptions[0]?.dataset.type;

  statSelect.innerHTML = "";

  if (type === "strength") {
    statSelect.innerHTML = `
            <option value="weight">Weight</option>
            <option value="reps">Reps</option>
        `;
  } else {
    statSelect.innerHTML = `
            <option value="distance">Distance (km)</option>
            <option value="duration">Duration (min)</option>
            <option value="heart_rate">Heart Rate</option>
        `;
  }
}

// Populate year dropdown
function loadYears() {
  const currentYear = new Date().getFullYear();
  yearSelect.innerHTML = "";

  for (let y = currentYear; y >= currentYear - 5; y--) {
    const opt = document.createElement("option");
    opt.value = y;
    opt.textContent = y;
    yearSelect.appendChild(opt);
  }
}

// -------------------------------
//  Fetch chart data
// -------------------------------
async function updateChart() {
  console.log("updateChart fired");
  const exerciseId = exerciseSelect.value;
  const stat = statSelect.value;
  const year = yearSelect.value;
  const type = exerciseSelect.selectedOptions[0].dataset.type;
  console.log(
    "exercise:",
    exerciseId,
    "type:",
    type,
    "stat:",
    stat,
    "year:",
    year,
  );

  if (!exerciseId) return;

  showLoading();

  const res = await fetch(
    `/view-progress/data?exercise_id=${exerciseId}&stat=${stat}&year=${year}&type=${type}`,
  );

  const data = await res.json();

  hideLoading();

  if (!data.labels.length) {
    showEmpty();
    clearStats();

    // hide chart when no data
    if (chart) {
      chart.destroy();
      chart = null;
    }

    return;
  }
  hideEmpty();
  updateStats(data);
  renderChart(data, stat);
}

// -------------------------------
//  Render Chart.js
// -------------------------------
function renderChart(data, stat) {
  if (chart) chart.destroy();

  chart = new Chart(document.getElementById("progressChart"), {
    type: "line",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: stat,
          data: data.values,
          borderColor: "rgb(200, 241, 53)",
          backgroundColor: "rgba(200, 241, 53, 0.15)",
          tension: 0.3,
          borderWidth: 2,
          pointRadius: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { color: "#6b7585" },
          offset: false,
        },

        y: { ticks: { color: "#6b7585" } },
      },
    },
  });
  chart.resize();
}

// -------------------------------
//  Update stat cards
// -------------------------------
function updateStats(data) {
  const stat = statSelect.value;

  statBestLabel.textContent = statLabelMap[stat] || "Best";
  statAvgLabel.textContent = statAvgLabelMap[stat] || "Average";

  const values = data.values;

  const best = Math.max(...values);
  const bestIndex = values.indexOf(best);

  const latest = values[values.length - 1];

  statBest.textContent = best;
  statBestDate.textContent = data.labels[bestIndex];

  statAvg.textContent = (
    values.reduce((a, b) => a + b, 0) / values.length
  ).toFixed(1);

  statCount.textContent = values.length;

  statLatest.textContent = latest;
  statLatestDate.textContent = data.labels[data.labels.length - 1];
  const exerciseName = exerciseSelect.selectedOptions[0].textContent;
  chartTitle.innerHTML = `<span style="color: var(--accent)">Exercise:</span> ${exerciseName}`;

  chartSubtitle.textContent = `Tracking ${stat} in ${yearSelect.value}`;
}

function clearStats() {
  statBest.textContent = "—";
  statBestDate.textContent = "no data";
  statAvg.textContent = "—";
  statCount.textContent = "—";
  statLatest.textContent = "—";
  statLatestDate.textContent = "no data";
}

// -------------------------------
//  UI State Helpers
// -------------------------------
function showLoading() {
  loadingState.classList.add("visible");
}
function hideLoading() {
  loadingState.classList.remove("visible");
}
function showEmpty() {
  emptyState.classList.add("visible");
}
function hideEmpty() {
  emptyState.classList.remove("visible");
}

// -------------------------------
//  Event Listeners
// -------------------------------
exerciseSelect.addEventListener("change", () => {
  loadStats();
  updateChart();
});
statSelect.addEventListener("change", updateChart);
yearSelect.addEventListener("change", updateChart);

init();
