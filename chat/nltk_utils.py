# chat/nltk_utils.py

import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set NLTK data path
nltk_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../nltk_data')
nltk.data.path.append(nltk_data_path)

# Ensure 'punkt' is downloaded
try:
    nltk.data.find('tokenizers/punkt')
    logger.info("Punkt tokenizer data is available.")
except LookupError:
    logger.error("Punkt tokenizer data is not found. Downloading...")
    nltk.download('punkt', download_dir=nltk_data_path)

stemmer = PorterStemmer()

def tokenize(sentence):
    """
    Tokenize a sentence into words
    """
    return nltk.word_tokenize(sentence)

def stem(word):
    """
    Stem a word to its root form
    """
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    """
    Return a bag of words array: 
    1 for each known word that exists in the sentence, 0 otherwise
    """
    # Stem each word
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    # Initialize bag with 0 for each word in the vocabulary
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag

