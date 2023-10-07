import pandas as pd


class CSVParser:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def get_images_url(self, base_image_col, additional_images_col):
        self.df['images'] = self.df[base_image_col] + ',' + self.df[additional_images_col]