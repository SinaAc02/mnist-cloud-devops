"""Train the CNN on MNIST."""

from pathlib import Path

import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms

from src.model import EnhancedCNN, count_parameters


EPOCHS = 20
BATCH_SIZE = 512
LEARNING_RATE = 0.001


def create_loaders():
    train_transform = transforms.Compose(
        [
            transforms.RandomAffine(12, translate=(0.1, 0.1), scale=(0.9, 1.1)),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,)),
        ]
    )
    normal_transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )

    training_images = datasets.MNIST("data", train=True, download=True, transform=train_transform)
    validation_images = datasets.MNIST(
        "data", train=True, download=True, transform=normal_transform
    )
    test_images = datasets.MNIST("data", train=False, download=True, transform=normal_transform)

    generator = torch.Generator().manual_seed(42)
    indices = torch.randperm(60_000, generator=generator)
    validation_indices = indices[:5_000]
    training_indices = indices[5_000:]

    training_loader = DataLoader(
        Subset(training_images, training_indices), batch_size=BATCH_SIZE, shuffle=True,num_workers=3
    )
    validation_loader = DataLoader(
        Subset(validation_images, validation_indices), batch_size=BATCH_SIZE,num_workers=3
    )
    test_loader = DataLoader(test_images, batch_size=BATCH_SIZE,num_workers=3)
    return training_loader, validation_loader, test_loader


def train_one_epoch(model, loader, loss_function, optimizer, device):
    model.train()
    correct = 0
    total = 0

    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        predictions = model(images)
        loss = loss_function(predictions, labels)
        loss.backward()
        optimizer.step()

        correct += (predictions.argmax(1) == labels).sum().item()
        total += labels.size(0)

    return correct / total


def evaluate(model, loader, loss_function, device):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            predictions = model(images)
            loss = loss_function(predictions, labels)

            total_loss += loss.item() * labels.size(0)
            correct += (predictions.argmax(1) == labels).sum().item()
            total += labels.size(0)

    return total_loss / total, correct / total


def save_graph(training_accuracy, validation_accuracy):
    epochs = range(1, len(training_accuracy) + 1)
    plt.plot(epochs, training_accuracy, label="Training")
    plt.plot(epochs, validation_accuracy, label="Validation")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig("artifacts/training_graph.png")
    plt.close()


def train_model():
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available")

    device = torch.device("cuda")
    training_loader, validation_loader, test_loader = create_loaders()
    model = EnhancedCNN().to(device)
    loss_function = nn.CrossEntropyLoss(label_smoothing=0.05)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)

    Path("artifacts").mkdir(exist_ok=True)
    model_path = Path("artifacts/best_model.pt")
    best_validation_loss = float("inf")
    training_accuracy = []
    validation_accuracy = []

    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(model)
    print(f"Trainable parameters: {count_parameters(model):,}")

    for epoch in range(EPOCHS):
        train_accuracy = train_one_epoch(
            model, training_loader, loss_function, optimizer, device
        )
        validation_loss, validation_acc = evaluate(
            model, validation_loader, loss_function, device
        )
        scheduler.step()

        training_accuracy.append(train_accuracy)
        validation_accuracy.append(validation_acc)

        print(
            f"Epoch {epoch + 1:02d}/{EPOCHS} - "
            f"training: {train_accuracy:.2%} - validation: {validation_acc:.2%}"
        )

        if validation_loss < best_validation_loss:
            best_validation_loss = validation_loss
            torch.save({"model_state_dict": model.state_dict()}, model_path)

    checkpoint = torch.load(model_path, weights_only=True)
    model.load_state_dict(checkpoint["model_state_dict"])
    _, test_accuracy = evaluate(model, test_loader, loss_function, device)
    save_graph(training_accuracy, validation_accuracy)

    print(f"Test accuracy: {test_accuracy:.2%}")
    print(f"Saved model: {model_path.resolve()}")


if __name__ == "__main__":
    train_model()
