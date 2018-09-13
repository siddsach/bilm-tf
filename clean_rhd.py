from roamtokenize import WordOnlyTokenizer
from roamtokenize.regex_strings import *
import re

normalization_patterns = {
        "date_re" : ('', '**DATE**'
        "number_re" : ('\s[0-9]+\s', '**NUMBER**')
        "long_ellipses" : ('','**ELLIPSE**'),
        "new lines" : ('\n'. ' '),
        "de-ids" : ('[A-Z0-9]{4,}', "**DEIDENTIFIED**"),
        "special numbers": "[0-9]+|\p+": "**SPECIALNUMBER**",
        }

things_to_normalize = list(normalization_patterns.keys())

def normalize(text):

    for pattern in things_to_normalize:
        re.sub(text, normalization_patterns[pattern][0], normalization_patterns[pattern][1])

    return text


TOKENIZER = WordOnlyTokenizer()

def str_tokenize(text):
    return " ".join(TOKENIZER.tokenize(text))
