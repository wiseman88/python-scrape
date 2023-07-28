import os
import requests
from PIL import Image
from io import BytesIO
import traceback


def download_and_optimize_images(image_urls, output_folder, max_width=1000, max_height=1000):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for url in image_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()

            image = Image.open(BytesIO(response.content))
            image.thumbnail((max_width, max_height), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)

            image_filename = os.path.basename(url)
            output_path = os.path.join(output_folder, image_filename)

            if not image_format_is_supported(image):
                print(f"Unsupported image format for {url}.")
                continue

            image.save(output_path, format=image.format)
            print(f"Downloaded and optimized: {url}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}. Request Exception: {e}")
        except IOError as e:
            print(f"Failed to open or save image {url}. IOError: {e}")
        except Exception as e:
            print(f"Unknown error while processing {url}: {e}")
            traceback.print_exc()


def image_format_is_supported(image):
    return image.format in ("JPEG", "PNG", "GIF")
