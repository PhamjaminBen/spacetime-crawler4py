from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords


stops = set(stopwords.words('english'))

#modifying stopwords to match the website
stops = stops - {"ain","aren","can","couldn","d","didn","doesn","don'","hadn","hasn","just",'ll', 'm', 'ma','mightn', "mightn't",'mustn','needn', "needn't", 'now', 'o','re', 's','shan',"should've", 'shouldn','t',"that'll", 've', "weren",'wasn',"won","wouldn",'y'}
stops = stops.union({"can't","cannot","couldn't","he'd","he'll","he's","here's","now's","i","i'd","i'll","i'm","i've","she'd","she'll","that's","they'd","they'll","they're","they've","we'd","we'll","we've","we're", "what's", "when's", "where's","who's","why's"})

#punctiation that gets parsed
punctuation = {'(',')','-','_','+','=','[',']','{','}',',','.','<','>',':',"/","\\",'&','?',';','!','@','*','$','#','\'','\"','%','\'\'','\"\"','`','``'}

#combination of stopwords and punctuation so no off tokens are counted
punctuation_stops = punctuation.union(stops)

#splits text into a list of tokens
def tokenize(text: str) -> list:
    tokens = list()
    for token in nltk.word_tokenize(text):
        #prevents replacement characters
        if '�' in token:
            continue
        if token.lower() not in punctuation_stops:
            if len(token) > 1:
                tokens.append(token)
        
    return tokens