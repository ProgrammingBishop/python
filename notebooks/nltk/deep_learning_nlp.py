# ==================================================
# CONTENTS
    # Overview
    # Chat Bot
# ==================================================


# Overview
def read_file( filepath ):
    with open( filepath ) as f:
        str_text = f.read()

    return str_text

# read_file( '.\\docs\\moby_dick_four_chapters.txt' )
import spacy 

nlp            = spacy.load( 'en', disable = [ 'parser', 'tagger', 'ner' ] )
nlp.max_length = 1198623

def seperate_punctuation( doc_text ):
    return [ token.text.lower() for token in nlp( doc_text ) if token.text not in '\n\n \n\n\n!"-#$%&()--.*+,-/:;<=>?@[\\]^_`{|}~\t\n ' ]

d      = read_file( '.\\docs\\moby_dick_four_chapters.txt' )
tokens = seperate_punctuation( d )

# Predict next word from previously supplied words
train_len = 25 + 1

text_sequences = []

for i in range( train_len, len(tokens) ):
    seq = tokens[ i - train_len:i ]
    text_sequences.append( seq )

from keras.preprocessing.text import Tokenizer

tokenizer = Tokenizer()

tokenizer.fit_on_texts( text_sequences )
sequences = tokenizer.texts_to_sequences( text_sequences )

for i in sequences[0]:
    print( f'{i} : {tokenizer.index_word[i]}' )

vocabulary_size = len( tokenizer.word_counts )
vocabulary_size

import numpy as np 

sequences = np.array( sequences )
sequences


# Chat Bot
# ==================================================