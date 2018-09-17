from roamtokenize import WordOnlyTokenizer
import re
from nltk.tokenize import sent_tokenize

normalization_patterns = [
        ("long_punctuation_formatting", '(\-{3,}|\.{3,}|\_{3,})',' FORMATTING '),
        ("de-ids", '(([0-9]+[A-Z]+)+[0-9]*|([A-Z]+[0-9]+)+[A-Z]*)', " DEIDENTIFIED "),
        ("data_re", r"\*\*DATE\[\d\d/\d\d(/\d\d\d\d)?]", " DATE "),
        ("initial", r" [A-Z]\.", "INITIAL"),
        ("number_re", '[0-9]+', 'NUMBER')]
        #("whitespace", '\s',  ' ')]

p_to_test = ['date_re', 'number_re']


def normalize(text):
    for pattern in normalization_patterns:
        text = re.sub(pattern[1], pattern[2], text)
    return text

def tokenize(text):
    text = [sent_tokenize(s) for s in text.split('\n') if s]
    sentences = [[word_tokenize(sent) for sent in line] for line in text]
    sentences = '\n'.join(['\n'.join(s) for s in sentences])
    return sentences

TOKENIZER = WordOnlyTokenizer()

def word_tokenize(text):
    return " ".join(TOKENIZER.tokenize(text))
