from rkg.restricted.aurora_etl.projects.roam.rhd_100k.organize import Roam100kRHDCanonicalDataClient
from nltk.tokenize import sent_tokenize
from clean_rhd import normalize, tokenize
import csv
import os
import boto3

print('Loading Data...')
client = Roam100kRHDCanonicalDataClient()
s3 = boto3.client

folder = 'data'

output_doc = 0
sents = ''
vocab = dict()

print('Preprocessing text...')

for i, ex in enumerate(client.iter_all()):


    # Cleaning text
    normalized_text = normalize(ex['fullText'])
    processed_sentences = tokenize(normalized_text)

    # Adding data
    sents += processed_sentences

    # Adding words to vocab
    for s in normalized_text.split(' '):
        if s is not '\n':
            if s not in vocab.keys():
                vocab[s] = 0
            vocab[s] += 1


    if (i+1) % 2 == 0:
        print('Writing...')
        # Write all current data to file and start new file
        current_file = open(os.path.join(folder, str(output_doc) + '.txt'), 'w')
        current_file.write(sents)
        sents = ''
        current_file.close()
        output_doc += 1
        print('Done.')

import csv
print('Writing Vocab...')
# Writing vocab
vocab = sorted(vocab.keys(), key=lambda k: vocab[k])
csv.writer(open('vocab.txt', 'w')).writerows(vocab)

print('Done.')



