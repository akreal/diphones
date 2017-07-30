Create Strings as file list: "wavList", "../data/samples/diphone/*.wav"
nFiles = Get number of strings

for i from 1 to nFiles
	select Strings wavList
	filename$ = Get string: i
	wavfilename$ = "../data/samples/diphone/" + filename$ 
	pngfilename$ = "../data/pitches/" + filename$ - ".wav" + ".png"

	if not fileReadable (pngfilename$)
		Read from file: wavfilename$
		object_name$ = selected$ ("Sound")
		View & Edit

		editor: "Sound " + object_name$
			Draw visible pitch contour: "yes", "no", "no", "no", "no", "yes"
		endeditor

		Save as 300-dpi PNG file: pngfilename$

		Remove
	endif
endfor
