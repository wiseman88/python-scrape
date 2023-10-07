import os

from image_processing.image_downloader import ImageDownloader
from image_processing.image_optimizer import ImageOptimizer


class ImageSaver:
    @staticmethod
    def save_image(i, url, product_name, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        image = ImageDownloader.download_image(url)

        image = ImageOptimizer.resize_image(image)

        image_filename = ImageOptimizer.slugify_image_name(product_name) + f'-megamix-{i}'

        path = os.path.join(output_folder,  image_filename)

        if not ImageOptimizer.check_image_format(image):
            print(f"Unsupported image format for {url}.")

        image.save(path, format=image.format)
        print(f"Downloaded and optimized: {url}")

