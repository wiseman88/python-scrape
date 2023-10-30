import os.path


def ensure_directory_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_html_files(data_folder):
    return [file for file in os.listdir(data_folder) if file.endswith(".html")]

