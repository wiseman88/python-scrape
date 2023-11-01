import os

from src.scrape.process import Scrape
from src.utils.file_utils import ensure_directory_exists, get_html_files


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(base_dir, '../', 'data')
    ensure_directory_exists(data_folder)

    scraper = Scrape(data_folder)
    scraper.process_all_files()
    scraper.save_to_csv()
    print("CSV file created successfully.")


if __name__ == "__main__":
    main()
