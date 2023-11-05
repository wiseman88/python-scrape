import pandas as pd


class CSVParser:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def create_images_column(self, base_image_col, additional_images_col):
        self.df['images'] = self.df[base_image_col] + ',' + self.df[additional_images_col]
        return self.df['images']

    def csv_rows(self):
        rows = self.df.iterrows()
        return rows

    @staticmethod
    def get_product_image_urls(images_str):
        return [item.strip() for item in images_str.strip('[]').split(',')]

    @staticmethod
    def process_csv_row(row):
        sku = row['sku']
        name = row['name']
        images = CSVParser.get_product_image_urls(row['images'])

        folder_to_save_images = f"../data/output_images/{sku}"
        return name, images, folder_to_save_images
