from __future__ import division
from collections import defaultdict
from nltk.translate import AlignedSent
from nltk.translate import Alignment
from nltk.translate import IBMModel
from nltk.translate.ibm_model import Counts
import warnings

class IBMModel1(IBMModel):

    def __init__(self, sentence_aligned_corpus, iterations, probability_tables = None):
        super(IBMModel1, self).__init__(sentence_aligned_corpus)

        if probability_tables is None:
            self.set_uniform_probabilities(sentence_aligned_corpus)
        else:
            self.translation_table = probability_tables['translation_table']

        for n in range(0, iterations):
            self.train(sentence_aligned_corpus)

        self.align_all(sentence_aligned_corpus)


    def set_uniform_probabilities(self, sentence_aligned_corpus):
        
        initial_prob = 1 / len(self.trg_vocab)

        if initial_prob < IBMModel.MIN_PROB:
            warnings.warn("Target language vocabulary is too large (" +
                          str(len(self.trg_vocab)) + " words). "
                          "Results may be less accurate.")

        for t in self.trg_vocab:
            self.translation_table[t] = defaultdict(lambda: initial_prob)

    def train(self, parallel_corpus):
        counts = Counts()
        for aligned_sentence in parallel_corpus:
            trg_sentence = aligned_sentence.words
            src_sentence = [None] + aligned_sentence.mots

            total_count = self.prob_all_alignments(src_sentence, trg_sentence)

            for t in trg_sentence:
                for s in src_sentence:
                    count = self.prob_alignment_point(s, t)
                    normalized_count = count / total_count[t]
                    counts.t_given_s[t][s] += normalized_count
                    counts.any_t_given_s[s] += normalized_count
                    
        self.maximize_lexical_translation_probabilities(counts)

    def prob_all_alignments(self, src_sentence, trg_sentence):
        alignment_prob_for_t = defaultdict(lambda: 0.0)
        for t in trg_sentence:
            for s in src_sentence:
                alignment_prob_for_t[t] += self.prob_alignment_point(s, t)
        return alignment_prob_for_t

    def prob_alignment_point(self, s, t):
        return self.translation_table[t][s]

    def prob_t_a_given_s(self, alignment_info):
        prob = 1.0

        for j,i in enumerate(alignment_info.alignment):
            if j==0:
                continue
            trg_word = alignment_info.trg_sentence[j]
            src_word = alignment_info.src_sentence[i]
            prob *= self.translation_table[trg_word][src_word]

        return max(prob, IBMModel.MIN_PROB)

    def align_all(self, parallel_corpus):
        for sentence_pair in parallel_corpus:
            self.align(sentence_pair)

    def align(self, sentence_pair):

        best_alignment = []
        
        for j, trg_word in enumerate(sentence_pair.words):
            best_prob = max(self.translation_table[trg_word][None], IBMModel.MIN_PROB)
            best_alignment_point = None

            for i, src_word in enumerate(sentence_pair.mots):
                align_prob = self.translation_table[trg_word][src_word]

                if align_prob >= best_prob:
                    best_prob = align_prob
                    best_alignment_point = i

            best_alignment.append((j, best_alignment_point))

        sentence_pair.alignment = Alignment(best_alignment)


def main():

    bitext = []
    num = sum(1 for line in open('in.txt', encoding = 'utf-8-sig'))

    with open('in.txt', 'r', encoding = 'utf-8-sig') as english, open('out.txt', 'r', encoding = 'utf-8-sig') as hindi:
        Elines = [Eline.rstrip('\n') for Eline in english]
        Hlines = [Hline.rstrip('\n') for Hline in hindi]
        for i in range(num):
            bitext.append(AlignedSent(Elines[i].split(), Hlines[i].split()))

    ibm1 = IBMModel1(bitext, 5)

    test_sentence = bitext[3]
    print(test_sentence.words,'\n')
    print(test_sentence.mots, '\n')
    print(test_sentence.alignment)

    
if __name__ == '__main__':
    main()
