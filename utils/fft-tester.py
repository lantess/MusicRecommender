import librosa
import numpy as np
import os
import CorrelationCalculator

reses = []

for file in os.listdir('../data/wav.new/'):
    y, sr = librosa.load('../data/wav/'+file, sr=20000)
    ff = np.abs(librosa.stft(y, n_fft=int(sr)))
    res = [np.average(x) for x in ff]
    print(len(res))
    reses.append(res)

for r in reses:
    for rr in reses:
        if r != rr:
            print(CorrelationCalculator.diff(r, rr))