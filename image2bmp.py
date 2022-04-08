import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import bmp2hex


def image_to_bmp(file_name, size):
    dist_name = f'res/{Path(file_name).stem}.bmp'
    image = Image.open(file_name)

    image = image.resize(size, resample=Image.LANCZOS).convert('1')

    image.save(dist_name, 'bmp')
    return dist_name
