
word = 'ਲੜਿਕਆ'

#ਕਸਈਆ


suffixes = {
    1: [u'ਆਂ', u'ਏ', u'ਓ', u'ਆ', u'ਵ$', u'ਈ', u'ਾਂ', u'ੀਂ', u'ਜ', u'ਸ', u'ਜ਼'], 
    2: [u'ੋ', u'ਿਓ', u'ੇ', u'ਿਆ', u'ਿ◌)']
}

for L in 1,2:
    if len(word) > L + 1:
        for suf in suffixes[L]:
            if word.endswith(suf):
                print(word[:-L])
