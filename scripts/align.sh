wav=$1;

jsgf=$(basename -s .wav $wav)".jsgf";

pocketsphinx_continuous \
	-infile $wav \
	-jsgf $jsgf \
	-dict phonemes.dict \
	-backtrace yes \
	-fsgusefiller no \
	-bestpath no \
	-wbeam 1e-1000 \
	-beam 1e-1000 \
	-pbeam 1e-1000 \
	-lpbeam 1e-1000 \
	-lponlybeam 1e-1000 \
	-pl_beam 1e-1000 \
	-pl_pbeam 1e-1000 \
	-pl_window  10000 \
	-maxhmmpf  -1 \
	-remove_silence no \
	2>$wav.log 1>/dev/null
