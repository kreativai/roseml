from PIL import Image
import io

def save_image_to_bytes(image: Image, format: str = 'jpeg') -> bytes:
    image = image.convert('RGB')
    buffer = io.BytesIO()
    image.save(fp=buffer, format=format)

    buffer.seek(0)
    return buffer.read()


def save_bytes_to_image(data: bytes) -> Image:
    return Image.open(io.BytesIO(data))
