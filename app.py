"""FastAPI application for MNIST predictions."""

from io import BytesIO
from pathlib import Path

import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError

from src.preprocessing import preprocess_image


app = FastAPI(title="MNIST Digit Classifier")
static_directory = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_directory), name="static")

model_path = Path(__file__).parent / "artifacts" / "mnist_model.onnx"
session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(static_directory / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type != "image/png":
        raise HTTPException(status_code=400, detail="Please upload a PNG image")

    try:
        image = Image.open(BytesIO(await file.read()))
        image.load()
        model_input, _ = preprocess_image(image)
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid image")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    scores = session.run(None, {"image": model_input})[0][0]
    probabilities = np.exp(scores - np.max(scores))
    probabilities = probabilities / probabilities.sum()

    prediction = int(probabilities.argmax())
    probability_values = {
        str(number): round(float(probability), 6)
        for number, probability in enumerate(probabilities)
    }

    return {
        "prediction": prediction,
        "probabilities": probability_values,
    }
