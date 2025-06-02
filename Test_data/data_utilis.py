import os
import csv


class DataReader:
    @staticmethod
    def get_csv_data(filename):
        # Ścieżka do katalogu, gdzie znajduje się ten skrypt
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, filename)

        rows = []
        with open(file_path, 'r') as data_file:
            reader = csv.reader(data_file)
            next(reader, None)
            for row in reader:
                rows.append(row)
        return rows
