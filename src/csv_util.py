import csv

DEFAULT_TEXT_ENCODING = "utf8"

def fetchCSVColumnValues(filename, column = "", encoding=DEFAULT_TEXT_ENCODING):
    values = []
    with open(filename,  "r", encoding=encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if column in row:
                values.append(row[column])
    return values

def saveListToCSVFile(filename, data, columns = []):
    with open(filename, "w+", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        if len(columns) > 0:
            csv_writer.writerow(columns)
        for row in data:
            csv_writer.writerow([row])

def readCSVFile(filename, encoding=DEFAULT_TEXT_ENCODING):
    contents = []
    try:
        with open(filename, "r", encoding=encoding) as csv_file:
            content = csv.DictReader(csv_file)
            for row in content:
                contents.append(row)

        return contents
    except:
        print(f"failed to read file {filename}")
        return contents

   

def writeCSVFile(filename, data, columns=[]):
    with open(filename, "w+", newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=columns)
        csv_writer.writeheader()
        csv_writer.writerows(data)