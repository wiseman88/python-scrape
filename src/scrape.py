import os
import csv
from bs4 import BeautifulSoup
from scrape.product import Product

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(BASE_DIR, 'data')

# CSV titles
titles = [
    "sku", "attribute_set_code", "product_type", "categories", "product_websites",
    "name", "short_description", "description", "product_online", "tax_class_name",
    "visibility", "price", "url_key", "base_image", "small_image", "thumbnail_image",
    "additional_attributes", "qty", "out_of_stock_qty", "use_config_min_qty",
    "is_qty_decimal", "allow_backorders", "use_config_backorders", "min_cart_qty",
    "use_config_min_sale_qty", "max_cart_qty", "use_config_max_sale_qty",
    "is_in_stock", "notify_on_stock_below", "use_config_notify_stock_qty",
    "manage_stock", "use_config_manage_stock", "use_config_qty_increments",
    "qty_increments", "use_config_enable_qty_inc", "enable_qty_increments",
    "is_decimal_divided", "website_id", "additional_images"
]

# Create a CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(BASE_DIR, 'data', 'output.csv')

with open(csv_file_path, "w", encoding="UTF8", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(titles)  # Write header row

    # Get a list of all HTML files in the data folder
    html_files = [file for file in os.listdir(data_folder) if file.endswith(".html")]

    for file_name in html_files:
        file_path = os.path.join(data_folder, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")
        product = Product(html_content)

        # Name
        title = product.extract_title()

        # URL
        url = product.extract_url()

        # SKU
        o_sku = product.extract_o_sku()
        sku = product.create_sku()

        # Description
        img_tags = product.extract_img_tags()
        description = product.description()

        # Price
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
        writer.writerow(
            [sku, "Default", "simple", "", "svk", title, "short_description", description, 2, "Taxable Goods",
             "Catalog, Search", price, url, main_image, main_image, main_image, additional_attributes, "99999", "0",
             "1", "0", "0", "1", "1", "1", "10000", "1", "1", "1", "1", "0", "1", "1", "1", "1", "0", "0", "0",
             additional_images])

print("CSV file created successfully.")
