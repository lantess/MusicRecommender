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

x_dft = range(1, 60)
x_fft = range(1, 60)

y_dft = [x * x for x in x_dft]
y_fft = [x * np.log2(x) for x in x_fft]

plt.title("Złożoność obliczeniowa poszczególnych algorytmów")
plt.xlabel=("Ilość próbek")
plt.ylabel=("Ilość obliczeń")
plt.plot(x_dft, y_dft, label="DFT")
plt.plot(x_fft, y_fft, label="FFT")
plt.legend(loc="upper left")
plt.show()