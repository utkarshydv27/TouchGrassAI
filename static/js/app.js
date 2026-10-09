
const form = document.querySelector("#mission-form");
const generateButton = document.querySelector("#generate-button");
const resultSection = document.querySelector("#result-section");
const missionResult = document.querySelector("#mission-result");
const completeButton = document.querySelector("#complete-button");

const minutesTotal = document.querySelector("#minutes-total");
const missionsTotal = document.querySelector("#missions-total");
const resetButton = document.querySelector("#reset-progress");

const STORAGE_KEY = "touchgrass-progress-v1";
let currentMissionMinutes = 15;
let currentMissionText = "";
let currentMissionCompleted = false;

function loadProgress() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    return {
      minutes: Number.isFinite(saved.minutes) && saved.minutes >= 0
        ? saved.minutes : 0,
      missions: Number.isFinite(saved.missions) && saved.missions >= 0
        ? saved.missions : 0
    };
  } catch {
    return { minutes: 0, missions: 0 };
  }
}

function renderProgress() {
  const progress = loadProgress();
  minutesTotal.textContent = String(progress.minutes);
  missionsTotal.textContent = String(progress.missions);
}

function showMessage(message) {
  missionResult.replaceChildren();
  const paragraph = document.createElement("p");
  paragraph.textContent = message;
  missionResult.appendChild(paragraph);
  resultSection.hidden = false;
}

function renderMission(text) {
  missionResult.replaceChildren();

  // Use textContent rather than innerHTML because AI output is untrusted.
  const paragraph = document.createElement("p");
  paragraph.textContent = text;
  missionResult.appendChild(paragraph);

  resultSection.hidden = false;
  resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const minutes = Number(formData.get("minutes"));
  const interest = formData.get("interest");
  const difficulty = formData.get("difficulty");

  generateButton.disabled = true;
  generateButton.querySelector("span").textContent = "Creating your mission...";
  completeButton.disabled = true;
  showMessage("Your local AI is thinking. This can take a little while.");

  try {
    const response = await fetch("/api/mission", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ minutes, interest, difficulty })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Could not create your mission.");
    }

    currentMissionMinutes = minutes;
    currentMissionText = data.mission;
    currentMissionCompleted = false;

    renderMission(currentMissionText);
    completeButton.disabled = false;
  } catch (error) {
    showMessage(
      error.message || "Something went wrong. Check that Flask and Ollama are running."
    );
  } finally {
    generateButton.disabled = false;
    generateButton.querySelector("span").textContent =
      "Find my outdoor mission";
  }
});

completeButton.addEventListener("click", () => {
  if (!currentMissionText || currentMissionCompleted) return;

  const progress = loadProgress();
  progress.minutes += currentMissionMinutes;
  progress.missions += 1;

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    currentMissionCompleted = true;
    completeButton.disabled = true;
    completeButton.textContent = "✓ Mission completed — nice work!";
    renderProgress();
  } catch {
    showMessage(
      "Your browser could not save progress. Check browser storage settings."
    );
  }
});

resetButton.addEventListener("click", () => {
  if (!window.confirm("Reset all saved outdoor progress?")) return;

  try {
    localStorage.removeItem(STORAGE_KEY);
    renderProgress();
  } catch {
    showMessage("Could not reset saved progress in this browser.");
  }
});

renderProgress();
