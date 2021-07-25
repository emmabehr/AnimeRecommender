import csv

def fetchCSVColumnValues(filename, column = ""):
    values = []
    with open(filename, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if column in row:
                values.append(row[column])
    return values