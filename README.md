# MNIST Digit Classifier

A small PyTorch and FastAPI application that recognizes digits drawn in the browser. The interface shows live probabilities for every digit from 0 to 9 and works on desktop and mobile screens.

## Run the application

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start FastAPI:

```bash
python -m uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`.

## Run with Docker

Build the image:

```bash
docker build -t mnist-cloud-devops .
```

Start the container:

```bash
docker run --rm -p 8000:8000 mnist-cloud-devops
```

The Docker image uses CPU-only PyTorch, so the deployment machine does not need an NVIDIA GPU.

## Train the model

The trained checkpoint is included at `artifacts/best_model.pt`. To train it again:

```bash
python train.py
```

MNIST is downloaded into `data/` automatically. Training uses CUDA and saves the checkpoint with the lowest validation loss.

## Run the tests

```bash
python -m pytest -v
```

The tests cover model loading, preprocessing, predictions, and API error responses.
