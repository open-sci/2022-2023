import csv

def detect_delimiter(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        dialect = csv.Sniffer().sniff(file.read(1024))
    return dialect.delimiter
