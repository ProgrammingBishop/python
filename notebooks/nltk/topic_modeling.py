# ==================================================
# CONTENTS
    # Latent Dirichlet Allocation
    # Non-negative Matrix Factorization
# ==================================================


# Latent Dirichlet Allocation
# ==================================================
import pandas as pd 

df = pd.read_csv( '.\\docs\\npr.csv' )
df.head()

from sklearn.feature_extraction.text import CountVectorizer

# max_df     : words to remove that show up in n% of documents
# min_df     : words to keep that show up in n documents
# stop_words : remove stop words
cv = CountVectorizer( max_df = 0.9, min_df = 2, stop_words = 'english' )

dtm = cv.fit_transform( df[ 'Article' ] )

from sklearn.decomposition import LatentDirichletAllocation

# n_components : number of possible categories
lda = LatentDirichletAllocation( n_components = 7, random_state = 42 )

lda.fit( dtm )

# Get vocabulary
cv.get_feature_names()[0]

# Get topics
lda.components_

# Get highest probability word per topic
single_topic = lda.components_[0]
single_topic.argsort()[ -10: ] # Get 10 greatest values (index pos of 10 highest prob words in doc)
top_ten_words = single_topic.argsort()[ -20: ]

for index in top_ten_words:
    print( cv.get_feature_names()[ index ] )

# Loop to get top words for all topics
for index, topic in enumerate( lda.components_ ):
    print( f'The top 15 words for top #{index}' )
    print( [ cv.get_feature_names()[ index ] for index in topic.argsort()[ -15: ] ] )
    print( '\n' )

# Set Topic Label for each Doc
topic_results = lda.transform( dtm )
df[ 'Topic' ] = topic_results.argmax( axis = 1 )
df.head()


# Non-negative Matrix Factorization
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer( max_df = 0.95, min_df = 2, stop_words = 'english' )
dtm   = tfidf.fit_transform( df[ 'Article' ] )

from sklearn.decomposition import NMF

nmf_model = NMF( n_components = 7, random_state = 42 )
nmf_model.fit( dtm )

for index, topic in enumerate( nmf_model.components_ ):
    print( f'The top 15 words for top #{index}' )
    print( [ tfidf.get_feature_names()[ index ] for index in topic.argsort()[ -15: ] ] )
    print( '\n' )

topic_results = nmf_model.transform( dtm )

# Create dictionary matching the topic numbers as keys with inferred topic as values
df[ 'Topic_2' ] = topic_results.argmax( axis = 1 )
df.head()