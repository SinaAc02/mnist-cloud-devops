# MNIST project guide

This project connects a browser drawing canvas to a trained digit classifier,
then packages the application for deployment on an Azure VM.

## Request flow

1. The browser sends the canvas as a PNG to `POST /predict`.
2. FastAPI converts the image to grayscale and crops its nonzero area.
3. Preprocessing fits the digit within 20 x 20 pixels, centers it on a 28 x 28
   background, and applies the MNIST mean and standard deviation.
4. ONNX Runtime runs the exported CNN on the CPU.
5. The API returns the predicted digit and ten probabilities. The browser
   updates the result and probability bars.

`GET /health` returns the service status. Empty drawings, invalid images and
unsupported upload types receive HTTP 400 responses.

## Model and training

`src/model.py` defines three convolution blocks with batch normalization,
max pooling and dropout, followed by a fully connected classifier. PyTorch
training uses CUDA, data augmentation, label smoothing, AdamW and a cosine
learning-rate schedule.

The training set contains 55,000 images, with 5,000 held out for validation.
`train.py` saves the checkpoint with the lowest validation loss, evaluates it
on the MNIST test set and writes a training graph. `export_onnx.py` exports that
checkpoint and validates the ONNX model structure.

| File | Purpose |
| --- | --- |
| `artifacts/best_model.pt` | PyTorch checkpoint for training and export |
| `artifacts/mnist_model.onnx` | Model loaded by the API and Docker image |
| `src/preprocessing.py` | Shared image preparation for API requests |
| `tests/test_app.py` | Model, preprocessing and endpoint tests |

## Container

The Docker image uses Python 3.12, installs the runtime dependencies and starts
Uvicorn on port 8000. Docker Compose binds that port to `127.0.0.1` on the host.
The `APP_IMAGE` variable selects a prebuilt image for deployment; local Compose
runs can build the image from the Dockerfile.

## Infrastructure

Terraform declares an Azure resource group, virtual network, subnet, network
security group, public IP, network interface, SSH public key and Linux VM.
The VM uses Ubuntu 24.04 LTS, the `azureuser` account and an SSH public key passed
through Terraform variables. Network rules permit inbound SSH on port 22 and
HTTP on port 80.

The resource group is configured in Denmark East; the VM and network resources
use Belgium Central. Configuration lives in `terraform/`, with example values
in `terraform/terraform.tfvars.example`.

## CI and deployment

The workflow in `.github/workflows/ci-cd.yml` checks tests, Terraform formatting
and validation, then builds a Docker image. Pull requests run those checks.
Pushes to `main` also run the deployment job after the checks succeed.

Deployment builds and publishes images to
`ghcr.io/sinaac02/mnist-cloud-devops`, tagged with the commit hash and `latest`.
The runner connects to the VM over SSH, updates its checkout, pulls the
commit-tagged image and restarts the Compose service. A health request checks
`http://localhost/health`, then the runner removes its registry login.

The VM needs Docker, Docker Compose and a checkout at `~/mnist-cloud-devops`.
The deployment user needs permission to run Docker. A reverse proxy on the host
must forward HTTP on port 80 to the app at `127.0.0.1:8000`.

The workflow reads `VM_HOST`, `VM_USER`, `VM_SSH_KEY` and `VM_KNOWN_HOSTS` from
GitHub repository secrets. The Terraform configuration provisions infrastructure;
the host software and reverse proxy need separate setup.
