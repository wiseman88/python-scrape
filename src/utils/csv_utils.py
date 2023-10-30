import csv


def write_to_csv(csv_file_path, data):
    with open(csv_file_path, "w", encoding="UTF8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data['headers'])

        for row in data['rows']:
            writer.writerow(row)
