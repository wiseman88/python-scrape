import os

from src.common.constants import TITLES
from src.scrape.product import Product
from src.utils.csv_utils import write_to_csv, create_csv_row
from src.utils.file_utils import get_html_files


class Scrape:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.csv_data = {'headers': TITLES, 'rows': []}

    def process_all_files(self):
        for file_name in get_html_files(self.data_folder):
            file_path = os.path.join(self.data_folder, file_name)
            product_data = self.process_product_file(file_path)

            # Create row and fill each column with data extracted from each product .html file
            row = create_csv_row(**product_data)
            self.csv_data['rows'].append(row)

    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except IOError as e:
            raise IOError(f"Error reading {file_path}: {e}")

    def process_product_file(self, file_path):
        product = Product(self.read_file(file_path))

        return {
            "sku": product.create_sku(),
            "title": product.extract_title(),
            "description": product.description(),
            "price": product.price(),
            "url": product.extract_url(),
            "main_image": product.extract_images()[0],
            "additional_attributes": Product.generate_additional_attributes(
                0, product.extract_o_sku(), product.extract_url(),
                Product.rating(), Product.sold(), 0
            ),
            "additional_images": Product.additional_images(product.extract_images())
        }

    def save_to_csv(self):
        csv_file_path = os.path.join(self.data_folder, 'output.csv')
        write_to_csv(csv_file_path, self.csv_data)
