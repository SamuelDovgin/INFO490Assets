#
# do NOT edit this file, it is copied
# from a master repository
#

import re



'''
the following regular expression tokenize's the text: 
['A-Za-z0-9]+-?['A-Za-z0-9]+ 
Note that this regular expression will
skip single letter words (and numbers)
not match double hyphenated words (Aunt--Poly) (it will be two matches)
keep single hyphenated words (e.g. iron-will)
include the apostrophe in all of its possible uses. 
Make sure you understand why the given regular expression 
has those limitations.  
how to treat: you-did—I-didn't
'''

def clean_chapter(chapter):
    c = chapter.replace("\n", " ")
    pattern = r"[A-Za-z0-9']+-?[A-Za-z0-9']+"
    # pattern = r"[A-Za-z0-9']+"
    regex = re.compile(pattern)
    tokens = regex.findall(c)

    # remove leading and trailing single quotes
    t = [t.strip("'") for t in tokens]
    return " ".join(t).strip()

def clean_chapters(chapters):
    out = []
    for i, c in enumerate(chapters):
        c = clean_chapter(c)
        if len(c) > 0:
            out.append(c)
    return out


def split_into_chapters(data):
    pattern = r'^CHAPTER\s[A-Z\s]+\.?$'
    # pattern = r'CHAPTER\s[A-Z\s]+'
    regex = re.compile(pattern, re.M)
    return [d.trim() in regex.split(data) if len(data.trim()) > 0]
    #return regex.split(data)


'''
normalize the tokens
Then for each of the returned tokens (from using the regular expression)
strip off any leading and trailing apostrophes
keep the internal ones
do NOT change the case of the word
you will need to use the powerful string methods you learned in the bootcamp
'''
def split_into_tokens(data, normalize=True, min_length=2):
    tokens = data.split()
    if normalize:
        tokens = [t.lower() for t in tokens if len(t) > min_length]
    return tokens


def print_tfidf(documents, tfidf, top_n):
    for d_idx, doc in enumerate(documents):
        top_10 = tfidf[d_idx].most_common(top_n)
        print("Document: {}".format(d_idx+1))
        for word, score in top_10:
            print(" Word: {:14.12} TF-IDF: {:10.5f}".format(word, round(score, 5)))
