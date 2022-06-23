import Database as db
import Variables as var
import librosa
import os
import struct
import numpy as np
import codecs
import threading
import Database as db
from Variables import SQLQuery as query
import time
import matplotlib.pyplot as plt


track = "../../data/wav/Adele - Send My Love (To Your New Lover).wav"
sr = 22500
d = 120.0
y, sr = librosa.load(track, duration=d, sr=sr)
fft = np.abs(librosa.stft(y=y))

fft = [fft[i] for i in range(int(len(fft)/4))]

s =[]
for f in fft:
    s.append(np.average(f))

#plt.plot(range(len(s)), s)
#plt.show()

plt.imshow(fft, cmap='gnuplot',
           vmin=0, vmax=70, origin='lower', aspect='auto')
plt.colorbar()
plt.show()