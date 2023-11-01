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

            row = create_csv_row(
                product_data["sku"],
                product_data["title"],
                product_data["description"],
                product_data["price"],
                product_data["url"],
                product_data["main_image"],
                product_data["additional_attributes"],
                product_data["additional_images"]
            )
            self.csv_data['rows'].append(row)

    @staticmethod
    def process_product_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        product = Product(html_content)

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
