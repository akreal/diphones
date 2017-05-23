import sys
import glob

for input_filename in glob.glob(sys.argv[1] + '/*/stm/*.stm'):
    output_filename = 'data/corpora/tedlium2/' + input_filename.split('/')[-1][0:-3] + 'txt'

    print(output_filename)

    with open(input_filename) as input_file, open(output_filename, 'w') as output_file:
        for string in input_file:
            parts = string.split()
            output_file.write(' '.join([parts[0] + '@%s:%s' % (parts[3], parts[4])] + [x.upper() for x in parts[6:]]) + '\n')
