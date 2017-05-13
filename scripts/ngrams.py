import glob
import operator

n = 1

ngrams = dict()

for transcription_filename in glob.glob('data/corpora/*/*.txt'):
    with open(transcription_filename) as transcription_file:
        for string in transcription_file:
            string_list = ['_SIL_'] + string.split()[1:] + ['_SIL_']
            for ngram in [' '.join(x) for x in zip(*[string_list[i:] for i in range(n)])]:
                if ngram in ngrams:
                    ngrams[ngram] += 1
                else:
                    ngrams[ngram] = 1

for ngram in sorted(sorted(ngrams.items(), key=operator.itemgetter(0)), key=operator.itemgetter(1), reverse=True):
    print(str(ngram[1]) + ':' + ngram[0])
