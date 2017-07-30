import glob
import math
from svgpathtools import svg2paths

def path_point(paths, i, pos):
    r = complex(0.0, 0.0)

    if i < len(paths):
        r = paths[i].point(pos)

    return r

def distance(paths1, paths2):
    i = 0
    distance = 0.0

    while i < len(paths1) or i < len(paths2):
        pos = 0.0

        while pos <= 1.0:
            distance += abs((path_point(paths1, i, pos) - path_point(paths2, i, pos)) ** 2)
            pos += 0.01

        i += 1

    distance = math.sqrt(distance)
    return distance


svgpaths = dict()

for svg in glob.glob('data/articulations/*.svg'):
    paths, _ = svg2paths(svg)
    svgpaths[svg.split('/')[-1][:-4]] = paths

paths = list()

paths.append({
    'spread': svgpaths['lips-spread'],
    'bilabial stop': svgpaths['lips-blstop'],
    'rounded': svgpaths['lips-rounded'],
    'labiodental contact': svgpaths['lips-ld']
})

paths.append({
    'postalveolar fricative': svgpaths['tongue-14'],
    'palatal fricative': svgpaths['tongue-15'],
    'alveolar fricative': svgpaths['tongue-12'],
    'dental fricative': svgpaths['tongue-11'],
    'rest': svgpaths['tongue-00'],
    'velar stop': svgpaths['tongue-26'],
    'alveolar stop': svgpaths['tongue-22']
})

paths.append({
    'oral': svgpaths['top-oral'],
    'nasal': svgpaths['top-nasal']
})

paths.append({
    'voiced': svgpaths['bottom-voiced'],
    'voiceless': svgpaths['bottom-voiceless']
})

phones = dict()

with open('data/phones.txt') as phones_file:
    for string in phones_file:
        controls = string.strip().split('\t')
        phones[controls[0]] = controls[1:]

with open('data/diphones.txt') as diphones_file:
    for string in diphones_file:
        diphone = string.strip()
        [phone1, phone2] = [phones[x] for x in diphone.split('_')]
        difficulty = 0.0

        for i in range(len(paths)):
            if phone1[i] != '-' and phone2[i] != '-':
                difficulty += distance(paths[i][phone1[i]], paths[i][phone2[i]])

        print('%s\t%.3f' % (diphone, difficulty))
