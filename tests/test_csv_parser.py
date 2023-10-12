import unittest
import pandas as pd
from src.image_processing.csv_parser import CSVParser


class TestCSVParser(unittest.TestCase):

    def setUp(self):

        self.file_path = "../data/input_csv/sample.csv"

        self.parser = CSVParser(self.file_path)

    def tearDown(self):
        pass

    def test_create_images_column(self):
        self.parser.create_images_column('base_image', 'additional_images')
        expected_output = pd.Series(data=['img1.jpg,img2.jpg,img3.jpg', 'img4.jpg,img5.jpg,img6.jpg'], name='images')
        pd.testing.assert_series_equal(self.parser.df['images'], expected_output)


if __name__ == '__main__':
    unittest.main()