import librosa
import matplotlib.pyplot as plt
import os
import numpy as np

for file in os.listdir('../data/wav/'):
    print(file)
    y, sr = librosa.load(os.path.join('../data/wav/', file))
    ff = np.abs(librosa.stft(y, n_fft=int(sr)))
    res = [np.average(x) for x in ff]
    plt.plot(res)
    plt.show()
