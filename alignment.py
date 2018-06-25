from collections import defaultdict
import copy
import itertools
import operator
from functools import reduce
import pickle
import csv
import json

'''Method to implement the EM Algorithm to obtain word alignment'''

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

    print('Enumerated sentences: \n')
    print('English \n')
    print(le, '\n')
    print('Hindi \n')
    print(lh, '\n')
        
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

    '''Finding the maximum probable alignment'''
    
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

    print('Translations: \n')                
    print(trans, '\n')

    posR = []
    wordR = []
    htrans = []
    
    for pos,word in le:
        if word in trans:
            posR.append(pos)
            wordR.append(word)
            htrans.append(trans[word])

    print('English word positions: \n')
    print(posR, '\n')
    print('English words: \n')
    print(wordR, '\n')
    print('Translated Hindi words: \n')
    print(htrans, '\n')

    hpos = []

    for h in htrans:
        for pos, word in lh:
            if (h == word):
                hpos.append(pos)
                break


    print('Hindi word positions: \n')
    print(hpos, '\n')


    '''Merging the two positions(English and Hindi) to get alignment for each word'''

    aligned = zip(posR, hpos)
    l = list(aligned)


    '''Forming sublists for individual sentences'''
    
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


    '''Writing the alignments in a text file'''

    with open('alignment.txt', 'w', encoding = 'utf-8-sig') as align:
        align.write('\n'.join(str(s1) for s1 in glist))


    print('Alignments and their corresponding probabilities: \n')
    return conditional_probs


def main():

    '''Reading the parallel corpus from two files'''
    
    sentences = []
    num = sum(1 for line in open('in.txt'))

    with open('in.txt', 'r', encoding = 'utf-8-sig') as english, open('out.txt', 'r', encoding = 'utf-8-sig') as hindi:
        Elines = [Eline.rstrip('\n') for Eline in english]
        Hlines = [Hline.rstrip('\n') for Hline in hindi]
        for i in range(num):
            sentences.append((Elines[i].split(), Hlines[i].split()))

    '''Aligning'''

    print (em_run(sentences))
    

if __name__ == '__main__':
    main()
