# ==================================================
# CONTENTS
    # Basics
    # Tokenization
    # Visualize Tokenization
    # Stemming
    # Lemmatization (possibly more effective than Stemming)
    # Stop Words
    # Phrase Matching & Vocabulary
# ==================================================

# Basics
# ==================================================
import spacy

# Load Model
nlp = spacy.load( 'en_core_web_sm' )

# Create document
doc = nlp( u'Tesla is looking at buying U.S startup for $6 million' )

for token in doc:
    # text : tokenized word
    # pos_ : part of speech
    # dep_ : syntactic dependency
    print( token.text, token.pos_, token.dep_ )

doc_2 = nlp( u'Tesla is not looking into startups anymore.' )

for token in doc_2:
    print( token.text, token.pos_, token.dep_ )

doc_2[0].pos_
doc_2[0].dep_

doc_3 = nlp( u"The History of Warcraft (also known as the 'history of the Warcraft universe') is a comprehensive account of lore created by Blizzard as background information to the World of Warcraft universe, and was made up of the entirety of Blizzard\'s published record so far. The full text was available on the official World of Warcraft site, but was removed for some unknown reason. In the absence of lore on the official sites, most (perhaps all?) of this material can be read within the World of Warcraft itself as in-game books." )

# Return section of document
wow_lore = doc_3[16:30]
print( wow_lore )

doc_4 = nlp( u'This is the first sentence. This is the second. This is the last.' )

# Return string by sentence
for sentence in doc_4.sents:
    print( sentence )

doc_4[6].is_sent_start


# Tokenization
# ==================================================
string = '"We\'re moving to L.A.!"'
doc    = nlp( string )

for token in doc:
    print( token.text )

# spacy keeps emails and urls intact
doc_2 = nlp( u'Tesla is not looking into startups anymore. sandred@gmail.com snail-mail http://oursite.com' )

for token in doc_2:
    print( token )

# spacy seperates distance measures and dollar symbols
doc_3 = nlp( u'5km is $301.56 in St. Louis in U.S. yes' )

for token in doc_3:
    print( token )

# Named Entities (like proper nouns)
doc_4 = nlp( u'Apple to build a new Hong Kong factory for $6 million' )

for token in doc_4:
    print( token.text, end = '|' )

for entity in doc_4.ents:
    print( entity )
    print( str( spacy.explain( entity.label_ ) ) )
    print( entity.label_ )
    print( '\n' )

# Noun Chunks (non and words describing the noun)
doc_5 = nlp( u'Autonomous cars shift insurance liability toward manufacturers.' )

for chunk in doc_5.noun_chunks:
    print( chunk )

# Visualize Tokenization
# ==================================================
from spacy import displacy

doc = nlp( u'Apple is going to build a U>K> factory for $6 million' )

# dep : syntactic dependency
# ent : entitiy
# view on localhost:5000
displacy.serve( doc, style= 'dep', options = { 'distance' : 110 } )

# Stemming
# ==================================================
# spacy does not have a builtin stemmer
# NLTK is better fit for stemming
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

p_stemmer = PorterStemmer()
s_stemmer = SnowballStemmer( language = 'english' )

words = [ 'run', 'runner', 'ran', 'runs', 'easily', 'fairly' ]

for word in words:
    print( word + '-->' + p_stemmer.stem( word ) )

for word in words:
    print( word + '-->' + s_stemmer.stem( word ) )

# Lemmatization
# ==================================================
doc = nlp( u'I am a runner running in a race because I love to run since I ran today.' )

def show_lemmas( text ):
    for token in text:
        print( f'{token.text:{12}} {token.pos_:{6}} {token.lemma:<{22}} {token.lemma_}' )

show_lemmas( doc )

# Stop Words
print( nlp.Defaults.stop_words )
print( len( nlp.Defaults.stop_words ) )
print( nlp.vocab[ 'is' ].is_stop )

# Add/Remove new stop words
nlp.Defaults.stop_words.add( 'btw' )
nlp.vocab[ 'btw' ].is_stop = True
print( len( nlp.Defaults.stop_words ) )

nlp.Defaults.stop_words.remove( 'btw' )
nlp.vocab[ 'btw' ].is_stop = False
print( len( nlp.Defaults.stop_words ) )

# Phrase Matching & Vocabulary
# ==================================================
from spacy.matcher import Matcher

matcher   = Matcher( nlp.vocab )
pattern_1 = [ { 'LOWER' : 'solarpower' } ]
pattern_2 = [ { 'LOWER' : 'solar' }, { 'IS_PUNCT' : True }, { 'LOWER' : 'power' } ]
pattern_3 = [ { 'LOWER' : 'solar' }, { 'LOWER' : 'power' } ]

matcher.add( 'SolarPower', None, pattern_1, pattern_2, pattern_3 )

doc = nlp( u'The Solar Power inductry continues to grow as solarpower increases. Solar-Power is great.' )

def format_matcher( doc, matcher ):
    for match_id, start, end in matcher:
        string_id = nlp.vocab.strings[ match_id ]
        span      = doc[ start : end ]
        print( match_id, string_id, start, end, span.text )

format_matcher( doc, matcher( doc ) )

# Remove Pattern
matcher.remove( 'SolarPower' )

# Compress pattern_2 and pattern_3
pattern_1 = [ { 'LOWER' : 'solarpower' } ]
# '*' means match 0 or more times
pattern_2 = [ { 'LOWER' : 'solar' }, { 'IS_PUNCT' : True, 'OP' : '*' }, { 'LOWER' : 'power' } ]
matcher.add( 'SolarPower', None, pattern_1, pattern_2 )

doc = nlp( u'The Solar Power inductry continues to grow as solarpower increases. Solar--Power is great.' )

format_matcher( doc, matcher( doc ) )

from spacy.matcher import PhraseMatcher

matcher = PhraseMatcher( nlp.vocab )

doc_3 = nlp( "The History of Warcraft (also known as the 'history of the Warcraft universe') is a comprehensive account of lore created by Blizzard as background information to the World of Warcraft universe, and was made up of the entirety of Blizzard\'s published record so far. The full text was available on the official World of Warcraft site, but was removed for some unknown reason. In the absence of lore on the official sites, most (perhaps all?) of this material can be read within the World of Warcraft itself as in-game books." )

phrase_list = [ 'Warcraft', 'Blizzard', 'lore' ]

phrase_patterns = [ nlp( text ) for text in phrase_list ]

matcher.add( 'BlizzardMatcher', None, phrase_patterns[0], phrase_patterns[1], phrase_patterns[2] )

found_matches = matcher( doc_3 )
print( found_matches )

format_matcher( doc_3, found_matches )