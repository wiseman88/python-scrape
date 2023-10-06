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
        # Convert non-ASCII characters to ASCII using unidecode
        name = unidecode(name)
        # Remove special characters, spaces, and convert to lowercase
        slug = re.sub(r'[^a-zA-Z0-9\s]', '', name).strip().lower()
        # Replace spaces with dashes
        slug = re.sub(r'\s+', '-', slug)

        return slug
