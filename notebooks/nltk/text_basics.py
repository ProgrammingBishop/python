# Read from text file
# with open( '.\\temp\\test.txt', 'r' ) as f:
#     var = f.readlines()


# Read from PDF file
# import PyPDF2

# file       = open( '.\\temp\\test.pdf', mode = 'rb' )
# pdf_reader = PyPDF2.PdfFileReader( file )
# page_one   = pdf_reader.getPage( 0 )

# page_one.extractText()

# file.close()


# Regular Expressions
import re 

text    = "The phone number is 123-456-7890. Call soon!"
pattern = "phone"

match      = re.search( pattern, text )
match_all  = re.findall( pattern, text )

for match in re.finditer( pattern, text ):
    print( match.span() )

print( match.start() )

pattern      = r'\d{3}-\d{3}-\d{4}'
phone_number = re.search( pattern, text )
print( phone_number.group() )

pattern      = r'(\d{3})-(\d{3})-(\d{4})'
phone_number = re.search( pattern, text )
print( phone_number.group(1) )

re.search( r'man|woman', 'This woman was here' )

re.findall( r'.at', "The cat in the hat sat" ) # wildcard
re.findall( r'\d$', 'This ends with 2' ) # ends with
re.findall( r'^\d', '1 is the loniest number' ) # starts with
re.findall( r'[^\d]+', '4 This 4 ends 5 with 2' ) # [^] = exclusion, + avoids letters returned
re.findall( r'[^?!.,"]+', 'This?DS ends!GFH with..," 2' ) # remove punctuation
re.findall( r'[\w]+-[\w]+', 'only-find the words that-are hyphenated-words' )