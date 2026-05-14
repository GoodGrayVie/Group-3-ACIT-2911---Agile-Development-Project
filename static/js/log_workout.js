// exercises is injected by Flask/Jinja before this script loads:
// <script>const exercises = {{ exercises_json | safe }};</script>
// Shape: { weights: [{id, name}, ...], cardio: [{id, name}, ...] }

// ── DOM references ──────────────────────────────────────────────
const typeRadios = document.querySelectorAll('input[name="workout-type"]');
const unitRadios = document.querySelectorAll('input[name="weight-unit"]');
const exerciseSelect = document.getElementById("exercise-select");
const addSetBtn = document.getElementById("add-set-btn");
const sessionLog = document.getElementById("session-log");
const emptyMessage = document.getElementById("empty-message");
const today = new Date();
const local = new Date(today.getTime() - today.getTimezoneOffset() * 60000);
document.getElementById("workout-date").valueAsDate = local;

// ── Helpers ─────────────────────────────────────────────────────

/** Returns the currently selected weight unit ('kg' or 'lb') */
function getUnit() {
  return document.querySelector('input[name="weight-unit"]:checked').value;
}

// ── Unit toggle ─────────────────────────────────────────────────
// When the user switches between kg and lb, update all existing
// weight column headers and input aria-labels in the session log
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

// ── Workout type toggle ─────────────────────────────────────────
// When the user switches between weights and cardio, repopulate
// the exercise dropdown with the relevant exercise list
typeRadios.forEach((radio) => {
  radio.addEventListener("change", () => populateExercises(radio.value));
});

/**
 * Populates the exercise dropdown based on workout type.
 * @param {string} type - 'weights' or 'cardio'
 */
function populateExercises(type) {
  exerciseSelect.innerHTML = '<option value="">Select exercise...</option>';

  if (type === "weights") {
    // Group exercises by muscle group
    const groups = {};
    exercises[type].forEach((ex) => {
      if (!groups[ex.muscle_group]) groups[ex.muscle_group] = [];
      groups[ex.muscle_group].push(ex);
    });

    // Create an <optgroup> per muscle group
    Object.entries(groups).forEach(([groupName, exList]) => {
      const optgroup = document.createElement("optgroup");
      optgroup.label = groupName;
      exList.forEach((ex) => {
        const option = document.createElement("option");
        option.value = ex.id;
        option.textContent = ex.name;
        optgroup.appendChild(option);
      });
      exerciseSelect.appendChild(optgroup);
    });
  } else {
    // Cardio has no muscle groups — flat list
    exercises[type].forEach((ex) => {
      const option = document.createElement("option");
      option.value = ex.id;
      option.textContent = ex.name;
      exerciseSelect.appendChild(option);
    });
  }
}

// Initialise dropdown with weights exercises on page load
populateExercises("weights");

// ── Add set ─────────────────────────────────────────────────────
// When the user clicks '+ Add set':
// 1. Check an exercise is selected
// 2. Find or create an exercise group in the session log
// 3. Append an empty editable row to that group's table
// 4. Focus the first visible input in the new row
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

  // Reuse existing group if this exercise was already added,
  // otherwise create a new group section
  let group = document.querySelector(
    `[data-exercise="${exerciseId}"][data-type="${type}"]`,
  );
  if (!group) {
    group = createExerciseGroup(exerciseName, exerciseId, type);
    sessionLog.appendChild(group);
  }

  // Set number is based on how many rows already exist in this group
  const tbody = group.querySelector("tbody");
  const setNumber = tbody.querySelectorAll("tr").length + 1;
  const row = document.createElement("tr");

  if (type === "weights") {
    // Hidden inputs carry exercise id, set number, and unit to Flask on submit
    // Visible inputs let the user enter reps, weight, and heart rate inline
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
    // Cardio rows carry exercise id as a hidden input
    // Visible inputs let the user enter duration, distance, and heart rate
    row.innerHTML = `
      <td style="display:none"><input type="hidden" name="cardio_exercise_id[]" value="${exerciseId}"></td>
      <td><input type="number" name="duration[]" min="1" placeholder="—" aria-label="Duration (mins)"></td>
      <td><input type="number" name="distance[]" min="0" step="0.1" placeholder="—" aria-label="Distance (km)"></td>
      <td><input type="number" name="cardio_heart_rate[]" min="0" placeholder="—" aria-label="Heart rate (bpm)"></td>
      <td><button type="button" class="btn-remove" onclick="this.closest('tr').remove()">✕</button></td>
    `;
  }

  tbody.appendChild(row);
  // Skip hidden inputs when focusing
  row.querySelector("input:not([type='hidden'])").focus();
});

// ── Exercise group ───────────────────────────────────────────────
/**
 * Creates a new exercise group article element containing a
 * labelled header and an empty table with the correct columns
 * for the given workout type.
 *
 * @param {string} name       - Display name of the exercise
 * @param {string} exerciseId - Database id of the exercise
 * @param {string} type       - 'weights' or 'cardio'
 * @returns {HTMLElement}     - The constructed article element
 */
function createExerciseGroup(name, exerciseId, type) {
  const group = document.createElement("article");
  group.className = "exercise-group";
  group.dataset.exercise = exerciseId;
  group.dataset.type = type;

  // Header row shows exercise name and a type badge
  group.innerHTML = `
    <div class="group-header">
      <h3>${name}</h3>
      <span class="type-badge ${type}">${type}</span>
    </div>
  `;

  const table = document.createElement("table");
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");

  // Column headers differ based on workout type
  const unit = getUnit();
  const headers =
    type === "weights"
      ? ["Set", "Reps", `Weight (${unit})`, "Heart rate (bpm)", ""]
      : ["Duration (mins)", "Distance (km)", "Heart rate (bpm)", ""];

  headers.forEach((text) => {
    const th = document.createElement("th");
    th.textContent = text;
    // Mark weight header so it can be updated when unit changes
    if (text.startsWith("Weight")) th.className = "weight-header";
    headerRow.appendChild(th);
  });

  thead.appendChild(headerRow);
  table.appendChild(thead);
  table.appendChild(document.createElement("tbody"));
  group.appendChild(table);

  return group;
}
