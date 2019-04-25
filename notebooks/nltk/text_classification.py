# ==================================================
# CONTENTS
    # Feature Extraction
    # TF-IDF
    # Project Example
# ==================================================

import spacy

import numpy  as np 
import pandas as pd


# Feature Extraction
# ==================================================
doc = [ 
    'In the world of Overwatch, humanity was graced',
    'with a golden age of technology, peace and exploration.',
    'On the exploration front, humans built the Horizon Lunar',
    'Colony. Their focus on the exploration of space, but',
    'also an active research facility. It was manned by a',
    'league of scientists and genetically engineered gorillas',
    'were there to test the effects of prolonged habitation in space.' 
]

X_test = []
y_test = []

y_train = [ 
    'Blizzard', 'Bioware', 'Blizzard', 'Bioware', 
    'Bioware',  'Bioware', 'Bioware' 
]

# Count Vectorization
from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer()

# Fit-Transform
train_counts = count_vect.fit_transform( doc )
train_counts.shape

# TF-IDF
# ==================================================
from sklearn.feature_extraction.text import TfidfTransformer

tf_idf = TfidfTransformer()
tf_idf_doc = tf_idf.fit_transform( train_counts )

tf_idf_doc.shape

# Combine Above Steps
from sklearn.feature_extraction.text import TfidfVectorizer

tf_idfv     = TfidfVectorizer()
tf_idfv_doc = tf_idfv.fit_transform( doc )

from sklearn.svm import LinearSVC

clf = LinearSVC()

clf.fit( tf_idfv_doc, y_train )

from sklearn.pipeline import Pipeline

text_clf = Pipeline([ 
    ( 'tfidf', TfidfVectorizer() ), 
    ( 'clf',   LinearSVC() )
])

text_clf.fit( doc, y_train )

predictions = text_clf.predict( X_test )

from sklearn.metrics import confusion_matrix, classification_report

print( confusion_matrix( y_test, predictions ) )
print( classification_report( y_test, predictions ) )

# Project Example - Decipher if positive or negative
# ==================================================
df = pd.read_csv( '.\\docs\\moviereviews.tsv', sep = '\t' )
df.head()

df.isnull().sum()

df.dropna( inplace = True )

# Better method to drop missing data
blanks = []

for index, _, review in df.itertuples():
    if review.isspace():
        blanks.append( index )

df.drop( blanks, inplace = True )

X = df[ 'review' ]
y = df[ 'label' ]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split( X, y, test_size = 0.3, random_state = 42 )

from sklearn.pipeline                import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm                     import LinearSVC

text_clf = Pipeline([
    ( 'tfidf', TfidfVectorizer() ),
    ( 'clf'  , LinearSVC() )
])

text_clf.fit( X_train, y_train )
predictions = text_clf.predict( X_test )

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print( confusion_matrix( y_test, predictions ) )
print( classification_report( y_test, predictions ) )
print( accuracy_score( y_test, predictions ) )