import os
import unittest
import pandas as pd
from src.image_processing.csv_parser import CSVParser

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
data_dir = os.path.join(root_dir, 'data', 'input_csv', 'sample.csv')


class TestCSVParser(unittest.TestCase):

    def setUp(self):

        self.file_path = data_dir

        self.parser = CSVParser(self.file_path)

    def tearDown(self):
        pass

    def test_create_images_column(self):
        self.parser.create_images_column('base_image', 'additional_images')
        expected_output = pd.Series(data=['img1.jpg,img2.jpg,img3.jpg', 'img4.jpg,img5.jpg,img6.jpg'], name='images')
        pd.testing.assert_series_equal(self.parser.df['images'], expected_output)

    def test_csv_rows(self):
        rows = list(self.parser.csv_rows())
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1]['sku'], 1)

    def test_process_images_row(self):
        images_str = 'img1.jpg,img2.jpg,img3.jpg'
        expected_output = ['img1.jpg', 'img2.jpg', 'img3.jpg']
        self.assertEqual(CSVParser.process_images_row(images_str), expected_output)

    def test_process_csv_row(self):
        sample_row = pd.Series({'sku': '1', 'name': 'Product 1', 'images': 'img1.jpg,img2.jpg,img3.jpg'})
        expected_output = ('Product 1', ['img1.jpg', 'img2.jpg', 'img3.jpg'], '../data/output_images/1')
        self.assertEqual(CSVParser.process_csv_row(sample_row), expected_output)


if __name__ == '__main__':
    unittest.main()