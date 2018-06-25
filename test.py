import ast

with open('in.txt', encoding = 'utf-8') as e, open('out.txt', encoding = 'utf-8') as h, open('alignment.txt', encoding = 'utf-8') as align:
    for english, hindi, alignment in zip(e, h, align):
        english = english.strip()
        hindi = hindi.strip()
        alignment = alignment.strip()
        alignment = list(ast.literal_eval(alignment))
        b = [i for i,_ in alignment]
        print(b)


##Elines = [Eline.rstrip('\n') for Eline in open('in.txt')]
##
##with open('out.txt', 'r', encoding = 'utf-8') as hindi:
##        Hlines = [Hline.rstrip('\n') for Hline in hindi]
##
##with open('in.txt', 'r') as f:
##    for i in f:


sentences = []
num = sum(1 for line in open('in.txt'))
print(num)

with open('in.txt', 'r', encoding = 'utf-8') as english, open('out.txt', 'r', encoding = 'utf-8') as hindi:
    Elines = [Eline.rstrip('\n') for Eline in english]
    Hlines = [Hline.rstrip('\n') for Hline in hindi]
    for i in range(num):
        sentences.append((Elines[i].split(), Hlines[i].split()))
    print(sentences)
