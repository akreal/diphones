import glob

print('Reading utterances')

utts = set()

with open('data/utts.txt') as utts_file:
    for string in utts_file:
        utts.add(string.split('\t')[1].strip())

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

print('Reading transcripts')

for transcription_filename in glob.glob('data/corpora/*/*.txt'):
    with open(transcription_filename) as transcription_file:
        for string in transcription_file:
            words = string.strip().split(' ')
            utt = words[0]

            if utt in utts:
                transcription = list()

                for w in words[1:]:
                    if w in vocabulary:
                        transcription.append(vocabulary[w])
                    else:
                        transcription.clear()
                        break

                    if len(transcription) != 0: 
                        grammar_filename = 'data/alignments/' + utt.replace('@', '_').replace(':', '_') + '.jsgf'

                        with open(grammar_filename, 'w') as grammar_file:
                            grammar_file.write('#JSGF V1.0;\n\ngrammar forcing;\n\npublic <phrase> = sil ')
                            grammar_file.write(' [ sil ] '.join(transcription) + ' sil ;\n')

