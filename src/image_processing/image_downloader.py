import requests
from PIL import Image
import traceback
from io import BytesIO


class ImageDownloader:
    @staticmethod
    def download_image(image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            return Image.open(BytesIO(response.content))

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {image_url}. Request Exception: {e}")
        except IOError as e:
            print(f"Failed to open or save image {image_url}. IOError: {e}")
        except Exception as e:
            print(f"Unknown error while processing {image_url}: {e}")
            traceback.print_exc()
