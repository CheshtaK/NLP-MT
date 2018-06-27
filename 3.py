from __future__ import division
from collections import defaultdict
from math import factorial
from nltk.translate import AlignedSent
from nltk.translate import Alignment
from nltk.translate import IBMModel
from nltk.translate import IBMModel2
from nltk.translate.ibm_model import Counts
import warnings

class IBMModel3(IBMModel):
    def __init__(self, sentence_aligned_corpus, iterations,probability_tables=None):
        super(IBMModel3, self).__init__(sentence_aligned_corpus)
        self.reset_probabilities()

        if probability_tables is None:
            ibm2 = IBMModel2(sentence_aligned_corpus, iterations)
            self.translation_table = ibm2.translation_table
            self.alignment_table = ibm2.alignment_table
            self.set_uniform_probabilities(sentence_aligned_corpus)
        else:
            self.translation_table = probability_tables['translation_table']
            self.alignment_table = probability_tables['alignment_table']
            self.fertility_table = probability_tables['fertility_table']
            self.p1 = probability_tables['p1']
            self.distortion_table = probability_tables['distortion_table']

        for n in range(0, iterations):
            self.train(sentence_aligned_corpus)

    def reset_probabilities(self):
        super(IBMModel3, self).reset_probabilities()
        self.distortion_table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: self.MIN_PROB))))

    def set_uniform_probabilities(self, sentence_aligned_corpus):
        l_m_combinations = set()
        for aligned_sentence in sentence_aligned_corpus:
            l = len(aligned_sentence.mots)
            m = len(aligned_sentence.words)
            if (l, m) not in l_m_combinations:
                l_m_combinations.add((l, m))

                if m != 0:
                    initial_prob = 1 / m
                if initial_prob < IBMModel.MIN_PROB:
                    warnings.warn("A target sentence is too long (" + str(m) +
                                  " words). Results may be less accurate.")
                for j in range(1, m+1):
                    for i in range(0, l+1):
                        self.distortion_table[j][i][l][m] = initial_prob

        self.fertility_table[0] = defaultdict(lambda: 0.2)
        self.fertility_table[1] = defaultdict(lambda: 0.65)
        self.fertility_table[2] = defaultdict(lambda: 0.1)
        self.fertility_table[3] = defaultdict(lambda: 0.04)
        MAX_FERTILITY = 10
        initial_fert_prob = 0.01 / (MAX_FERTILITY - 4)
        for phi in range(4, MAX_FERTILITY):
             self.fertility_table[phi] = defaultdict(lambda: initial_fert_prob)

        self.p1 = 0.5

    def train(self, parallel_corpus):
        counts = Model3Counts()
        for aligned_sentence in parallel_corpus:
            l = len(aligned_sentence.mots)
            m = len(aligned_sentence.words)

            sampled_alignments, best_alignment = self.sample(aligned_sentence)
            aligned_sentence.alignment = Alignment(best_alignment.zero_indexed_alignment())
            total_count = self.prob_of_alignments(sampled_alignments)

            for alignment_info in sampled_alignments:
                count = self.prob_t_a_given_s(alignment_info)
                normalized_count = count / total_count
            
                for j in range(1, m+1):
                    counts.update_lexical_translation(normalized_count, alignment_info, j)
                    counts.update_distortion(normalized_count, alignment_info, j, l, m)

                counts.update_null_generation(normalized_count, alignment_info)
                counts.update_fertility(normalized_count, alignment_info)


        existing_alignment_table = self.alignment_table
        self.reset_probabilities()
        self.alignment_table = existing_alignment_table

        self.maximize_lexical_translation_probabilities(counts)
        self.maximize_distortion_probabilities(counts)
        self.maximize_fertility_probabilities(counts)
        self.maximize_null_generation_probabilities(counts)

    def maximize_distortion_probabilities(self, counts):
        MIN_PROB = IBMModel.MIN_PROB
        for j, i_s in counts.distortion.items():
            for i, src_sentence_lengths in i_s.items():
                for l, trg_sentence_lengths in src_sentence_lengths.items():
                    for m in trg_sentence_lengths:
                        estimate = (counts.distortion[j][i][l][m] / counts.distortion_for_any_j[i][l][m])
                        self.distortion_table[j][i][l][m] = max(estimate, MIN_PROB)

    def prob_t_a_given_s(self, alignment_info):
        src_sentence = alignment_info.src_sentence
        trg_sentence = alignment_info.trg_sentence
        l = len(src_sentence) - 1  
        m = len(trg_sentence) - 1
        p1 = self.p1
        p0 = 1 - p1

        probability = 1.0
        MIN_PROB = IBMModel.MIN_PROB

        null_fertility = alignment_info.fertility_of_i(0)
        probability *= (pow(p1, null_fertility) * pow(p0, m - 2 * null_fertility))
        if probability < MIN_PROB:
            return MIN_PROB

        for i in range(1, null_fertility + 1):
            probability *= (m - null_fertility - i + 1) / i
            if probability < MIN_PROB:
                return MIN_PROB

        for i in range(1, l + 1):
            fertility = alignment_info.fertility_of_i(i)
            probability *= (factorial(fertility) *
                self.fertility_table[fertility][src_sentence[i]])
            if probability < MIN_PROB:
                return MIN_PROB

        for j in range(1, m + 1):
            t = trg_sentence[j]
            i = alignment_info.alignment[j]
            s = src_sentence[i]

            probability *= (self.translation_table[t][s] *
                self.distortion_table[j][i][l][m])
            if probability < MIN_PROB:
                return MIN_PROB

        return probability


class Model3Counts(Counts):
    def __init__(self):
        super(Model3Counts, self).__init__()
        self.distortion = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
        self.distortion_for_any_j = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

    def update_distortion(self, count, alignment_info, j, l, m):
        i = alignment_info.alignment[j]
        self.distortion[j][i][l][m] += count
        self.distortion_for_any_j[i][l][m] += count


def main():

    bitext = []
    num = sum(1 for line in open('in.txt', encoding = 'utf-8-sig'))

    with open('in.txt', 'r', encoding = 'utf-8-sig') as english, open('out.txt', 'r', encoding = 'utf-8-sig') as hindi:
        Elines = [Eline.rstrip('\n') for Eline in english]
        Hlines = [Hline.rstrip('\n') for Hline in hindi]
        for i in range(num):
            bitext.append(AlignedSent(Elines[i].split(), Hlines[i].split()))

    ibm3 = IBMModel3(bitext, 5)


##    b =[]
##    alignments = []
##    for i in range(len(bitext)):
##        b.append(tuple(Alignment.__str__(bitext[i].alignment)))

##    for t in b:
##        if '-' in t:
##            print(t)
##        
####        b.append (Alignment.__str__(bitext[i].alignment))

##    print(b)
    
        
##
##    for i in range(len(b)):
##        alignments.append(b[i].unicode_repr())
##
##    print(alignments)

##    with open('alignment.txt', 'w', encoding = 'utf-8-sig') as align:
##        align.write(str(b))




##    for i in range(len(b)):
##        alignments.append(b[i])
##        
##        alignments.append(Alignment.fromstring(str(bitext[i].alignment)))
##
##    print(b)
##    print(alignments)
            


    test_sentence = bitext[3]
    print(test_sentence.words,'\n')
    print(test_sentence.mots, '\n')
    print(test_sentence.alignment)

    
if __name__ == '__main__':
    main()

