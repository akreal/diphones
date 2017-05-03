import sys

vocabulary = dict()

for dictionary_filename in ['data/librispeech-lexicon.txt', 'data/TEDLIUM.152k.dic']:
    with open(dictionary_filename) as dictionary_file:
        for string in dictionary_file:
            if string[0] != '#':
                if '\t' in string:
                    [word, transcription] = string.strip().split('\t')
                else:
                    parts = string.strip().split(' ')
                    [word, transcription] = [parts[0], ' '.join(parts[1:])]

                if word in vocabulary:
                    # could print it out here for data/lexicon-duplicates.txt
                    next

                transcription = transcription \
                    .replace('AW', 'AA UH') \
                    .replace('AY', 'AA IY') \
                    .replace('ER', 'UH R') \
                    .replace('EY', 'EH IY') \
                    .replace('OW', 'AO UH') \
                    .replace('OY', 'AO IY')
                vocabulary[word] = transcription

with open(sys.argv[1]) as words_file:
    for string in words_file:
        [count, phrase] = string.strip().split(':')

        found = True
        transcription = list()

        for word in phrase.split(' '):
            if word in vocabulary:
                if len(transcription) != 0:
                    transcription.append('SIL')

                for phone in vocabulary[word].split(' '):
                    transcription.append(phone.rstrip('0123456789'))
            else:
                found = False

        if found:
            print(count + '\t' + phrase + '\t' + ' '.join(['_'.join(x) for x in zip(transcription, transcription[1:])]))

