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


mellib = librosa.filters.mel(sr=22500, n_fft=2048)
x = librosa.filters.mel(sr=22500, n_fft=2048, n_mels=len(mellib), fmin=0, fmax=22500 / 2)

for i in range(len(mellib)):
    plt.plot(x[i], mellib[i])
plt.show()