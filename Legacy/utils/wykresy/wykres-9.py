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
y, r = librosa.load(track, duration=d, sr=sr)
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
print(len(mfcc), len(mfcc[0]))
print(mfcc)

i = 0
for m in mfcc:
    plt.plot(range(len(m)), m, label='Filtr '+str(i))
    i = i+1

plt.title("MFCC dla wybranego utworu")
plt.xlabel=("Wartość")
plt.ylabel=("Czas")
plt.legend(loc="lower right")
plt.show()