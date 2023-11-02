import unittest
from unittest.mock import patch, Mock
from src.image_processing.image_saver import ImageSaver


class TestImageSaver(unittest.TestCase):

    @patch("os.path.exists", return_value=False)
    @patch("os.makedirs")
    @patch("src.image_processing.image_downloader.ImageDownloader.download_image")
    @patch("src.image_processing.image_optimizer.ImageOptimizer.resize_image")
    @patch("src.image_processing.image_optimizer.ImageOptimizer.slugify_image_name")
    @patch("os.path.join", return_value="mocked/path/to/image")
    @patch("src.image_processing.image_optimizer.ImageOptimizer.check_image_format", return_value=True)
    @patch("builtins.print")
    def test_save_image(self, mock_print, mock_check_format, mock_join, mock_slugify, mock_resize, mock_download, mock_makedirs, mock_exists):

        mock_image = Mock()
        mock_image.format = "JPEG"
        mock_image.save = Mock()

        mock_download.return_value = mock_image
        mock_resize.return_value = mock_image
        mock_slugify.return_value = "scrape-name"

        ImageSaver.save_image(1, "http://example.com/image.jpg", "Product Name", "output_folder")

        mock_makedirs.assert_called_once_with("output_folder")
        mock_download.assert_called_once_with("http://example.com/image.jpg")
        mock_resize.assert_called_once_with(mock_image)
        mock_slugify.assert_called_once_with("Product Name")
        mock_image.save.assert_called_once_with("mocked/path/to/image", format=mock_image.format)
        mock_print.assert_called_once_with("Downloaded and optimized: http://example.com/image.jpg")

    @patch("src.image_processing.image_saver.ImageSaver.save_image")
    @patch("builtins.print")
    def test_save_images_to_folder_success(self, mock_print, mock_save_image):
        mock_save_image.return_value = None

        image_urls = ["http://example.com/1.jpg", "http://example.com/2.jpg"]
        ImageSaver.save_images_to_folder("ProductName", image_urls, "output_folder")

        mock_save_image.assert_called_with(2, "http://example.com/2.jpg", "ProductName", "output_folder")
        mock_print.assert_not_called()

    @patch("src.image_processing.image_saver.ImageSaver.save_image")
    @patch("builtins.print")
    def test_save_images_to_folder_failure(self, mock_print, mock_save_image):
        mock_save_image.side_effect = Exception("Some error")

        image_urls = ["http://example.com/1.jpg"]
        ImageSaver.save_images_to_folder("ProductName", image_urls, "output_folder")

        mock_save_image.assert_called_once_with(1, "http://example.com/1.jpg", "ProductName", "output_folder")
        mock_print.assert_called_once_with("Error downloading image 1 for ProductName: Some error")


if __name__ == "__main__":
    unittest.main()
