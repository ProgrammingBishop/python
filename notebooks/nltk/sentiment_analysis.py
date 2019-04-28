# ==================================================
# CONTENTS
    # Word Vectors
    # Sentiment Analysis
# ==================================================

import spacy

# Word Vectors
# ==================================================
nlp = spacy.load( 'en_core_web_lg' )
nlp( u'lion' ).vector

tokens = nlp( u'like love hate' )

for token1 in tokens:
    for token2 in tokens:
        print( token1.text, token2.text, token1.similarity( token2 ) )

tokens = nlp( u'dog cat Bioware' )

# vector_norm is sum-of-sqaures euclidean of all dim (300, ) for word
for token in tokens:
    print( token.text, token.has_vector, token.vector_norm, token.is_oov )

# Vector Arithmetic (cosine similarity or words)
from scipy import spatial

cosine_similarity = lambda vec1, vec2: 1 - spatial.distance.cosine( vec1, vec2 )

king  = nlp.vocab[ 'king' ].vector
man   = nlp.vocab[ 'man' ].vector
woman = nlp.vocab[ 'woman' ].vector

new_vec               = king - man + woman
computed_similarities = []

for word in nlp.vocab:
    if word.has_vector:
        if word.is_lower:
            if word.is_alpha:
                similarity = cosine_similarity( new_vec, word.vector )
                computed_similarities.append( ( word, similarity ) )

# For illicit tuples you can sort by first item. -item for descending order of item at index 1 (which is similarity)
computed_similarities = sorted( computed_similarities, key = lambda item : -item[ 1 ] )
print( [ t[ 0 ].text for t in computed_similarities[ :10 ] ] )


# Sentiment Analysis - Unsupervised Learning
# ==================================================
import nltk

nltk.download( 'vader_lexicon' )

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

a = 'This is a good game. BEST EVER MADE!!!'

sid.polarity_scores( a )

a = 'Anthem sucked and I want my money back.'

sid.polarity_scores( a )

import pandas as pd 

df = pd.read_csv( '.\\docs\\amazonreviews.tsv', sep = '\t' )

df[ 'label' ].value_counts()

df.dropna( inplace = True )

blanks = []

for index, label, review in df.itertuples():
    if type( review ) == str:
        if review.isspace():
            blanks.append( index )

df.iloc[0][ 'review' ]
sid.polarity_scores( df.iloc[0][ 'review' ] )

df[ 'scores' ] = df[ 'review' ].apply( lambda review : sid.polarity_scores( review ) )
df[ 'compound' ] = df[ 'scores' ].apply( lambda d : d[ 'compound' ] )

df.head()

df[ 'comp_score' ] = df[ 'compound' ].apply( lambda score : 'pos' if score >= 0 else 'neg' )
df.head()

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print( accuracy_score( df[ 'label' ], df[ 'comp_score' ] ) )
print( classification_report( df[ 'label' ], df[ 'comp_score' ] ) )
print( confusion_matrix( df[ 'label' ], df[ 'comp_score' ] ) )