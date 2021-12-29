import librosa
import matplotlib.pyplot as plt
import os
import numpy as np

for file in os.listdir('../data/wav/'):
    print(file)
    y, sr = librosa.load(os.path.join('../data/wav/', file))
    yf = librosa.feature.mfcc(y=y, sr=sr)
    print(yf.shape)
    for mfcc in yf:
        plt.plot(mfcc)
    plt.show()
