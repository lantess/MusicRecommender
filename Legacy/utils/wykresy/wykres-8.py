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
    sr = 22500
    d = 120.0
    y, r = librosa.load(track, duration=d, sr=sr)
    tempo = librosa.beat.tempo(y=y, sr=r, aggregate=None)
    print(tempo)
    plt.plot(range(len(tempo)), tempo, label=label.get(track))

plt.title("FFT dla wybranych utworów")
plt.xlabel=("Okno")
plt.ylabel=("Tempo")
plt.legend(loc="upper left")
plt.show()