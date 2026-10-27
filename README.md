# MNIST Digit Classifier

Draw a digit in the browser and see the prediction and probabilities for digits
0-9. The app uses a PyTorch-trained CNN exported to ONNX, with FastAPI and
ONNX Runtime serving predictions on the CPU.

## Run locally

The repository includes the exported model. Create an environment and install
the runtime dependencies:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-runtime.txt
.\.venv\Scripts\python.exe -m uvicorn app:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000), draw a digit and adjust the
brush size as needed. Predictions update as you draw. On other systems, use the
Python executable from your virtual environment.

## Docker

```bash
docker build -t mnist-cloud-devops .
docker run --rm -p 8000:8000 mnist-cloud-devops
```

The image installs `requirements-runtime.txt` and uses
`artifacts/mnist_model.onnx` for CPU inference.

Docker Compose builds the same application and binds it to local port 8000:

```bash
docker compose up --build
```

Stop it with `docker compose down`. Deployment can select a registry image
through the `APP_IMAGE` environment variable.

## Training and export

Install the training dependencies in the same environment, then run:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe train.py
.\.venv\Scripts\python.exe export_onnx.py
```

Training requires CUDA and downloads MNIST to `data/`. It reserves 5,000 of the
60,000 training images for validation and evaluates the chosen checkpoint on
the test set. The lowest validation loss determines the checkpoint saved to
`artifacts/best_model.pt`. Export writes `artifacts/mnist_model.onnx`.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
.\.venv\Scripts\python.exe -m pytest -v
```

Tests exercise the included ONNX model, input preprocessing, the health and
prediction endpoints, and invalid-image responses.

## Deployment

GitHub Actions runs tests, Terraform validation and a Docker build on pushes and
pull requests to `main`. A successful push to `main` also publishes the image to
GitHub Container Registry and updates the Azure VM over SSH. Images receive
`latest` and commit-hash tags; deployment selects the commit-hash tag.

Deployment uses these repository secrets:

| Secret | Value |
| --- | --- |
| `VM_HOST` | VM public IP address |
| `VM_USER` | SSH username, `azureuser` in the Terraform configuration |
| `VM_SSH_KEY` | Private SSH key used by the deployment runner |
| `VM_KNOWN_HOSTS` | Verified SSH host-key entry for the VM |

The deployment health check requests `http://localhost/health` on the VM, so the
host needs a reverse proxy forwarding port 80 to the app on local port 8000.
See the [project guide](ARCHITECTURE.md) for the request
flow, infrastructure and deployment prerequisites.
