vocabulary = dict()

for n in ['uni', 'bi']:
    with open('data/{}grams_diphones.txt'.format(n)) as words_file:
        for string in words_file:
            [count, word, transcription] = string.split('\t')
            vocabulary[word] = [transcription.strip(), int(count)]

def context(diphone, phrase):
    t = vocabulary[phrase][0].split(' ')

    #if diphone not in t:
    #    print(diphone)
    #    print(t)

    di = t.index(diphone)
    context = ''

    if di != 0:
        context += t[di - 1]
    else:
        context += 'BEGIN'

    context += t[di]

    if di != len(t) - 1:
        context += t[di + 1]
    else:
        context += 'END'

    return context

def ifseen(diphone, phrase, seen):
    candidate = set([context(diphone, phrase)])

    if len(seen.intersection(candidate)) > 0:
        return False
    else:
        seen |= candidate
        return True

count = 0

with open('data/diphones.txt') as diphones_file, open('data/words.txt', 'w') as diphone_words_file:
    for string in diphones_file:
        words = list()
        seen = set()

        diphone = string.strip()

        v = vocabulary
        f = filter(lambda x: diphone in v[x][0].split(' '), v.keys())
        sorted_by_count = sorted(f, key=lambda x: v[x][1], reverse=True)

        # for each of the 700 most frequent diphones
        if count < 700:
            # 3 words with diphone appearing as near to the front of the word as possible
            words.extend(sorted(filter(lambda x: ifseen(diphone, x, seen), sorted_by_count),
                key=lambda x: v[x][0].index(diphone))[:3])

            seen = set([context(diphone, x) for x in words])

            # 3 words with the diphone appearing as close to the end of the word as possible
            words.extend(sorted(filter(lambda x: ifseen(diphone, x, seen), sorted_by_count),
                key=lambda x: len(v[x][0]) - v[x][0].rindex(diphone))[:3])

            seen = set([context(diphone, x) for x in words])

            # 4 words selected for high frequency of use in speech
            words.extend([i for i in filter(lambda x: ifseen(diphone, x, seen), sorted_by_count)][:4])

        # for each of the remaining less frequent diphones
        else:
            # a word with the diphone occurring near the front
            words.extend(sorted(filter(lambda x: ifseen(diphone, x, seen), sorted_by_count),
                key=lambda x: v[x][0].index(diphone))[:1])

            seen = set([context(diphone, x) for x in words])

            # a word with the diphone occurring near the end
            words.extend(sorted(filter(lambda x: ifseen(diphone, x, seen), sorted_by_count),
                key=lambda x: len(v[x][0]) - v[x][0].rindex(diphone))[:1])

            seen = set([context(diphone, x) for x in words])

            # the most frequent word with the diphone
            words.extend([i for i in filter(lambda x: ifseen(diphone, x, seen), sorted_by_count)][:1])
 
        for word in words:
            diphone_words_file.write('\t'.join([diphone, word, str(v[word][1]), v[word][0]]) + '\n')

        count += 1
        print('Done diphone ' + str(count))
