import csv
import re
from bs4 import BeautifulSoup

file_path = "data/index.html"

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

sku = re.findall(r'\d+$', url)
sku = ''.join(sku)

# Description
description = soup.find('div', attrs={'data-box-name': 'Description'})
img_tags = description.find_all('img')
for img_tag in img_tags:
    img_tag.extract()

if description:
    description = description.find_all('div')[4]
    description = description.decode_contents()

else:
    print("Element not found.")

# Price
price = soup.find("meta", attrs={"itemprop": "price"})
price = price.get("content")


# Additional attributes
def generate_additional_attributes(skladom, original_sku, original_url, rating, sold, incoming):
    generated_additional_attributes = f'xxx_skladom={skladom},xxx_original_sku={original_sku},xxx_original_url={original_url},xxx_rating={rating},xxx_sold={sold},xxx_incoming={incoming}'
    return generated_additional_attributes


additional_attributes = generate_additional_attributes(0, sku, url, 4.75, 28, 0)

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
csv_file_path = "data/title.csv"

with open(csv_file_path, "w", encoding="UTF8", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(titles)  # Write header row
    writer.writerow([sku, "Default", "simple", "", "svk", title, "short_description", description, 2, "Taxable Goods",
                     "Catalog, Search", price, url, "", "", "", additional_attributes])

print("CSV file created successfully.")
