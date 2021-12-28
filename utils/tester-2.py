import librosa
import matplotlib.pyplot as plt
import scipy.fft as fft
import numpy as np
import os

for file in os.listdir('../data/wav.new/'):
    print(file)
    y, sr = librosa.load(os.path.join('../data/wav.new/', file))
    yf = np.abs(fft.rfft(y, workers=os.cpu_count()))
    xf = fft.rfftfreq(len(y), d=1 / sr)
    plt.plot(xf, yf)

plt.show()