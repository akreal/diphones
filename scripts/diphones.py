import sys

vocabulary = dict()

with open('data/librispeech-lexicon.txt') as dictionary_file:
    for string in dictionary_file:
        if string[0] != '#':
            [word, transcription] = string.strip().split('\t')
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
        [_, phrase] = string.strip().split(':')

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
            print(phrase, '  ', ' '.join(['_'.join(x) for x in zip(transcription, transcription[1:])]))

