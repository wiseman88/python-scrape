import unittest
from unittest.mock import patch, Mock
from PIL import Image
from io import BytesIO
import requests
from src.image_processing.image_downloader import ImageDownloader


class TestImageDownloader(unittest.TestCase):
    @patch('requests.get')
    @patch('PIL.Image.open')
    def test_download_image_successful(self, mock_image_open, mock_requests_get):

        image_url = 'http://example.com/image.jpg'
        image_content = b'Mock image content'
        mock_response = Mock()
        mock_response.content = image_content
        mock_requests_get.return_value = mock_response
        mock_image = Mock()
        mock_image_open.return_value = mock_image

        downloaded_image = ImageDownloader.download_image(image_url)

        mock_requests_get.assert_called_once_with(image_url)
        mock_response.raise_for_status.assert_called_once()
        mock_image_open.assert_called_once()
        # Ensure that Image.open was called with a BytesIO object
        args, _ = mock_image_open.call_args
        self.assertIsInstance(args[0], BytesIO)
        self.assertEqual(downloaded_image, mock_image)

    @patch('requests.get')
    def test_download_image_request_exception(self, mock_requests_get):

        image_url = 'http://example.com/image.jpg'
        mock_requests_get.side_effect = requests.exceptions.RequestException('Request Exception')

        downloaded_image = ImageDownloader.download_image(image_url)

        self.assertIsNone(downloaded_image)
        mock_requests_get.assert_called_once_with(image_url)

    @patch('requests.get')
    @patch('traceback.print_exc')
    def test_download_image_unknown_error(self, mock_traceback_print_exc, mock_requests_get):

        image_url = 'http://example.com/image.jpg'
        mock_requests_get.side_effect = Exception('Unknown Error')

        downloaded_image = ImageDownloader.download_image(image_url)

        self.assertIsNone(downloaded_image)
        mock_requests_get.assert_called_once_with(image_url)
        mock_traceback_print_exc.assert_called_once()


if __name__ == '__main__':
    unittest.main()
