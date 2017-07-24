import re
import sys

log_filename = sys.argv[1]

phone = re.compile('^(\w+)\s+(\d+)\s+(\d+)\s+-?\d+(\.\d+\s+-?\d+\s+-?\d+\s+\d+\s+)?$')
intervals = list()
xmax = 0.0
index2interval = list()

with open(log_filename) as logfile:
    for string in logfile:
        match = phone.match(string)
        if match:
            interval = { 'xmin': float(match.group(2)) / 100, 'xmax': float(match.group(3)) / 100, 'text': match.group(1) }
            xmax = interval['xmax']

            for i in range(len(interval['text']) + 1):
                index2interval.append(len(intervals))

            intervals.append(interval)

textgrid_filename = log_filename[:-3] + 'TextGrid'
tiername = log_filename.split('/')[-1][:-4]

with open(textgrid_filename, 'w') as tg:
    tg.write('File type = "ooTextFile"\nObject class = "TextGrid"\n\nxmin = 0\n')
    tg.write('xmax = %0.2f\ntiers? <exists>\nsize = 1\n' % (xmax))
    tg.write('item []:\n\titem [1]:\n\t\tclass = "IntervalTier"\n\t\tname = "%s"\n' % (tiername))
    tg.write('\t\txmin = 0 \n\t\txmax = %0.2f \n\t\tintervals: size = %d\n' % (xmax, len(intervals)))

    for i in range(len(intervals)):
        tg.write('\t\tinvertals [%d]:\n\t\t\txmin = %0.2f \n\t\t\txmax = %0.2f \n\t\t\ttext = "%s" \n'
            % (i + 1, intervals[i]['xmin'], intervals[i]['xmax'], intervals[i]['text']))
