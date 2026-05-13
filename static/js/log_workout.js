// exercises is injected by Flask/Jinja before this script loads:
// <script>const exercises = {{ exercises_json | safe }};</script>

const typeRadios = document.querySelectorAll('input[name="workout-type"]');
const unitRadios = document.querySelectorAll('input[name="weight-unit"]');
const exerciseSelect = document.getElementById("exercise-select");
const addSetBtn = document.getElementById("add-set-btn");
const sessionLog = document.getElementById("session-log");
const emptyMessage = document.getElementById("empty-message");

function getUnit() {
  return document.querySelector('input[name="weight-unit"]:checked').value;
}

// Update all existing weight column headers and input labels when unit changes
unitRadios.forEach((radio) => {
  radio.addEventListener("change", () => {
    const unit = radio.value;
    document.querySelectorAll(".weight-header").forEach((th) => {
      th.textContent = `Weight (${unit})`;
    });
    document
      .querySelectorAll('input[aria-label^="Weight"]')
      .forEach((input) => {
        input.setAttribute("aria-label", `Weight (${unit})`);
      });
  });
});

// Swap exercise dropdown options when workout type changes
typeRadios.forEach((radio) => {
  radio.addEventListener("change", () => populateExercises(radio.value));
});

function populateExercises(type) {
  exerciseSelect.innerHTML = '<option value="">Select exercise...</option>';
  exercises[type].forEach((ex) => {
    const option = document.createElement("option");
    option.value = ex.id;
    option.textContent = ex.name;
    exerciseSelect.appendChild(option);
  });
}

populateExercises("weights");

// Add an empty editable row to the session log
addSetBtn.addEventListener("click", () => {
  const type = document.querySelector(
    'input[name="workout-type"]:checked',
  ).value;
  const exerciseName =
    exerciseSelect.options[exerciseSelect.selectedIndex]?.text;
  const exerciseId = exerciseSelect.value;

  if (!exerciseId) {
    alert("Please select an exercise.");
    return;
  }

  emptyMessage.hidden = true;

  let group = document.querySelector(
    `[data-exercise="${exerciseId}"][data-type="${type}"]`,
  );
  if (!group) {
    group = createExerciseGroup(exerciseName, exerciseId, type);
    sessionLog.appendChild(group);
  }

  const tbody = group.querySelector("tbody");
  const setNumber = tbody.querySelectorAll("tr").length + 1;
  const row = document.createElement("tr");

  if (type === "weights") {
    row.innerHTML = `
      <td style="display:none"><input type="hidden" name="exercise_id[]" value="${exerciseId}"></td>
      <td style="display:none"><input type="hidden" name="set_number[]" value="${setNumber}"></td>
      <td style="display:none"><input type="hidden" name="weight_unit[]" value="${getUnit()}"></td>
      <td>${setNumber}</td>
      <td><input type="number" name="reps[]" min="1" placeholder="—" aria-label="Reps"></td>
      <td><input type="number" name="weight[]" min="0" step="0.5" placeholder="—" aria-label="Weight (${getUnit()})"></td>
      <td><input type="number" name="set_heart_rate[]" min="0" placeholder="—" aria-label="Heart rate (bpm)"></td>
      <td><button type="button" class="btn-remove" onclick="this.closest('tr').remove()">✕</button></td>
    `;
  } else {
    row.innerHTML = `
      <td style="display:none"><input type="hidden" name="cardio_exercise_id[]" value="${exerciseId}"></td>
      <td><input type="number" name="duration[]" min="1" placeholder="—" aria-label="Duration (mins)"></td>
      <td><input type="number" name="distance[]" min="0" step="0.1" placeholder="—" aria-label="Distance (km)"></td>
      <td><input type="number" name="cardio_heart_rate[]" min="0" placeholder="—" aria-label="Heart rate (bpm)"></td>
      <td><button type="button" class="btn-remove" onclick="this.closest('tr').remove()">✕</button></td>
    `;
  }

  tbody.appendChild(row);
  row.querySelector("input:not([type='hidden'])").focus();
});

function createExerciseGroup(name, exerciseId, type) {
  const group = document.createElement("article");
  group.className = "exercise-group";
  group.dataset.exercise = exerciseId;
  group.dataset.type = type;

  group.innerHTML = `
    <div class="group-header">
      <h3>${name}</h3>
      <span class="type-badge ${type}">${type}</span>
    </div>
  `;

  const table = document.createElement("table");
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");

  const unit = getUnit();
  const headers =
    type === "weights"
      ? ["Set", "Reps", `Weight (${unit})`, "Heart rate (bpm)", ""]
      : ["Duration (mins)", "Distance (km)", "Heart rate (bpm)", ""];

  headers.forEach((text) => {
    const th = document.createElement("th");
    th.textContent = text;
    if (text.startsWith("Weight")) th.className = "weight-header";
    headerRow.appendChild(th);
  });

  thead.appendChild(headerRow);
  table.appendChild(thead);
  table.appendChild(document.createElement("tbody"));
  group.appendChild(table);

  return group;
}