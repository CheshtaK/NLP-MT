def main():
    num = sum(1 for line in open('in.txt', encoding = 'utf-8-sig'))
    
    with open('in.txt', 'r', encoding = 'utf-8-sig') as hindi, open('out.txt', 'r', encoding = 'utf-8-sig') as lang:
        Hlines = [Hline.rstrip('\n') for Hline in hindi]
        Llines = [Lline.rstrip('\n') for Lline in lang]

        sentencesH = []
        sentencesL = []
        lh = []
        ll = []

##        for i in range(num):
##            sentencesH.append(Hlines[i].split())

        for i in range(num):
            sentencesL.append(Llines[i].split())
            
##        for sentenceH in sentencesH:
##            for h in enumerate(sentenceH):
##                lh.append(h)

        for sentenceL in sentencesL:
            for l in enumerate(sentenceL):
                ll.append(l)

##        print(lh,'\n')
        print(ll,'\n')

        posH = []
        posL = []

##        for pos,word in lh:
##            posH.append(pos)

        for pos,word in ll:
            posL.append(pos)

        posH = posL

##        print(posH,'\n')
##        print(len(posH),'\n')
##        print(posL,'\n')
##        print(len(posL),'\n')

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
