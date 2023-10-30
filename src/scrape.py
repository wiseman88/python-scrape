import os
from scrape.product import Product
from utils.file_utils import ensure_directory_exists, get_html_files
from utils.csv_utils import write_to_csv


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(base_dir, 'data')
    ensure_directory_exists(data_folder)

    # Create a CSV file
    csv_file_path = os.path.join(base_dir, 'data', 'output.csv')

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

    csv_data = {
        'headers': titles,
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
        img_tags = product.extract_img_tags()
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
        row = [
            sku, "Default", "simple", "", "svk", title, "short_description",
            description, 2, "Taxable Goods", "Catalog, Search", price, url,
            main_image, main_image, main_image, additional_attributes,
            "99999", "0", "1", "0", "0", "1", "1", "1", "10000", "1",
            "1", "1", "1", "0", "1", "1", "1", "1", "0", "0", "0",
            additional_images
        ]

        csv_data['rows'].append(row)

    write_to_csv(csv_file_path, csv_data)
    print("CSV file created successfully.")


if __name__ == "__main__":
    main()
