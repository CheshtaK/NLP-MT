from collections import defaultdict
import sys
import math
import csv

countHindi = defaultdict(lambda: defaultdict(int))
sumCountEnglish = defaultdict(int)
countEnglish = defaultdict(lambda: defaultdict(int))
sumCountHindi = defaultdict(int)

def findTranslationProbability():
    with open('phrases.csv', encoding = 'utf-8-sig') as phrases:
        rows = list(csv.reader(phrases))
        for row in rows:
            countHindi[row[0]][row[1]] += 1
            sumCountEnglish[row[0]] += 1
##            countEnglish[row[1]][row[0]] += 1
##            sumCountHindi[row[1]] += 1
##        print(countHindi, sumCountEnglish)
##        print()
##        print()
##        print(countEnglish, sumCountHindi)


    data = []
    for key in countHindi:
        for key1 in countHindi[key]:
##            print(countHindi[key][key1], sumCountEnglish[key])
            translationProbability = math.log(float(countHindi[key][key1])/sumCountEnglish[key])
            data.append(key1 + '\t' + key + '\t' + str(translationProbability))

    with open('tgs.txt', 'w', encoding = 'utf-8-sig') as f:
        f.write('\n'.join(data))


##    data = []
##    for key in countEnglish:    
##        for key1 in countEnglish[key]:
##            print(countEnglish[key][key1], sumCountHindi[key])
##            translationProbability = math.log(float(countEnglish[key][key1])/sumCountHindi[key])
##            data.append(key1 + '\t' + key + '\t' + str(translationProbability))
##
##    with open('sgt.txt', 'w', encoding = 'utf-8-sig') as f:
##        f.write('\n'.join(data))


def main():
    findTranslationProbability()

if __name__ == "__main__":
    main()


##
##with open('phrases.csv', encoding = 'utf-8-sig') as phrases:
##    rows = list(csv.reader(phrases))
##    for row in rows:
##        print(row[0], row[1])
