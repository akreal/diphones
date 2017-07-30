import sys
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram

audio_filename = sys.argv[1]
spectrogram_filename = audio_filename.replace('data/samples/diphone', 'data/img/spectrograms').replace('.wav', '.png')

fs, x = wavfile.read(audio_filename)
f, t, Sxx = spectrogram(x, fs, nperseg=32, nfft=128, mode="magnitude", window=('tukey', 0.1))
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')

plt.savefig(spectrogram_filename)
