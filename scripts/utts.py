import glob

aligned = set()

with open('data/aligned.txt') as aligned_file:
    for string in aligned_file:
        aligned.add(string.strip())

words = set()

with open('data/words.txt') as words_file:
    for string in words_file:
        words.add(' ' + string.split('\t')[1] + ' ')

transcripts = dict()

for transcription_filename in glob.glob('data/corpora/*/*.txt'):
    with open(transcription_filename) as transcription_file:
        for string in transcription_file:
            string = string.strip()
            si = string.index(' ')
            utt = string[:si].replace('@', '-').replace(':', '_')
            if utt in aligned:
                transcripts[utt] = ' _SIL_ ' + string[si + 1:] + ' _SIL_ '


with open('data/utts.txt', 'w') as utts_file:
    for word in words:
        for utt in transcripts.keys():
            if word in transcripts[utt]:
                utts_file.write('%s\t%s\n' % (word, utt))
