from collections import defaultdict
import math
import csv

countHindi = defaultdict(lambda: defaultdict(int))
sumCountEnglish = defaultdict(int)

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
            if (countHindi[key][key1]) == (sumCountEnglish[key]):
                translationProbability = 1.0
                data.append(key1 + '\t' + key + '\t' + str(translationProbability) + '\t' + str(len(key1.split())))
            else:
                translationProbability = math.log(float(countHindi[key][key1])/sumCountEnglish[key])
                data.append(key1 + '\t' + key + '\t' + str(translationProbability) + '\t' + str(len(key1.split())))

    with open('tgs.txt', 'w', encoding = 'utf-8-sig') as f:
        f.write('\n'.join(data))

    for i in range(len(data)):
        print(data[i])

                        
def main():
    findTranslationProbability()


if __name__ == "__main__":
    main()
