import os

from src.image_processing.image_downloader import ImageDownloader
from src.image_processing.image_optimizer import ImageOptimizer


class ImageSaver:
    @staticmethod
    def save_image(i, url, product_name, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        image = ImageDownloader.download_image(url)

        image = ImageOptimizer.resize_image(image)

        image_filename = ImageOptimizer.slugify_image_name(product_name) + f'-megamix-{i}' + '.jpeg'

        path = os.path.join(output_folder,  image_filename)

        if not ImageOptimizer.check_image_format(image):
            print(f"Unsupported image format for {url}.")

        image.save(path, format=image.format)
        print(f"Downloaded and optimized: {url}")

    @staticmethod
    def save_images_to_folder(name, image_urls, folder_to_save_images):
        for i, url in enumerate(image_urls, start=1):
            try:
                ImageSaver.save_image(i, url, name, folder_to_save_images)
            except Exception as e:
                print(f"Error downloading image {i} for {name}: {str(e)}")
