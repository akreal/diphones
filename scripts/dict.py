import re
import sys

diphones = set()

with open('data/diphones-am/etc/diphones-am.phone') as diphones_file:
    for string in diphones_file:
        diphones.add(string.strip())

words = set()
altword = re.compile('^(.+)\(\d+\)$')

dictionary_filename = sys.argv[1]
dictionary_diphones_filename = dictionary_filename[:-5] + "-diphones" + dictionary_filename[-5:]

with open(dictionary_filename) as dictionary_file, \
    open(dictionary_diphones_filename, 'w') as dictionary_diphones_file:
    for string in dictionary_file:
        if string[0] != '#':
            parts = [x for x in string.strip().split(' ') if x != '']

            if len(parts) == 2:
                parts.append(parts[1])

            [word, transcription] = [parts[0], ' '.join(parts[1:])]

            transcription = transcription.strip() \
                .replace('AW', 'AA UH') \
                .replace('AY', 'AA IY') \
                .replace('ER', 'UH R') \
                .replace('EY', 'EH IY') \
                .replace('OW', 'AO UH') \
                .replace('OY', 'AO IY')

            transcription = [x.rstrip('0123456789') for x in transcription.split(' ')]
            transcription = ['_'.join(x) for x in zip(transcription, transcription[1:])]
            transcription_set = set(transcription)

            string = ''

            if transcription_set & diphones == transcription_set:
                match = altword.match(word)
                if (match and match.group(1) in words) or (not match):
                    string = '%s %s\n' % (word, ' '.join(transcription))
                    words.add(word)

        dictionary_diphones_file.write(string)
