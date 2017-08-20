# PocketSphinx diphones alignment

## Introduction

This repository contains the work I have done for
[Diphone alignment and acoustic scores](https://summerofcode.withgoogle.com/projects/#5723520257490944)
project as a part of Google Summer of Code 2017 program.
Also please see
the pull requests to the upstream
[PocketSphinx](https://github.com/cmusphinx/pocketsphinx/pull/90) and
[CMUSphinx Website](https://github.com/cmusphinx/cmusphinx.github.io/pull/30) repositories.

## Scripts

## Data

`diphones.txt`: initial target list of diphones [provided](https://cmusphinx.github.io/wiki/diphones/)
by the project mentor James Salsman. Used by `words.py` and `difficulties.py` scripts.

`corpora/librispeech`, `corpora/tedlium2`: text transcriptions imported from
[LibriSpeech ASR corpus](http://www.openslr.org/12/) and
[TED-LIUM corpus release 2](http://www-lium.univ-lemans.fr/en/content/ted-lium-corpus)
in the same format.

`librispeech-lexicon.txt`, `TEDLIUM.152k.dic`: dictionaries with phonetic transcriptions copied
from the corpora without changes.

`merged.dict`: merged dictionary of the two above.
Produced by `merge_dictionaries.py` script, used by `state_align.c` program.

`phonemes.dict`: phonemes dictionary.
Copied from
[Pocketsphinx for Pronunication Evaluation](https://cmusphinx.github.io/wiki/pocketsphinx_pronunciation_evaluation/)
page, used by `align.sh` script.

`unigrams.txt`, `bigrams.txt`: lists of unigrams and bigrams listed by frequency built from
the contents of `corpora` directory. Produced by `ngrams.py` script, used by `diphones.py` script.

`unigrams_diphones.txt`, `bigrams_diphones.txt`: the same lists, but with diphone transcriptions
built using the dictionaries. Produced by `diphones.py` script, used by `words.py` and `am.py`
scripts.

`words.txt`: list of sample words for the diphones. "Words" can be both unigrams and bigrams,
in case of diphones containing *salience* phone. Produced by `words.py` script,
used by `utts.py` and `diphone_audio.py` scripts.

`aligned.txt`: list of utterances for which forced phonetic aligner (`align.sh`) produced some results.
Produced by running `grep` on the logs of forced phonetic aligner, used by `utts.py` script.

`utts.txt`: list of utterances containing sample words. Produced by `utts.py` script,
used by `praat.py` script.

`samples/word`: audio recordings of sample words, extracted from audio prepared by `audio.py` script.
Produced manually with help of `praat.py` and `samples.praat` scripts, used by `diphone_audio.py` script.

`samples/diphone`: audio samples of diphones extracted from the audio recordings of sample words.
Produced by `diphone_audio.py` script, used by `spectrogram.py` and `pitches.praat` scripts.

`img/spectrograms`: spectrogram images of the diphone audio samples.
Produced by `spectrogram.py` script.

`img/pitches`: pitch images of the diphone audio samples.
Produced by `pitches.praat` script.

`articulations`: SVG files representing different places and manners of articulation.
Actual SVG files are not included but are listed in `svg.lst` file and
can be downloaded from [Interactive Sagittal Section](http://smu-facweb.smu.ca/~s0949176/sammy/)
site using `download.sh` script that can be found in the same directory.
Used by `difficulties.py` script.

`phones.txt`: list of phones and corresponding values of articulation switches
on Interactive Sagittal Section site. Produced manually by self-observation,
used by `difficulties.py` script.

`difficulties.txt`: list of diphones with values of difficulty for human pronunciation.
Produced by `difficulties.py` script.

`librispeech-bad-utterances.txt`: list of utterances which caused
problems in the diphones AM training. Produced by running `grep` on the logs
of training process, used by `am.py` script.

`diphones-am`: database structure for the diphones AM training.
Produced by `am.py` script, used by `sphinxtrain`.

`model`: diphones AM. Produced by `sphinxtrain`.

## Miscellaneous

