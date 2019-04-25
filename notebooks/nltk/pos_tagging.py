# ==================================================
# CONTENTS
    # Parts of Speech (POS)
    # Entity Recognition (NER)
# ==================================================

import spacy
from spacy import displacy


# Parts of Speech (POS)
# ==================================================
nlp = spacy.load( 'en_core_web_sm' )
doc = nlp( u'The quick brown fox jumped over the lazy dog' )

pos_counts = doc.count_by( spacy.attrs.POS )
tag_counts = doc.count_by( spacy.attrs.TAG )

# POS ID to Name
for key, value in sorted( pos_counts.items() ):
    print( f'{key:{5}}. {doc.vocab[ key ].text:{7}} {value}' )

for key, value in sorted( tag_counts.items() ):
    print( f'{key:{20}}. {doc.vocab[ key ].text:{7}} {value}' )


# Entity Recognition (NER)
# ==================================================
def show_ents( doc ):
    if doc.ents:
        for ent in doc.ents:
            print( ent.text + " - " + ent.label_ + " - " + str( spacy.explain( ent.label_ ) ) )
    else:
        print( "None found" )

doc = nlp( u'I am a mother, artist, gamer, and photographer' )
show_ents( doc )

# Add Entity
doc = nlp( u'Tesla to build a U.K. factory for $6 million' )

from spacy.tokens import Span

ORG      = doc.vocab.strings[ u'ORG' ]
new_ent  = Span( doc, 0, 1, label = ORG )
doc.ents = list( doc.ents ) + [ new_ent ]

show_ents( doc )

# Add Multiple Entities
doc = nlp( u'Blizzard-Ent just released. a new game called Diablo 4. Blizzard Ent will be at E3' )

from spacy.matcher import PhraseMatcher

matcher         = PhraseMatcher( nlp.vocab )
phrase_list     = [ 'Blizzard-Ent', 'Blizzard Ent' ]
phrase_patterns = [ nlp( text ) for text in phrase_list ]

matcher.add( 'Blizzard', None, *phrase_patterns )

found_matches = matcher( doc )
print( found_matches )

from spacy.tokens import Span

PROD     = doc.vocab.strings[ u'PRODUCT' ]
new_ents = [ Span( doc, match[1], match[2], label = PROD ) for match in found_matches ]

doc.ents = list( doc.ents ) + new_ents
show_ents( doc )


# Sentence Segmentation
# ==================================================
# .sents is a generator (does not hold in memory so not indexable)
# Pass as list to index
for sent in doc.sents:
    print( sent )754