import librosa
import matplotlib.pyplot as plt
import scipy.fft as fft
import os

y, sr = librosa.load('../data/wav/14 Yours Truly, Austin Post.wav')
n = 640000

yf = fft.rfft(y, workers=os.cpu_count())
xf = fft.rfftfreq(len(y), d=1/sr)
yf2 = fft.rfft(y, workers=os.cpu_count(), n=n)
xf2 = fft.rfftfreq(n, d=1/sr)

print(xf)
print(xf2)

plt.plot(xf, yf)
plt.plot(xf2, yf2)
plt.show()