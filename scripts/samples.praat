Read Table from comma-separated file... ../data/utts.csv
select Table utts
nRows = Get number of rows

for i from 1 to nRows
	select Table utts
	utterance$ = Get value... i utterance
	word$ = Get value... i word
	filename$ = Get value... i filename
	filename$ = "../data/samples/" + filename$ + ".wav"

	if not fileReadable (filename$)
		Read from file... ../data/audio/'utterance$'.wav
		object_name$ = selected$ ("Sound")
		Read from file... ../data/audio/'utterance$'.TextGrid
		plus Sound 'object_name$'
		View & Edit
		pause  Select word 'word$'!

		editor: "TextGrid " + object_name$
			Save selected sound as WAV file... 'filename$'
		endeditor

		Remove
	endif
endfor