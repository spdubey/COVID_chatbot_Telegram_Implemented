import pickle
import re
import string
import nltk
import numpy as np
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag.perceptron import PerceptronTagger
from nltk.stem import PorterStemmer
from numba import jit
from _config import contractions


#
def replace_word_contractions(text):
    for word in text.split():
        if word.lower() in contractions:
            text = text.replace(word, contractions[word.lower()])
    return text

def remove_non_alphabet(text):
    # compile regex
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def remove_URLs(text):
    # compile regex
    url_re = re.compile('(https://+.\S*)')
    text = url_re.sub('', text).strip()
    return text

def remove_digits(text):
    # compile regex
    num_re = re.compile('(\\d+)')
    # remove numbers
    text = num_re.sub('', text)
    return text

def remove_stop_words(text):
    """take a word and check it against the common stop words list from NLTK"""
    stops = set(stopwords.words("english"))
    text = ' '.join([word.lower() for word in text.split() if word.lower() not in stops])
    return text

def porter_stemmer(text):
    pst = PorterStemmer()
    return ' '.join([pst.stem(word) for word in text.split()])

def wordnet_lemmatizer(text):
    word_lem = WordNetLemmatizer()
    return ' '.join([word_lem.lemmatize(word) for word in text.split()])