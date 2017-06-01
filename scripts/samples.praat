Read Table from comma-separated file... ../data/utts.csv
select Table utts
nRows = Get number of rows

for i from 1 to nRows
	select Table utts
	utterance$ = Get value... i utterance
	word$ = Get value... i word
	filename$ = Get value... i filename
	start = Get value... i start
	end = Get value... i end

	filename$ = "../data/samples/" + filename$ + ".wav"
	if not fileReadable (filename$)
		Read from file... ../data/audio/'utterance$'.wav
		object_name$ = selected$ ("Sound")
		Read from file... ../data/audio/'utterance$'.TextGrid
		plus Sound 'object_name$'
		View & Edit

		editor: "TextGrid " + object_name$
			if start != end
				Select: start, end
				Zoom to selection
				Zoom out
			endif

			beginPause: "Select the word <" + word$ + ">"
			save = endPause: "Skip", "Save", 2

			if save = 2
				Save selected sound as WAV file... 'filename$'
			endif
		endeditor

		Remove
	endif
endfor
