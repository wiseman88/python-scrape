import os
import csv
import random
import re
from bs4 import BeautifulSoup

from image_downloader import download_and_optimize_images

data_folder = "data"  # Update this to the path of your data folder

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
csv_file_path = "data/output.csv"

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

        # Name
        meta_tag = soup.find("meta", attrs={"property": "og:title"})
        title = meta_tag.get("content") if meta_tag else "No title found."

        # URL
        url = soup.select_one('link[rel="canonical"]')
        url = url.get("data-savepage-href") if url else "No url found."

        # SKU
        o_sku = re.findall(r'\d+$', url)
        o_sku = ''.join(o_sku)
        sku = '21' + o_sku

        # Description
        html = soup.find('div', attrs={'data-box-name': 'Description'})
        img_tags = html.find_all('img')

        if html:
            desc = html.find_all('div', class_='mgn2_16 _0d3bd_am0a-')
            description = ''
            for div in desc:
                div_content = ''.join(map(str, div.contents))
                description += div_content
        else:
            print("Element not found.")

        # Price
        price = soup.find("meta", attrs={"itemprop": "price"})
        price = price.get("content")
        price = float(price)
        price = price / 2
        price = round(price * 20) / 20

        # Additional attributes
        def generate_additional_attributes(skladom, original_sku, original_url, rating, sold, incoming):
            generated_additional_attributes = f'xxx_skladom={skladom},xxx_original_sku={original_sku},xxx_original_url={original_url},xxx_rating={rating},xxx_sold={sold},xxx_incoming={incoming}'
            return generated_additional_attributes


        rating = round(random.uniform(4.65, 4.99), 2)
        sold = round(random.uniform(10, 200))

        additional_attributes = generate_additional_attributes(0, o_sku, url, rating, sold, 0)

        # Images
        images = [tag['data-savepage-src'] for tag in img_tags]
        main_image = images[0]
        additional_images = images[1:] if len(images) > 1 else None
        additional_images = ",".join(additional_images)

        if __name__ == "__main__":

            output_folder = f"output_images/{sku}"
            download_and_optimize_images(images, output_folder)

        # Write the row to the CSV file
        writer.writerow([sku, "Default", "simple", "", "svk", title, "short_description", description, 2, "Taxable Goods",
                         "Catalog, Search", price, url, main_image, main_image, main_image, additional_attributes, "99999", "0", "1", "0", "0", "1", "1", "1", "10000", "1", "1", "1", "1", "0", "1", "1", "1", "1", "0", "0", "0", additional_images])

print("CSV file created successfully.")