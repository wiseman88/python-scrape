import re

from PIL import Image
from unidecode import unidecode


class ImageOptimizer:
    @staticmethod
    def resize_image(image, max_width=1000, max_height=1000):
        image.thumbnail((max_width, max_height), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
        return image

    @staticmethod
    def check_image_format(image):
        return image.format in ("JPEG", "PNG", "GIF")

    @staticmethod
    def slugify_image_name(name):
        name = unidecode(name)
        slug = re.sub(r'\W+', '-', name).strip().lower()
        return slug
