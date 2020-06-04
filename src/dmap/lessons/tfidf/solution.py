import collections
import math
from lib import Util

def tfidf(documents):

    N_DOC_COUNT = len(documents)
    
    print("calculating TF/Document")
    #TF per document
    vocabulary = collections.Counter()
    doc_tf = [collections.Counter() for x in range(0, N_DOC_COUNT)]
    for d_idx, doc in enumerate(documents):
        tokens = Util.split_into_tokens(doc)
        for t_idx, term in enumerate(tokens):
            doc_tf[d_idx][term] += 1/len(tokens)
            vocabulary[term] += 1
    
    #print(vocabulary.most_common(10))
    #print(doc_tf[0].most_common(10))
    
    #IDF
    print("calculating IDF across documents")
    term_idf = collections.Counter()
    for term in vocabulary:
        # how many documents contain this term?
        term_count = 0
        for d_idx, doc in enumerate(documents):
            tokens = Util.split_into_tokens(doc)
            count = min(1, tokens.count(term)) # either 0 or 1
            term_count += count
        
        # version 1
        #term_idf[term] = math.log10(N_DOC_COUNT/float(max(1, term_count)))
        
        #version best
        term_idf[term] = -1.0 * math.log10(float(term_count)/N_DOC_COUNT)
    
        # version 3
        #term_idf[term] = math.log10( (1 + N_DOC_COUNT) / float(1 + term_count))

        # version 4
        #term_idf[term] = math.log10(N_DOC_COUNT) / float(1 + term_count)

        # version 5 degrades when N_DOC_COUNT is 2 and term_count is 1
        # then all words have zero weight 
        # if (term_count + 1 > N_DOC_COUNT):
        #     term_count = N_DOC_COUNT - 1
        # term_idf[term] = math.log10(N_DOC_COUNT/float(1 + term_count))
        
    tfidf = [collections.Counter() for x in range(0, N_DOC_COUNT)]
    for d_idx, doc in enumerate(documents):
        tokens = Util.split_into_tokens(doc)
        for term in tokens:
            tf  = doc_tf[d_idx][term]
            idf = term_idf[term]
            print("{:12} {:10.3f} {:10.3f}".format(term, tf, idf))
            tfidf[d_idx][term] = tf * idf
        # all done with document d_idx, we could print here
    return tfidf


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

def word_matrix_to_df(wm, feature_names):
    # create an index for each row
    doc_names = ['Doc{:d}'.format(idx) for idx, _ in enumerate(wm)]
    df = pd.DataFrame(data=wm.toarray(), index=doc_names, columns=feature_names)
    return (df)

def v1(corpus):
    # instantiate the vectorizer object
    cvec = CountVectorizer(lowercase=True)

    # convert the documents into a document-term matrix
    # this steps generates word counts for the words in docs
    wm = cvec.fit_transform(corpus)
    # retrieve the terms found in the corpora
    tokens = cvec.get_feature_names()
    # create a dataframe from the matrix
    df = word_matrix_to_df(wm, tokens)
    print(df.head())

def v2(corpus):
    # also pass in a preprocessor as well
    #cvec = CountVectorizer(tokenizer=Util.split_into_tokens)
    cvec = CountVectorizer(tokenizer=Util.split_into_tokens,
                           # both single and bi-grams
                           ngram_range=(1, 2),
                           stop_words=['and', 'but'])
    wm = cvec.fit_transform(corpus)
    tokens = cvec.get_feature_names()
    df = word_matrix_to_df(wm, tokens)
    print(df.head())

def v3(corpus):
    cv = CountVectorizer(tokenizer=Util.split_into_tokens)
    wm = cv.fit_transform(corpus)

    #If you give use_idf = False, you will score using only TF.
    #tfidf = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf.fit(wm)

    df = pd.DataFrame(tfidf.idf_, index=cv.get_feature_names(), columns=["idf_weights"])
    #df = df_idf.sort_values(by=['idf_weights'])
    print(df.head())

def v4(corpus):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([documentA, documentB])
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)

def tfidf_pro(corpus):

    #v3(corpus)
    #return

    # tokenizer=util.tokenize
    vectorizer = TfidfVectorizer(smooth_idf=False, norm=None)
    vectorizer.build_preprocessor()
    vectorizer.build_tokenizer()
    vectorizer.build_analyzer()

    wm = vectorizer.fit_transform(corpus)
    tokens = vectorizer.get_feature_names()
    data = wm.toarray()
    for i, col in enumerate(data):
        print(i)
        for j, n in enumerate(tokens):
            print(tokens[j], col[j])

# doc_names = ['Doc{:d}'.format(idx) for idx, _ in enumerate(wm)]
# df = pd.DataFrame(data=wm.toarray(), index=doc_names,
#                                     columns=tokens)
# print(df.head(10))

if __name__ == "__main__":

    data = Util.read_local_file('data/cith.txt')
    chapters = Util.split_into_chapters(data)
    documents = Util.clean_chapters(chapters)

    # first 3 chapters
    corpus = documents[0:1]
    tfidf_scores = tfidf(corpus)
    Util.print_tfidf(corpus, tfidf_scores, 10)

    tfidf_pro(corpus)
