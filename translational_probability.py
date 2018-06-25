import csv

with open('phrases.csv', encoding = 'utf-8-sig') as phrases:
    rows = list(csv.reader(phrases))
    print (rows[0][0])
