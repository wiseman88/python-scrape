from image_processing.csv_parser import CSVParser
from image_processing.image_saver import ImageSaver

file_path = '../data/output.csv'

csv_parser = CSVParser(file_path)
csv_parser.create_images_column('base_image', 'additional_images')

for index, row in csv_parser.csv_rows():
    name, images, folder_to_save_images = CSVParser.process_csv_row(row)

    ImageSaver.save_images_to_folder(name, images, folder_to_save_images)
