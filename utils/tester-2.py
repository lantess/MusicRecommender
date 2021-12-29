import librosa
import matplotlib.pyplot as plt
import os
import numpy as np

for file in os.listdir('../data/wav/'):
    print(file)
    y, sr = librosa.load(os.path.join('../data/wav/', file))
    zcr = librosa.feature.zero_crossing_rate(y + 0.0001)
    print(np.average(zcr[0]), len(zcr[0]), zcr[0])

