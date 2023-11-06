import unittest
from io import BytesIO

from PIL import Image
from src.image_processing.image_optimizer import ImageOptimizer


class TestImageOptimizer(unittest.TestCase):
    def test_resize_image_successfully(self):
        test_image = Image.new('RGB', (1500, 1600))

        resized_image = ImageOptimizer.resize_image(test_image, max_width=1000, max_height=1000)

        self.assertLessEqual(resized_image.width, 1000)
        self.assertLessEqual(resized_image.height, 1000)

    def test_jpeg_format(self):
        image_data = BytesIO()
        Image.new("RGB", (100, 100)).save(image_data, format="JPEG")
        image_data.seek(0)

        image = Image.open(image_data)
        self.assertTrue(ImageOptimizer.check_image_format(image))

    def test_slugify_image_name(self):
        test_product_name = "Bottle of * John Jay * Keeshan"
        expected_output = "bottle-of-john-jay-keeshan"
        self.assertEqual(ImageOptimizer.slugify_image_name(test_product_name), expected_output)


if __name__ == '__main__':
    unittest.main()
