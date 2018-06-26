from nltk.translate import AlignedSent, IBMModel1

bitext = []
bitext.append(AlignedSent(['klein', 'ist', 'das', 'haus'], ['the', 'house', 'is', 'small']))
bitext.append(AlignedSent(['das', 'haus', 'ist', 'ja', 'groß'], ['the', 'house', 'is', 'big']))
bitext.append(AlignedSent(['das', 'buch', 'ist', 'ja', 'klein'], ['the', 'book', 'is', 'small']))
bitext.append(AlignedSent(['das', 'haus'], ['the', 'house']))
bitext.append(AlignedSent(['das', 'buch'], ['the', 'book']))
bitext.append(AlignedSent(['ein', 'buch'], ['a', 'book']))

print(bitext, '\n')

ibm1 = IBMModel1(bitext, 5)

print(ibm1.translation_table['buch']['book'], '\n')

test_sentence = bitext[2]
print(test_sentence.words, '\n')
print(test_sentence.mots, '\n')
print(test_sentence.alignment, '\n')
