"""Prepare a canvas image for the MNIST model."""

from PIL import Image
from torchvision import transforms


normalize = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ]
)


def preprocess_image(image: Image.Image):
    image = image.convert("L")
    box = image.getbbox()

    if box is None:
        raise ValueError("The canvas is empty")

    digit = image.crop(box)
    digit.thumbnail((20, 20), Image.Resampling.LANCZOS)

    mnist_image = Image.new("L", (28, 28), color=0)
    left = (28 - digit.width) // 2
    top = (28 - digit.height) // 2
    mnist_image.paste(digit, (left, top))

    tensor = normalize(mnist_image).unsqueeze(0)
    return tensor, mnist_image
