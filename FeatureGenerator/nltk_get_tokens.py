"""
Get tokens from NLTK
"""

import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize

def read_stop_words():
    stop_words = []
    with open('common-english-words.txt', 'r') as fh:
        contents = fh.read().split(',')
        for c in contents:
            # Cannot use extend, append is fine
            stop_words.append(c)
    return stop_words

def clean_punctuation(mystr):
    hyperlink = re.compile(r'\bhttp:\\/\\/.*\\/.+?\b')
    twitter_entities = re.compile(r'@|#')
    html_ent = re.compile(r'&amp;')
    punctuation = re.compile(r',|\.|"|\'|\\|/|\||!|\?|:|\-|\(|\)')
    alphanums = re.compile(r'\w+\d|\d+\w')

    # not the best or perfect, but hey
    mystr = re.sub(hyperlink, '', mystr)
    mystr = re.sub(twitter_entities, '', mystr)
    mystr = re.sub(punctuation, '', mystr)
    mystr = re.sub(alphanums, '', mystr)
    mystr = re.sub(html_ent, '', mystr)
    return mystr
    
def clean_stop_words(mystr):
    stop_words = read_stop_words()
    token_list = mystr.split()
    filtered_list = [w for w in token_list if w not in stop_words]
    filtered_string = ' '.join(filtered_list)
    return filtered_string

def lemmatize(wnl, cleaned_str):
    list_of_tokens = cleaned_str.split(' ')
    list_of_lemm_tok = filter(lambda x: wnl.lemmatize(x), list_of_tokens)
    lemm_str = ' '.join(list_of_lemm_tok)
    return lemm_str

def sanitize_for_unicode(mystr):
    return mystr.encode('utf-8')

def generate(mystr):
    # Assumption: garbled yet flat text; one huge string
    # Need: 
        # tokenization
        # stop word removal
        # lemmatization
        # punctuation removal

    filtered_string = clean_stop_words(mystr)
    cleaned_string = clean_punctuation(filtered_string)
    wnl = WordNetLemmatizer()
    lemmatized_string = lemmatize(wnl, cleaned_string)
    return sanitize_for_unicode(lemmatized_string)

