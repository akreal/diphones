import re
import os.path

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

phone = re.compile('^(\w+)\s+(\d+)\s+(\d+)\s+\d+\.\d+\s+-?\d+\s+\d+\s+\d+\s+$')

with open('data/utts.txt') as utts, open('data/utts.csv', 'w') as utts_csv:
    utts_csv.write('utterance,word,filename,start,end\n')

    for string in utts:
        [word, utt] = string.strip().split('\t')
        word = word.strip()
        transcription = [vocabulary[x] for x in word.split(' ')]

        alignment_filename = 'data/audio/' + utt + '.wav.log'

        intervals = list()
        xmax = 0.0
        index2interval = list()

        if not os.path.isfile(alignment_filename):
            continue

        with open(alignment_filename) as alignment:
            for string in alignment:
                match = phone.match(string)
                if match:
                    interval = { 'xmin': float(match.group(2)) / 100, 'xmax': float(match.group(3)) / 100, 'text': match.group(1) }
                    xmax = interval['xmax']

                    for i in range(len(interval['text']) + 1):
                        index2interval.append(len(intervals))

                    intervals.append(interval)

        textgrid_filename = alignment_filename[:-7] + 'TextGrid'

        with open(textgrid_filename, 'w') as tg:
            tg.write('File type = "ooTextFile"\nObject class = "TextGrid"\n\nxmin = 0\n')
            tg.write('xmax = %0.2f\ntiers? <exists>\nsize = 1\n' % (xmax))
            tg.write('item []:\n\titem [1]:\n\t\tclass = "IntervalTier"\n\t\tname = "phoneme"\n')
            tg.write('\t\txmin = 0 \n\t\txmax = %0.2f \n\t\tintervals: size = %d\n' % (xmax, len(intervals)))

            for i in range(len(intervals)):
                tg.write('\t\tinvertals [%d]:\n\t\t\txmin = %0.2f \n\t\t\txmax = %0.2f \n\t\t\ttext = "%s" \n'
                    % (i + 1, intervals[i]['xmin'], intervals[i]['xmax'], intervals[i]['text']))

        intervals_string = ' '.join(x['text'] for x in intervals)
        start = end = 0.0

        for sil in [' ', ' sil ']:
            transcription_string = sil.join(transcription)
            if transcription_string in intervals_string:
                start = intervals[index2interval[intervals_string.index(transcription_string)]]['xmin']
                end = intervals[index2interval[intervals_string.index(transcription_string) + len(transcription_string)]]['xmax']
                break

        utts_csv.write('%s,%s,%s,%0.2f,%0.2f\n' % (utt, word, re.sub('[^A-Z]','_', word), start, end))
