import matplotlib.pyplot as plt
import numpy as np
import librosa

y, sr = librosa.load(librosa.ex('choice'), duration=5)
C = np.abs(librosa.cqt(y, sr=sr))
V = np.abs(librosa.vqt(y, sr=sr))

res = [np.average(c) for c in C]

plt.plot(range(len(res)), res)
plt.show()