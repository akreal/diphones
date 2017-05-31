import re
import os.path

phone = re.compile('^(\w+)\s+(\d+)\s+(\d+)\s+\d+\.\d+\s+-?\d+\s+\d+\s+\d+\s+$')

with open('data/utts.txt') as utts, open('data/utts.csv', 'w') as utts_csv:
    utts_csv.write('utterance,word,filename\n')

    for string in utts:
        [word, utt] = string.strip().split('\t')
        word = word.strip()

        alignment_filename = 'data/audio/' + utt + '.wav.log'

        intervals = list()
        xmax = 0.0

        if not os.path.isfile(alignment_filename):
            continue

        with open(alignment_filename) as alignment:
            for string in alignment:
                match = phone.match(string)
                if match:
                    interval = { 'xmin': float(match.group(2)) / 100, 'xmax': float(match.group(3)) / 100, 'text': match.group(1) }
                    xmax = interval['xmax']
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

        utts_csv.write('%s,%s,%s\n' % (utt, word, re.sub('[^A-Z]','_', word)))
        #if not os.path.isfile('data/samples/' + sample_filename):
        #    print('Word: "%s"; file: "%s"' %(word, sample_filename))
        #    subprocess.call(['praat', '--open', textgrid_filename, alignment_filename[:-4]])
