# PocketSphinx diphone alignment

## Introduction

This repository contains the work I have done for
[Diphone alignment and acoustic scores](https://summerofcode.withgoogle.com/projects/#5723520257490944)
project as a part of Google Summer of Code 2017 program.
Also please see
the pull requests to the upstream
[PocketSphinx](https://github.com/cmusphinx/pocketsphinx/pull/90) and
[CMUSphinx Website](https://github.com/cmusphinx/cmusphinx.github.io/pull/30) repositories.

## Data

### diphones.txt

Initial target list of diphones [provided](https://cmusphinx.github.io/wiki/diphones/)
by the project mentor James Salsman. Used by `words.py` and `difficulties.py` scripts.

### corpora/librispeech, corpora/tedlium2

Text transcriptions imported from
[LibriSpeech ASR corpus](http://www.openslr.org/12/) and
[TED-LIUM corpus release 2](http://www-lium.univ-lemans.fr/en/content/ted-lium-corpus)
in the same format.

### librispeech-lexicon.txt, TEDLIUM.152k.dic

Dictionaries with phonetic transcriptions copied
from the corpora without changes.

### merged.dict

Merged dictionary of the two above.
Produced by `merge_dictionaries.py` script, used by `state_align.c` program.

### phonemes.dict

Phonemes dictionary.
Copied from
[Pocketsphinx for Pronunication Evaluation](https://cmusphinx.github.io/wiki/pocketsphinx_pronunciation_evaluation/)
page, used by `align.sh` script.

### unigrams.txt, bigrams.txt

Lists of unigrams and bigrams listed by frequency obtained from
the contents of `corpora` directory. Produced by `ngrams.py` script, used by `diphones.py` script.

### unigrams_diphones.txt, bigrams_diphones.txt

Same lists, but with diphone transcriptions
built using the dictionaries. Produced by `diphones.py` script, used by `words.py` and `am.py`
scripts.

### words.txt

List of sample words for the diphones. "Words" can be unigrams or bigrams
(in case of diphones containing *salience* phone). Produced by `words.py` script,
used by `utts.py` and `diphone_audio.py` scripts.

### aligned.txt

List of utterances for which forced phonetic aligner (`align.sh`) produced some results.
Produced by running `grep` on the logs of forced phonetic aligner, used by `utts.py` script.

### utts.txt

List of utterances containing sample words. Produced by `utts.py` script,
used by `praat.py` script.

### samples/word

Audio recordings of sample words, extracted from audio prepared by `audio.py` script.
Produced manually with help of `praat.py` and `samples.praat` scripts, used by `diphone_audio.py` script.

### samples/diphone

Audio samples of diphones extracted from the audio recordings of sample words.
Produced by `diphone_audio.py` script, used by `spectrogram.py` and `pitches.praat` scripts.

### img/spectrograms

Spectrogram images of the diphone audio samples.
Produced by `spectrogram.py` script.

### img/pitches

Pitch contour images of the diphone audio samples.
Produced by `pitches.praat` script.

### articulations

SVG files representing different places and manners of articulation.
Actual SVG files are not included but are listed in `svg.lst` file and
can be downloaded from [Interactive Sagittal Section](http://smu-facweb.smu.ca/~s0949176/sammy/)
site using `download.sh` script that can be found in the same directory.
Used by `difficulties.py` script.

### phones.txt

List of phones and corresponding values of the articulation switches
on Interactive Sagittal Section site. Produced manually by self-observation,
used by `difficulties.py` script.

### difficulties.txt

List of diphones with values of difficulty for human pronunciation.
Produced by `difficulties.py` script.

### librispeech-bad-utterances.txt

List of utterances which caused
problems in the diphones AM training. Produced by running `grep` on the logs
of training process, used by `am.py` script.

### diphones-am

Database structure for the diphones AM training.
Produced by `am.py` script, used by `sphinxtrain`.

### model

Diphones AM. Produced by `sphinxtrain`.

## Scripts

### align.sh

Runs `pocketsphinx_continuous` program with certain parameters.

### dict.py

Coverts a dictionary from phone to diphone representation for usage
with a diphone AM.

### diphones.py

Adds diphone-level phonetic transcriptions to a list of ngrams.

### merge_dictionaries.py

Merges two dictionaries into single one.

### praat.py

Prepares list of utterances and TextGrid label files for `samples.praat` script.

### utts.py

Creates list of utterances which both contain sample words for diphones and were
successfully processed by forced phonetic aligner.

### am.py

Generates database structure for the diphones AM training.

### difficulties.py

Calculates the degree of difficulty for human pronunciation for given diphones
based on the distance between SVG paths representing articulation configuration
of two phones composing each of diphones.

### import_tedlium.py

Imports text transcriptions from TED-LIUM corpus structure to this repository.

### ngrams.py

Extracts all ngrams from text transcriptions of the corpora and saves them sorted by frequency.

### samples.praat

Iterates over sample words and utterances, asks user to select an audio interval
with sample word and saves it to the directory with words audio samples.

### words.py

Selects sample words for diphones using rules described
[here](https://sourceforge.net/p/cmusphinx/mailman/message/35804570/).

### audio.py

Selects utterances containing sample words and converts their audio
to the format suitable for PocketSphinx processing.

### diphone_audio.py

Extracts diphone audio samples from word audio samples.

### log2textgrid.py

Converts timestamped labels from output of PocketSphinx to Praat TextGrid label file.

### pitches.praat

Produces pitch contour images for diphone audio samples.

### spectrogram.py

Produces spectrogram images for diphone audio samples.

## Miscellaneous

### state_align.c

Produces a phonetic alignment of given words for given audio file using state search mode of PocketSphinx.
Used in `diphone_audio.py` script for the extraction of diphone's timestamp and duration.

