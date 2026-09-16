"""FastAPI application for MNIST predictions."""

from io import BytesIO
from pathlib import Path

import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError

from src.model import EnhancedCNN
from src.preprocessing import preprocess_image


app = FastAPI(title="MNIST Digit Classifier")
static_directory = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_directory), name="static")

model = EnhancedCNN()
checkpoint_path = Path(__file__).parent / "artifacts" / "best_model.pt"
checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()


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
        tensor, _ = preprocess_image(image)
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid image")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    with torch.no_grad():
        output = model(tensor)
        probabilities = torch.softmax(output, dim=1)[0]

    prediction = int(probabilities.argmax())
    probability_values = {
        str(number): round(float(probability), 6)
        for number, probability in enumerate(probabilities)
    }

    return {
        "prediction": prediction,
        "probabilities": probability_values,
    }
