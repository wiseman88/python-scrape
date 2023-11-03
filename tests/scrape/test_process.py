import unittest
from unittest.mock import patch, mock_open
from src.scrape.process import Scrape


class TestScrape(unittest.TestCase):

    def test_read_file_success(self):
        mock_content = 'Hello, world!'
        with patch('builtins.open', mock_open(read_data=mock_content), create=True):
            result = Scrape.read_file('dummy_path.html')
            self.assertEqual(result, mock_content)

    def test_read_file_unicode(self):
        mock_content = 'Hello, ŵorld!'
        with patch('builtins.open', mock_open(read_data=mock_content), create=True):
            result = Scrape.read_file('dummy_path.html')
            self.assertEqual(result, mock_content)

    def test_read_file_not_found(self):
        with self.assertRaises(IOError):
            Scrape.read_file('non_existent_file.html')

    @patch('builtins.open', new_callable=mock_open)
    def test_read_file_io_error(self, mock_file):
        mock_file.side_effect = IOError("Some I/O error")
        with self.assertRaises(IOError) as cm:
            Scrape.read_file('faulty_path.html')
        self.assertIn('Error reading faulty_path.html', str(cm.exception))


if __name__ == '__main__':
    unittest.main()
