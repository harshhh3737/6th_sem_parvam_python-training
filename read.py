import csv
with open('student.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)