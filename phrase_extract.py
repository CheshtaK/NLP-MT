# -*- coding: utf-8 -*-

def phrase_extraction(srctext, trgtext, alignment):
    def extract(f_start, f_end, e_start, e_end):
        if f_end < 0:  
            return {}
        for e,f in alignment:
            if ((f_start <= f <= f_end) and (e < e_start or e > e_end)):
                return {}

        phrases = set()
        fs = f_start
        while True:
            fe = f_end
            while True:
                src_phrase = " ".join(srctext[i] for i in range(e_start,e_end+1))
                trg_phrase = " ".join(trgtext[i] for i in range(fs,fe+1))
                phrases.add(((e_start, e_end+1), src_phrase, trg_phrase))
                fe += 1 
                if fe in f_aligned or fe == trglen:
                    break
            fs -=1 
            if fs in f_aligned or fs < 0:
                break
        return phrases

    srctext = srctext.split()   
    trgtext = trgtext.split()   
    srclen = len(srctext)       
    trglen = len(trgtext)       
    e_aligned = [i for i,_ in alignment]
    f_aligned = [j for _,j in alignment]

    bp = set() 
    for e_start in range(srclen):
        for e_end in range(e_start, srclen):
            f_start, f_end = trglen-1 , -1  
            for e,f in alignment:
                if e_start <= e <= e_end:
                    f_start = min(f, f_start)
                    f_end = max(f, f_end)
            phrases = extract(f_start, f_end, e_start, e_end)
            if phrases:
                bp.update(phrases)
    return bp

#             0     1     2     3    4 
srctext = "please enter valid phone no"
#           0   1   2  3   4  5 
trgtext = "कृपया मान्य फोन नंबर दर्ज करें"
alignment = [(0,0), (1,4), (1,5), (2,1), (3,2), (4,3)]

phrases = phrase_extraction(srctext, trgtext, alignment)

dlist = {}
for p, a, b in phrases:
    if a in dlist:
        dlist[a][1].append(b)
    else:
        dlist[a] = [p, [b]]

for v in dlist.values():
    v[1].sort(key=lambda x: len(x))


def ordering(p):
    k,v = p
    return v[0]

for i, p in enumerate(sorted(dlist.items(), key = ordering), 1):
    k, v = p
    print ("({0}) {1} {2} — {3}".format( i, v[0], k, " ; ".join(v[1])))
