from collections import defaultdict
import copy
import itertools
import operator
from functools import reduce
import pickle
import csv

def em_run(sentence_pairs):

    source_sentences, target_sentences = list(zip(*sentence_pairs))
    
    le = []
    lh = []

    for sentencesE in source_sentences:
        for e in enumerate(sentencesE):
            le.append(e)
    
    for sentencesH in target_sentences:
        for h in enumerate(sentencesH):
            lh.append(h)

    print(le)
    print(lh)
    print ()
    print()
        
    source_vocabulary = set(itertools.chain.from_iterable(source_sentences))
    target_vocabulary = set(itertools.chain.from_iterable(target_sentences))

    uniform_prob = 1.0 / len(source_vocabulary)

    conditional_probs_old = None
    conditional_probs = {(source_w, target_w): uniform_prob
                         for source_w in source_vocabulary
                         for target_w in target_vocabulary}

    alignments = [[list(zip(source, target_perm))
                   for target_perm in itertools.permutations(target)]
                  for source, target in sentence_pairs]
    

    i = 0
    while conditional_probs_old != conditional_probs:
        conditional_probs_old = copy.copy(conditional_probs)

        alignment_probs = {
            i: {
                tuple(alignment):
                reduce(operator.mul, [conditional_probs[pair]
                                      for pair in alignment])
                for alignment in sentence_alignments
            }

            for i, sentence_alignments in enumerate(alignments)
        }

        for sentence_idx, sentence_alignments in alignment_probs.items():
            total = float(sum(sentence_alignments.values()))
            probs = {alignment: value / total
                     for alignment, value in sentence_alignments.items()}
            alignment_probs[sentence_idx] = probs


        word_translations = defaultdict(lambda: defaultdict(float))
        for sentence_alignments in alignment_probs.values():
            for word_pairs, prob in sentence_alignments.items():
                for source_word, target_word in word_pairs:
                    word_translations[target_word][source_word] += prob

        conditional_probs = {}
        for target_word, translations in word_translations.items():
            total = float(sum(translations.values()))
            for source_word, score in translations.items():
                conditional_probs[source_word, target_word] = score / total

    wordP = []
    trans = {}
    
    for source in source_vocabulary:
        wordP = []
        for target in target_vocabulary:
            if (source, target) in conditional_probs:
                wordP.append(conditional_probs[source, target])
        maxP = max(wordP)
        for target in target_vocabulary:
            if (source, target) in conditional_probs:
                if(conditional_probs[source, target] == maxP):
                    trans.update({source : target})
                    
    print(trans)
    print()
    print()


    posR = []
    wordR = []
    htrans = []
    
    for pos,word in le:
        if word in trans:
            posR.append(pos)
            wordR.append(word)
            htrans.append(trans[word])

    print()
    print()
    print(posR)
    print()
    print(wordR)
    print()
    print(htrans)

    hpos = []

    for h in htrans:
        for pos, word in lh:
            if (h == word):
                hpos.append(pos)
                break


    print()
    print(hpos)


    print()
    print()
    aligned = zip(posR, hpos)
    l = list(aligned)
    print(l)

    index = []

##    x = [i[0] for i in l]
##    for s in x:
##        if(s == 0):
##            index.append(x.index(s))
##            print('break')
##
##    print(index)


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

##    for s in glist:
##        print(*s)

    
    with open('alignment.csv', 'w') as f:
        wr = csv.writer(f)
        wr.writerows(glist)
            

    
##    print([x for x in [list(group) for key, group in itertools.groupby(l, key = lambda k: k[1] == 0)]
##          if x[0][1] != 0])

##    SplitList = []
##
##    for i, tup in enumerate(l):
##        if i != len(l)-1:
##            if i == 0:
##                tmp = []
##            if tup[0] == 0:
##                tmp.append(tup)
##                if tmp:
##                    SplitList.append(tmp)
##                    tmp = []
##        else:
##            tmp.append(tup)
##            
##    print(SplitList)

    #if ((i[0] for i in l):
     #   print ('break')



##    with open('alignment.txt', 'wb') as align:
##        pickle.dump(l, align)
    
    print()
    print()
    return conditional_probs


def main():

    Elines = [Eline.rstrip('\n') for Eline in open('in.txt')]

    with open('out.txt', 'r', encoding = 'utf-8') as hindi:
        Hlines = [Hline.rstrip('\n') for Hline in hindi]
        
    SENTENCES = [(Elines[0].split(), Hlines[0].split()),
                 (Elines[1].split(), Hlines[1].split()),
                 (Elines[2].split(), Hlines[2].split())]

    print (em_run(SENTENCES))

if __name__ == '__main__':
    main()
