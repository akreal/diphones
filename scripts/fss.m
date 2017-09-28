% Based on: Dajani, H. R., Wong, W., & Kunov, H. (2005). Fine structure spectrography and its application in speech. The Journal of the Acoustical Society of America, 117(6), 3902-3918.

pkg load signal;

wav = argv(){1};

[X, fs] = audioread(wav);

fd = abs(stft(X, win_size = 64, inc = 1, num_coef = 4096, win_type="hanning")) .^ 2;

s = zeros(size(fd));

for i = 1:size(fd)(2)
	[val idx] = findpeaks(fd(:,i), "MinPeakHeight", 0.0, "MinPeakDistance", 0, "MinPeakWidth", 0);

	for p = idx'
		pr = max(1, p - 14):min(size(s)(1), p + 14);
		s(pr, i) = fd(pr, i);
	endfor
endfor

% The forth root is suggested in: Cheung, S., & Lim, J. S. (1992). Combined multiresolution (wide-band/narrow-band) spectrogram. IEEE Transactions on signal processing, 40(4), 975-977.
% The magnitude was squared before for the port picking, so I do the eighth root
s = s .^ 0.125;

hf = figure();
imagesc([0, size(X)(1) / fs], [0, 8000], s(1:4000,:));
set(gca,'YDir','normal');
xlabel("Time [sec]");
ylabel("Frequency [Hz]");
print(hf, strcat(wav, "_color.png"));
