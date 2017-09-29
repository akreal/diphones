import re
import os
import subprocess

genders = dict()

with open('data/utt2gender.txt') as utt2gender:
    for string in utt2gender:
        [utt, gender] = string.strip().split('\t')
        genders[utt] = gender

utts = dict()

with open('data/diphone2utt.txt') as diphone2utt:
    for string in diphone2utt:
        [diphone, utt] = string.strip().split('\t')
        utts[diphone] = utt

print('Diphone\tSpectrogram\tWord\tWord count\tPosition from the word\'s start\tPosition from the word\'s end\tSample duration\tUtterance\tSpeaker\'s gender\tSpeech type')

dre = re.compile('Duration: \d\d:\d\d:(\d\d\.\d\d)')
diphones = dict()

with open('data/words.txt') as words:
    for string in words:
        [diphone, word, count, transcription] = string.strip().split('\t')
        word_filename = 'data/samples/word/' + re.sub('[^A-Z]','_', word) + '.wav'

        if not os.path.isfile(word_filename):
            continue

        if diphone in diphones:
            diphones[diphone] += 1
        else:
            diphones[diphone] = 1

        filename = '%s_%02d' % (diphone, diphones[diphone])
        wav_filename = 'data/samples/diphone/' + filename + '.wav'
        duration = ''

        if os.path.isfile(wav_filename):
            result = subprocess.run(['ffprobe', wav_filename],
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, universal_newlines=True)

            match = dre.search(result.stderr)

            if match:
                duration = match.group(1)
        else:
            continue

        transcription = transcription.split(' ')
        lposition = transcription.index(diphone) + 1
        transcription.reverse()
        rposition = transcription.index(diphone) + 1

        utt = utts[filename + '.wav']

        st = 'spontaneous'

        if utt[0].isdigit():
            st = 'read'

        print('%s\t%s.png\t%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s' %
            (diphone, filename, word, int(count), lposition, rposition, duration, utt, genders[utt], st))
