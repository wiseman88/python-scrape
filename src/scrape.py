import os
from scrape.product import Product
from utils.file_utils import ensure_directory_exists, get_html_files
from utils.csv_utils import write_to_csv, create_csv_row
from common.constants import TITLES


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(base_dir, 'data')
    ensure_directory_exists(data_folder)

    # Create a CSV file
    csv_file_path = os.path.join(base_dir, 'data', 'output.csv')

    csv_data = {
        'headers': TITLES,
        'rows': []
    }

    for file_name in get_html_files(data_folder):
        file_path = os.path.join(data_folder, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        product = Product(html_content)

        # Extract product details
        title = product.extract_title()
        url = product.extract_url()
        o_sku = product.extract_o_sku()
        sku = product.create_sku()
        description = product.description()
        price = product.price()

        # Additional attributes
        rating = Product.rating()
        sold = Product.sold()
        additional_attributes = Product.generate_additional_attributes(0, o_sku, url, rating, sold, 0)

        # Images
        all_images = product.extract_images()
        main_image = all_images[0]
        additional_images = Product.additional_images(all_images)

        # Write the row to the CSV file
        row = create_csv_row(sku, title, description, price, url, main_image,
                             additional_attributes, additional_images)

        csv_data['rows'].append(row)

    write_to_csv(csv_file_path, csv_data)
    print("CSV file created successfully.")


if __name__ == "__main__":
    main()
