import glob
import subprocess

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
            print('Processing utterance ' + utt)

            transcription = list()

            for w in words[1:]:
                if w in vocabulary:
                    transcription.append(vocabulary[w])
                else:
                    transcription.clear()
                    break

            if len(transcription) != 0:
                grammar_filename = 'data/audio/' + utt.replace('@', '-').replace(':', '_') + '.jsgf'

                with open(grammar_filename, 'w') as grammar_file:
                    grammar_file.write('#JSGF V1.0;\n\ngrammar forcing;\n\npublic <phrase> = [ sil ] ')
                    grammar_file.write(' [ sil ] '.join(transcription) + ' [ sil ] ;\n')

                if '@' in utt:
                    mask = '/data/TEDLIUM_release2/*/sph/' + utt[:utt.index('@')] + '.sph'
                else:
                    mask = '/data/LibriSpeech/*/*/*/' + utt + '.flac'

                audio_source = glob.glob(mask)

                if len(audio_source) == 1:
                    audio_filename = grammar_filename[:-4] + 'wav'
                    convert_command = ['sox', audio_source[0], '-c', '1', '-r', '16000', '-b', '16', audio_filename]

                    if '@' in utt:
                        interval = utt[utt.index('@') + 1:].split(':')
                        interval[1] = str(float(interval[1]) - float(interval[0]))
                        convert_command += ['trim'] + interval

                    subprocess.run(convert_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
