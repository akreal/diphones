import re
import os.path

print('Reading vocabularies')

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

                word = word.upper()

                if word in vocabulary:
                    next

                transcription = transcription \
                    .replace('AW', 'AA UH') \
                    .replace('AY', 'AA IY') \
                    .replace('ER', 'UH R') \
                    .replace('EY', 'EH IY') \
                    .replace('OW', 'AO UH') \
                    .replace('OY', 'AO IY')

                transcription = ''.join(filter(lambda x: not x.isdigit(), transcription))

                vocabulary[word] = transcription.lower()

vocabulary['_SIL_'] = 'sil'

print('Generating grammars')

with open('data/words.txt') as words:
    for string in words:
        [_, word, _, _] = string.strip().split('\t')
        wav_filename = 'data/samples/' + re.sub('[^A-Z]','_', word) + '.wav'
        transcription = [vocabulary[x] for x in word.split(' ')]

        if not os.path.isfile(wav_filename):
            continue

        grammar_filename = wav_filename[:-3] + 'jsgf'

        with open(grammar_filename, 'w') as grammar_file:
            grammar_file.write('#JSGF V1.0;\n\ngrammar forcing;\n\npublic <phrase> = [ sil ] ')
            grammar_file.write(' '.join(transcription) + ' [ sil ] ;\n')

