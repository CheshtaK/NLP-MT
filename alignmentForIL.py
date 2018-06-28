def main():
    num = sum(1 for line in open('in.txt', encoding = 'utf-8-sig'))
    
    with open('in.txt', 'r', encoding = 'utf-8-sig') as hindi, open('out.txt', 'r', encoding = 'utf-8-sig') as lang:
        Hlines = [Hline.rstrip('\n') for Hline in hindi]
        Llines = [Lline.rstrip('\n') for Lline in lang]

        sentencesH = []
        sentencesL = []
        lh = []
        ll = []

        for i in range(num):
            sentencesH.append(Hlines[i].split())

        for i in range(num):
            sentencesL.append(Llines[i].split())

        parallel = zip(sentencesH, sentencesL)
        lp = list(parallel)
##        print(lp)

        for i in lp:
            while len(i[0]) != len(i[1]):
                if len(i[0]) < len(i[1]):
                    i[0].append('UNK')
                elif len(i[0]) > len(i[1]):
                    i[1].append('UNK')
                print(i)

        n_sentencesH, n_sentencesL = zip(*lp)

        nh = list(n_sentencesH)
        nl = list(n_sentencesL)

        for sentenceH in nh:
            for h in enumerate(sentenceH):
                lh.append(h)

        for sentenceL in nl:
            for l in enumerate(sentenceL):
                ll.append(l)

        posH = []
        posL = []

        for pos,word in lh:
            posH.append(pos)

        for pos,word in ll:
            posL.append(pos)

        print(posH,'\n')
        print(len(posH),'\n')
        print(posL,'\n')
        print(len(posL),'\n')

        aligned = zip(posH, posL)
        l = list(aligned)

        print(l,'\n')
        print(len(l),'\n')

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
