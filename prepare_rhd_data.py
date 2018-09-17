from rkg.restricted.aurora_etl.projects.roam.rhd_100k.organize import Roam100kRHDCanonicalDataClient
from nltk.tokenize import sent_tokenize
from clean_rhd import normalize, tokenize
import csv
import os
import boto3

print('Loading Data...')
client = Roam100kRHDCanonicalDataClient()
s3 = boto3.client('s3')

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


    if (i+1) % 1000 == 0:
        print('Writing...')
        # Write all current data to file and start new file
        local_filename = os.path.join(folder, str(output_doc) + '.txt')
        current_file = open(local_filename, 'w')
        current_file.write(sents)
        sents = ''
        current_file.close()

        print('Uploading to S3...')
        s3.upload_file(local_filename, 'roam-developers', os.path.join('yifengtao_elmo_data/rhd', str(output_doc) + '.txt'))
        print('Done.')

        output_doc += 1

import csv
print('Writing Vocab...')
# Writing vocab
vocab = sorted(vocab.keys(), key=lambda k: vocab[k])
csv.writer(open('vocab.txt', 'w')).writerows(vocab)

print('Done.')



