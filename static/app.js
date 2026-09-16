const canvas = document.querySelector("#drawingCanvas");
const context = canvas.getContext("2d");
const brushSize = document.querySelector("#brushSize");
const clearButton = document.querySelector("#clearButton");
const predictionValue = document.querySelector("#predictionValue");
const probabilityList = document.querySelector("#probabilityList");
const statusText = document.querySelector("#status");

let drawing = false;
let hasDrawing = false;
let predictionTimer;
let latestRequest = 0;

function clearCanvas() {
  context.fillStyle = "black";
  context.fillRect(0, 0, canvas.width, canvas.height);
  hasDrawing = false;
  predictionValue.textContent = "—";
  statusText.textContent = "Start drawing to see the probabilities.";
  updateProbabilities({}, -1);
}

function canvasPosition(event) {
  const rectangle = canvas.getBoundingClientRect();
  return {
    x: (event.clientX - rectangle.left) * (canvas.width / rectangle.width),
    y: (event.clientY - rectangle.top) * (canvas.height / rectangle.height),
  };
}

function startDrawing(event) {
  drawing = true;
  hasDrawing = true;
  canvas.setPointerCapture(event.pointerId);
  const point = canvasPosition(event);
  context.beginPath();
  context.moveTo(point.x, point.y);
  context.lineTo(point.x, point.y);
  context.stroke();
  schedulePrediction();
}

function draw(event) {
  if (!drawing) return;
  const point = canvasPosition(event);
  context.lineTo(point.x, point.y);
  context.stroke();
  schedulePrediction();
}

function stopDrawing() {
  if (!drawing) return;
  drawing = false;
  clearTimeout(predictionTimer);
  predictCanvas();
}

function schedulePrediction() {
  clearTimeout(predictionTimer);
  predictionTimer = setTimeout(predictCanvas, 150);
}

function updateProbabilities(probabilities, prediction) {
  probabilityList.innerHTML = "";

  for (let number = 0; number <= 9; number += 1) {
    const probability = probabilities[number] ?? 0;
    const percentage = probability * 100;
    const row = document.createElement("div");
    row.className = `probability-row${number === prediction ? " active" : ""}`;
    row.innerHTML = `
      <strong>${number}</strong>
      <div class="bar-track"><div class="bar-fill" style="width: ${percentage}%"></div></div>
      <span class="percentage">${percentage.toFixed(1)}%</span>
    `;
    probabilityList.append(row);
  }
}

async function predictCanvas() {
  if (!hasDrawing) return;

  const requestNumber = ++latestRequest;
  statusText.textContent = "Reading your drawing…";

  const image = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
  const formData = new FormData();
  formData.append("file", image, "digit.png");

  try {
    const response = await fetch("/predict", { method: "POST", body: formData });
    const result = await response.json();

    if (!response.ok) throw new Error(result.detail || "Prediction failed");
    if (requestNumber !== latestRequest) return;

    predictionValue.textContent = result.prediction;
    statusText.textContent = "Probabilities update as you draw.";
    updateProbabilities(result.probabilities, result.prediction);
  } catch (error) {
    if (requestNumber !== latestRequest) return;
    statusText.textContent = error.message;
  }
}

context.lineCap = "round";
context.lineJoin = "round";
context.strokeStyle = "white";

brushSize.addEventListener("input", () => {
  context.lineWidth = Number(brushSize.value);
});
clearButton.addEventListener("click", clearCanvas);
canvas.addEventListener("pointerdown", startDrawing);
canvas.addEventListener("pointermove", draw);
canvas.addEventListener("pointerup", stopDrawing);
canvas.addEventListener("pointercancel", stopDrawing);

context.lineWidth = Number(brushSize.value);
clearCanvas();
