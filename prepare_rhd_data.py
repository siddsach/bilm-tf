from rkg.restricted.aurora_etl.projects.roam.rhd_100k.organize import \
    Roam100kRHDCanonicalDataClient
from nltk.tokenize import sent_tokenize
from clean_rhd import normalize, str_tokenize
from csv import writer
import os

client = Roam100kRHDCanonicalDataClient()


folder = ''

output_doc = 0
sents = []
vocab = dict()

for i, ex in enumerate(client.iter_all()):

    if i > 10:
        break
    print("BEFORE:")
    print(ex)
    # Cleaning text
    tokenized_text = str_tokenize(ex['fullText'])
    normalized_text = normalize(tokenized_text)
    print("AFTER:")
    print(ex)

    # Adding words to vocab
    for s in normalized_text.split(' '):
        if s not in vocab.keys():
            vocab[s] = 0
        vocab[s] += 1

    # Adding data
    sents += sent_tokenize(normalized_text)

    if (i+1 % 1000) == 0:
        # Write all current data to file and start new file
        current_file = open(os.path.join(folder, str(output) + '.txt'), 'r')
        writer = writer(current_file)
        writer.writerows(sents)
        sents = []
        current_file.close()
        output_doc += 1

# Writing vocab
vocab = sorted(vocab, lambda k: vocab[k])
writer(open('vocab.txt', 'w')).writerows(vocab)



