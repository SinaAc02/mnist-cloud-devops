"""Export the trained PyTorch model to ONNX."""

from pathlib import Path

import onnx
import torch

from src.model import EnhancedCNN


checkpoint_path = Path("artifacts/best_model.pt")
onnx_path = Path("artifacts/mnist_model.onnx")

model = EnhancedCNN()
checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

example_image = torch.zeros(1, 1, 28, 28)

torch.onnx.export(
    model,
    example_image,
    onnx_path,
    input_names=["image"],
    output_names=["scores"],
    opset_version=18,
    dynamo=False,
)

onnx.checker.check_model(onnx.load(onnx_path))
print(f"Saved ONNX model: {onnx_path.resolve()}")
