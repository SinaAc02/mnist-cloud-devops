from io import BytesIO

import pytest
import numpy as np
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw

from app import app, session
from src.preprocessing import preprocess_image


client = TestClient(app)


def make_png(empty=False):
    image = Image.new("L", (280, 280), color=0)
    if not empty:
        draw = ImageDraw.Draw(image)
        draw.line((140, 55, 140, 225), fill=255, width=20)

    content = BytesIO()
    image.save(content, format="PNG")
    return content.getvalue()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_prediction_returns_all_probabilities():
    response = client.post(
        "/predict",
        files={"file": ("digit.png", make_png(), "image/png")},
    )
    result = response.json()

    assert response.status_code == 200
    assert result["prediction"] in range(10)
    assert set(result["probabilities"]) == {str(number) for number in range(10)}
    assert sum(result["probabilities"].values()) == pytest.approx(1.0, abs=0.00001)


def test_empty_canvas_is_rejected():
    response = client.post(
        "/predict",
        files={"file": ("empty.png", make_png(empty=True), "image/png")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "The canvas is empty"


def test_non_png_file_is_rejected():
    response = client.post(
        "/predict",
        files={"file": ("digit.txt", b"not an image", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please upload a PNG image"


def test_preprocessing_creates_model_shape():
    image = Image.open(BytesIO(make_png()))
    model_input, processed_image = preprocess_image(image)

    assert model_input.shape == (1, 1, 28, 28)
    assert model_input.dtype == np.float32
    assert processed_image.size == (28, 28)


def test_model_produces_ten_scores():
    model_input = np.zeros((1, 1, 28, 28), dtype=np.float32)
    output = session.run(None, {"image": model_input})[0]

    assert output.shape == (1, 10)
