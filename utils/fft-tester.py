import librosa
import os
import CorrelationCalculator
import matplotlib.pyplot as plt

reses = []

for file in os.listdir('../data/wav.new/'):
    y, sr = librosa.load('../data/wav/'+file, sr=20000)
    rms = librosa.feature.rms(y=y, frame_length=sr)[0]
    reses.append(rms)

for r in reses:
    for rr in reses:
        cc = CorrelationCalculator.second_my_own_fucking_corr(rr, r)
        print(cc)