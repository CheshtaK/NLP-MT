from collections import defaultdict
import sys
import math
import csv

countHindi = defaultdict(lambda: defaultdict(int))
sumCountEnglish = defaultdict(int)
countEnglish = defaultdict(lambda: defaultdict(int))
sumCountHindi = defaultdict(int)

'''Method to find Translation Probability'''

def findTranslationProbability():
    with open('phrases.csv', encoding = 'utf-8-sig') as phrases:
        rows = list(csv.reader(phrases))
        for row in rows:
            countHindi[row[0]][row[1]] += 1
            sumCountEnglish[row[0]] += 1
            
    data = []
    for key in countHindi:
        for key1 in countHindi[key]:
            translationProbability = math.log(float(countHindi[key][key1])/sumCountEnglish[key])
            data.append(key1 + '\t' + key + '\t' + str(translationProbability))

    with open('tgs.txt', 'w', encoding = 'utf-8-sig') as f:
        f.write('\n'.join(data))


def main():
    findTranslationProbability()


if __name__ == "__main__":
    main()
