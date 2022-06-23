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


tracks = ["../../data/wav/Czesław Niemen - Mów do mnie jeszcze [Official Audio].wav",
          "../../data/wav/AC_DC - You Shook Me All Night Long (Official Video).wav",
          "../../data/wav/Beethoven Symphony No.9.wav",
          "../../data/wav/Les Misérables - 26- Drink With Me.wav"
          ]
label = {tracks[0]: "Rock",
         tracks[1]: "Metal",
         tracks[2]: "Muzyka klasyczna",
         tracks[3]: "Muzyka musicalowa"}

for track in tracks:
    sr = 10000
    d = 1.0
    y, r = librosa.load(track, offset=30.0, duration=d, sr=sr)
    N = int(d * sr);
    fft = np.abs(np.fft.rfft(y))
    x = np.fft.rfftfreq(N, 1/sr)
    plt.plot(x, fft, label=label.get(track))

plt.title("FFT dla wybranych utworów")
plt.xlabel=("HZ")
plt.ylabel=("Moc")
plt.legend(loc="upper left")
plt.show()