import lzma

vocabulary = dict()

for n in ['uni', 'bi']:
    with lzma.open('data/{}grams_diphones.txt.xz'.format(n)) as words_file:
        vocabulary[n] = dict()
        for string in words_file:
            [count, word, transcription] = string.decode('utf-8').split('\t')
            vocabulary[n][word] = [transcription.strip(), int(count)]

count = 0

with open('data/diphones.txt') as diphones_file, open('data/words.txt', 'w') as diphone_words_file:
    for string in diphones_file:
        words = list()

        diphone = string.strip()

        if 'SIL' in diphone:
            v = vocabulary['bi']
        else:
            v = vocabulary['uni']

        f = filter(lambda x: diphone in v[x][0], v.keys())
        sorted_by_count = sorted(f, key=lambda x: v[x][1], reverse=True)

        # for each of the 700 most frequent diphones
        if count < 700:
            # 3 words with diphone appearing as near to the front of the word as possible
            words.extend(sorted(filter(lambda x: x not in words, sorted_by_count),
                key=lambda x: v[x][0].index(diphone))[:3])

            # 3 words with the diphone appearing as close to the end of the word as possible
            words.extend(sorted(filter(lambda x: x not in words, sorted_by_count),
                key=lambda x: len(v[x][0]) - v[x][0].rindex(diphone))[:3])

            # 4 words selected for high frequency of use in speech
            words.extend([i for i in filter(lambda x: x not in words, sorted_by_count)][:4])

        # for each of the remaining less frequent diphones
        else:
            # a word with the diphone occurring near the front
            words.extend(sorted(filter(lambda x: x not in words, sorted_by_count),
                key=lambda x: v[x][0].index(diphone))[:1])

            # a word with the diphone occurring near the end
            words.extend(sorted(filter(lambda x: x not in words, sorted_by_count),
                key=lambda x: len(v[x][0]) - v[x][0].rindex(diphone))[:1])

            # the most frequent word with the diphone
            words.extend([i for i in filter(lambda x: x not in words, sorted_by_count)][:1])
 
        for word in words:
            diphone_words_file.write('\t'.join([diphone, word, str(v[word][1]), v[word][0]]) + '\n')

        count += 1
