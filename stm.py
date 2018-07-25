import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import word_tokenize
from numpy.random import seed
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
from tensorflow import set_random_seed

set_random_seed ( 2 )
seed ( 1 )

filenames = sorted ( glob.glob ( 'fulltext/*.xml' ) )

'''
parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE)) 

summarizer = Summarizer(Stemmer(LANGUAGE))
summarizer.stop_words = get_stop_words(LANGUAGE)

for sentence in summarizer(parser.document, sentence_counts):
    print(sentence)

'''

tokenized_list = [ ]

# Loading the first file and getting all the sentences in it
file = open ( filenames[ 3889 ] , 'r' )
lines = file.read ( ).split ( '\n' )
lines = [ x for x in lines if x not in [ ' ' ] ]
lines = [ x for x in lines if len ( x ) > 0 ]

sentenses = [ ]

for line in lines:
    if (line[ :13 ] == '<sentence id='):
        sentense = line.split ( '>' )[ 1 ].split ( '<' )[ 0 ]
        sentenses.append ( sentense )

sentences = pd.DataFrame ( sentenses , columns=[ 'Sentences' ] )

countVectorizer = CountVectorizer ( strip_accents='unicode' ,
                                    analyzer='word' ,
                                    token_pattern=r'\w{1,}' ,
                                    stop_words='english' ,
                                    ngram_range=(1 , 1) )

vectorizedText = countVectorizer.fit_transform ( sentences[ 'Sentences' ] )

ldaModel = LatentDirichletAllocation ( n_components=10 , learning_method='online' , random_state=0 , verbose=0 )
lda_topics = ldaModel.fit_transform ( vectorizedText )


from collections import Counter

lda_keys = lda_topics.argmax ( axis=1 )
lda_categories , lda_counts = zip ( *Counter ( lda_keys ).items ( ) )

tsne_Model = TSNE ( n_components=2 , perplexity=50 , learning_rate=100 , n_iter=2000 , verbose=1 , random_state=0 ,
                    angle=0.75 )
tsne_vector = tsne_Model.fit_transform ( lda_topics )

for topic in range ( 10 ):
    mask = topic == lda_keys
    sample_mask = np.zeros ( mask.sum ( ) ).astype ( bool )
    sample_mask[ :int ( 1000 / 10 ) ] = True

    plt.scatter ( tsne_vector[ mask , 0 ][ sample_mask ] , tsne_vector[ mask , 1 ][ sample_mask ] ,
                  label='topic {}'.format ( topic ) )

plt.legend ( )
plt.show ( )

textVector = countVectorizer.transform ( [ sentences[ 'Sentences' ][ 10 ] ] )
newTransformedVector = ldaModel.transform ( textVector.toarray ( ) )
topic = np.argmax ( newTransformedVector )
print ( topic )

from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot

model = Word2Vec ( sentences , min_count=1 )

X = model[ model.wv.vocab ]
pca = PCA ( n_components=2 )
result = pca.fit_transform ( X )
pyplot.scatter ( result[ : , 0 ] , result[ : , 1 ] )
words = list ( model.wv.vocab )
for i , word in enumerate ( words ):
    pyplot.annotate ( word , xy=(result[ i , 0 ] , result[ i , 1 ]) )
pyplot.show ( )

total_word_count = 0
for text in sentences[ 'Sentences' ]:
    total_word_count += len ( text.split ( ) )

print ( 'There are {0} words total.'.format ( total_word_count ) )

stop_words = set ( stopwords.words ( 'english' ) )

filtered_sentences = [ ]
filtered_sentences_sent = [ ]
filtered_sentences_word = [ ]

total_word_count = 0

for i in range ( len ( sentences ) ):

    word_tokens = word_tokenize ( sentences[ 'Sentences' ][ i ] )

    print ( word_tokens )

    filtered_sentence = [ w for w in word_tokens if not w in stop_words ]

    filtered_sentence = [ ]

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append ( w )

    for text in sentences[ 'Sentences' ][ i ]:
        total_word_count += len ( text.split ( ) )

    filtered_sentences.append ( filtered_sentence )

print ( 'There are {0} words total.'.format ( total_word_count ) )

tokenized_word_list = [ ]

for i in range ( len ( sentences ) ):
    tree_tokens = TreebankWordTokenizer ( sentences[ 'Sentences' ][ i ] )

tokenized_word_list.append ( tree_tokens )
