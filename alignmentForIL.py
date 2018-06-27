def main():
    num = sum(1 for line in open('in.txt', encoding = 'utf-8-sig'))
    
    with open('in.txt', 'r', encoding = 'utf-8-sig') as hindi, open('out.txt', 'r', encoding = 'utf-8-sig') as lang:
        Hlines = [Hline.rstrip('\n') for Hline in hindi]
        Llines = [Lline.rstrip('\n') for Lline in lang]

        sentences = []
        lh = []

        for i in range(num):
            sentences.append(Hlines[i].split())

        print(sentences)

        for sentencesH in sentences:
            for h in enumerate(sentencesH):
                lh.append(h)

        print(lh)

        posH = []

        for pos,word in lh:
            posH.append(pos)

        print(posH)

        posL = posH

        print(posL)

        aligned = zip(posH, posL)
        l = list(aligned)

        glist = []
        subl = []

        for tup in l:
            if tup[0] == 0:
                if subl != []:
                    glist.append(subl)
                    subl = []
            subl.append(tup)
        if subl != []:
            glist.append(subl)

        print('Final word alignments: \n')
        for s in glist:
            print(*s)
        print('\n')


        with open('alignment.txt', 'w', encoding = 'utf-8-sig') as align:
            align.write('\n'.join(str(s1) for s1 in glist))
            align.write('\n')


if __name__ == '__main__':
    main()
