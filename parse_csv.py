import csv

def parse_csv(path='./data.csv'):
    data = []

    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data.append(tuple(row))
    return data
