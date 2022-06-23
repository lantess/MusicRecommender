import os

import librosa
import numpy.fft as fft
import numpy as np
import csv

import Variables as var

length = 20000

def scale_arr(y_arr, x_arr) -> list:
    res = [[] for q in range(int(length/2)+1)]
    for i in range(len(y_arr)):
        x = int(np.floor(x_arr[i]))
        res[x].append(y_arr[i])
    return [float(np.average(arr)) if len(arr) > 0 else 0 for arr in res]


files = os.listdir(var.WAV_DIR)
for file in files:
    file = os.path.join(var.WAV_DIR, file)
    y, sr = librosa.load(file, sr=var.FOURIER_SAMPLES)
    y_data = fft.rfft(y)
    x_data = fft.rfftfreq(len(y), 1/sr)
    scaled = scale_arr(y_data, x_data)
    with open(var.SCALED_FFT_DATA, 'a') as out:
        o = csv.writer(out)
        o.writerow(scaled)
