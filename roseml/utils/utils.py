from PIL import Image
import io
from copy import deepcopy
import json
import shutil
import os
from roseml.storage.gcstorage import GCStorage

def save_image_to_bytes(image: Image, format: str = 'jpeg') -> bytes:
    image = image.convert('RGB')
    buffer = io.BytesIO()
    image.save(fp=buffer, format=format)

    buffer.seek(0)
    return buffer.read()


def save_bytes_to_image(data: bytes) -> Image:
    return Image.open(io.BytesIO(data))



def get_new_shapes(shapes, longest_max_size=1024, smallest_max_size=512, sides_divisible=16):
    shapes = deepcopy(list(shapes))
    print(f'shapes before {shapes}')
    if min(shapes) > smallest_max_size:
        coeff = min(shapes) / smallest_max_size
        shapes[0] = shapes[0] / coeff
        shapes[1] = shapes[1] / coeff
        
    if max(shapes) > longest_max_size:
        coeff = max(shapes) / longest_max_size
        shapes[0] = shapes[0] / coeff
        shapes[1] = shapes[1] / coeff
    
    if shapes[0] % sides_divisible != 0:
        shapes[0] = ((shapes[0] // sides_divisible)+1) * sides_divisible
    
    
    if shapes[1] % sides_divisible != 0:
        shapes[1] = ((shapes[1] // sides_divisible)+1) * sides_divisible

    shapes[0] = int(shapes[0])
    shapes[1] = int(shapes[1])
    print(f'shapes after {shapes}')
    return shapes


def download_gcp_file(gs_uri, local_path):
    if 'SERVICE_ACCOUNT_JSON' in os.environ:
        service_account_info = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])
        service_account_path = 'service_accont_info.json'
        with open(service_account_path, 'w', encoding='utf-8') as f:
            json.dump(service_account_info, f, ensure_ascii=False, indent=4)
        storage = GCStorage(creds=service_account_path)
    else:
        storage = GCStorage()

    storage.download_file(gs_uri=gs_uri, local_filename=local_path)


def upload_gcp_file(gs_uri, local_path):
    if 'SERVICE_ACCOUNT_JSON' in os.environ:
        service_account_info = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])
        service_account_path = 'service_accont_info.json'
        with open(service_account_path, 'w', encoding='utf-8') as f:
            json.dump(service_account_info, f, ensure_ascii=False, indent=4)
        storage = GCStorage(creds=service_account_path)
    else:
        storage = GCStorage()
    storage.upload_file(gs_uri=gs_uri, local_filename=local_path)
