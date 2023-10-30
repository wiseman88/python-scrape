import csv


def write_to_csv(csv_file_path, data):
    with open(csv_file_path, "w", encoding="UTF8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data['headers'])

        for row in data['rows']:
            writer.writerow(row)


def create_csv_row(sku, title, description, price, url, main_image, additional_attributes, additional_images):
    return [
        sku, "Default", "simple", "", "svk", title, "short_description",
        description, 2, "Taxable Goods", "Catalog, Search", price, url,
        main_image, main_image, main_image, additional_attributes,
        "99999", "0", "1", "0", "0", "1", "1", "1", "10000", "1",
        "1", "1", "1", "0", "1", "1", "1", "1", "0", "0", "0",
        additional_images
    ]
