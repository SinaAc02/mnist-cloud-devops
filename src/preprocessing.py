"""Prepare a canvas image for the MNIST model."""

import numpy as np
from PIL import Image


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

    model_input = np.asarray(mnist_image, dtype=np.float32) / 255.0
    model_input = (model_input - 0.1307) / 0.3081
    model_input = model_input[np.newaxis, np.newaxis, :, :]
    return model_input, mnist_image
