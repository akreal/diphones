import os
import glob
import subprocess

db = 'diphones-am'
db_path = 'data/' + db

os.makedirs(db_path + '/etc', exist_ok=True)

print('Reading unigrams')

vocabulary = dict()

with open('data/unigrams_diphones.txt') as unigrams_file:
    for unigram in unigrams_file:
        parts = unigram.strip().split('\t')

        if len(parts) != 3:
            continue

        word = parts[1].lower()
        transcription = parts[2].strip()
        vocabulary[word] = transcription

print('Reading list of bad utterances')

bad_utterances = set()

with open('data/librispeech-bad-utterances.txt') as bad_utterances_file:
    for utt in bad_utterances_file:
        bad_utterances.add(utt.strip())

print('Reading list of bad (rare) diphones')

bad_diphones = set()

with open('data/librispeech-bad-diphones.txt') as bad_diphones_file:
    for diphone in bad_diphones_file:
        bad_diphones.add(diphone.strip())

os.makedirs(db_path + '/wav', exist_ok=True)

words = set()
phones = set()

for dataset in ['train', 'test']:
    print('Creating ' + dataset + ' dataset')

    with open(db_path + '/etc/' + db + '_' + dataset + '.transcription', 'w') as transcriptions_file, \
            open(db_path + '/etc/' + db + '_' + dataset + '.fileids', 'w') as fileids_file, \
            open(db_path + '/etc/' + dataset + '-text.txt', 'w') as text_file:
        for transcription_filename in glob.glob('/data/LibriSpeech/' + dataset  + '-clean*/*/*/*.txt'):
            with open(transcription_filename) as transcription_file:
                for string in transcription_file:
                    parts = string.strip().split(' ')
                    utterance = parts[0]
                    transcription = [x.lower() for x in parts[1:]]

                    skip = False
                    transcription_phones = set()

                    if utterance in bad_utterances:
                        skip = True

                    for word in transcription:
                        if word in vocabulary:
                            transcription_phones |= set(vocabulary[word].split(' '))
                        else:
                            skip = True
                            break

                    if len(transcription_phones & bad_diphones) > 0:
                        skip = True

                    if not skip:
                        transcription_words = set(transcription)

                        if dataset == 'train':
                            words |= transcription_words
                            phones |= transcription_phones

                        if transcription_words & words == transcription_words and \
                            transcription_phones & phones == transcription_phones:

                            text = ' '.join(transcription)
                            text_file.write(text + '\n')
                            transcriptions_file.write('<s> ' + text + ' </s> (' + utterance + ')\n')
                            fileids_file.write(utterance + '\n')

                            convert_command = ['sox',
                                transcription_filename[:transcription_filename.rindex('/') + 1] + utterance + '.flac',
                                '-c', '1', '-r', '16000', '-b', '16', db_path + '/wav/' + utterance + '.wav']
                            subprocess.run(convert_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print('Creating dictionary')

with open(db_path + '/etc/' + db + '.dic', 'w') as dict_file:
    for word in sorted(words):
        dict_file.write(word + ' ' + vocabulary[word] + '\n')

print('Creating phoneset')

phones.add('SIL')

with open(db_path + '/etc/' + db + '.phone', 'w') as phoneset_file:
    for phone in sorted(phones):
        phoneset_file.write(phone + '\n')
