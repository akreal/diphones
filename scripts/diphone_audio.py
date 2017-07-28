import re
import os.path
import subprocess

phone = re.compile('^([A-Z]{1,3})\t(\d+)\t(\d+)\t-?\d+$')
diphones = dict()

with open('data/words.txt') as words:
    for string in words:
        [diphone, word, _, _] = string.strip().split('\t')
        word_filename = 'data/samples/word/' + re.sub('[^A-Z]','_', word) + '.wav'

        if not os.path.isfile(word_filename):
            continue

        word = word.replace('_SIL_', '<sil>').lower()

        result = subprocess.run(['misc/state_align', word_filename, word],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)

        intervals = list()

        for string in result.stdout.split('\n'):
            match = phone.match(string)
            if match:
                intervals.append({
                    'xmin': float(match.group(2)) / 100,
                    'xmax': float(match.group(3)) / 100,
                    'text': match.group(1)
                })

        if diphone in diphones:
            diphones[diphone] += 1
        else:
            diphones[diphone] = 1

        diphone_filename = 'data/samples/diphone/' + diphone + '_%02d.wav' % (diphones[diphone])

        phones = diphone.split('_')

        for i in range(len(intervals) - 1):
            if intervals[i]['text'] == phones[0] and intervals[i + 1]['text'] == phones[1]:
                if intervals[i]['xmin'] != intervals[i]['xmax'] and intervals[i + 1]['xmin'] != intervals[i + 1]['xmax']:
                    start = intervals[i]['xmin'] + (intervals[i]['xmax'] - intervals[i]['xmin']) * 2 / 3
                    duration = (intervals[i]['xmax'] - intervals[i]['xmin']) * 2 / 3 + \
                        (intervals[i + 1]['xmax'] - intervals[i + 1]['xmin']) / 3

                    subprocess.run(['sox', word_filename, diphone_filename, 'trim', str(start), str(duration)],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                    print('Extracted %s from %s' % (diphone_filename, word_filename))
                else:
                    print('One of %s\'s phones has zero length in %s' % (diphone, word_filename))
