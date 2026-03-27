from pathlib import Path
import math
import numpy as np
from PIL import Image


def choose_width(file_size: int) -> int:
    if file_size < 10_000:
        return 32
    if file_size < 30_000:
        return 64
    if file_size < 100_000:
        return 128
    if file_size < 500_000:
        return 256
    if file_size < 1_000_000:
        return 512
    return 1024


def bytes_to_grayscale_image(file_path: str, output_path: str) -> dict:
    path = Path(file_path)
    data = path.read_bytes()

    if not data:
        raise ValueError("File is empty.")

    arr = np.frombuffer(data, dtype=np.uint8)
    width = choose_width(len(arr))
    height = math.ceil(len(arr) / width)

    padded_len = width * height
    if padded_len > len(arr):
        arr = np.pad(arr, (0, padded_len - len(arr)), mode="constant", constant_values=0)

    img_array = arr.reshape((height, width))
    image = Image.fromarray(img_array, mode="L")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)

    return {
        "image_path": str(output),
        "width": width,
        "height": height,
        "file_size_bytes": len(data),
    }
