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
'''
metal_arr = ["../data/wav/AC_DC - Danger (Official Music Video).wav",
             "../data/wav/AC_DC - Back In Black (Official Video).wav",
             "../data/wav/AC_DC - Bad Boy Boogie (Live from Rock Goes To College).wav",
             "../data/wav/AC_DC - Ballbreaker (Entertainment Center, Sydney, November 1996).wav",
             "../data/wav/AC_DC - Boogie Man (Plaza De Toros De Las Ventas, July 1996).wav",
             "../data/wav/AC_DC - Cover You In Oil (Official Video).wav",
             "../data/wav/AC_DC - Dirty Deeds Done Dirt Cheap (Joe Louis Arena, Detroit MI, November 1983).wav",
             "../data/wav/AC_DC - Dog Eat Dog (Apollo Theatre, Glasgow, April 1978).wav",
             "../data/wav/AC_DC - Flick Of The Switch (Official Video).wav",
             "../data/wav/AC_DC - Fling Thing_Rocker (Filmed April 30, 1978).wav"]

classic_arr = ["../data/wav/Chopin Nocturne Op.27 No.1 (Arthur Rubinstein).wav",
               "../data/wav/Chopin - Polonaise in A, Op.40 No.1, ' Military '.wav",
               "../data/wav/Chopin - Polonaise in A-flat major, Op. 53 - 'Heroique'.wav",
               "../data/wav/Chopin - Prelude in C minor, op. 28 no. 20 _ Cory Hall, pianist-composer.wav",
               "../data/wav/Chopin - Prelude No 4.wav",
               "../data/wav/Chopin - Prelude Op. 28 No. 15 'Raindrop' in D flat major (Cortot).wav",
               "../data/wav/Chopin Etude op.10-12(Aya was 19 years old).wav",
               "../data/wav/chopin mazurka op.24 no.4 in b flat minor.wav",
               "../data/wav/Chopin Nocturne Op.9 No.2 (Arthur Rubinstein).wav",
               "../data/wav/Chopin  Etude Op. 10 No. 3 in E major 'Tristesse'.wav"]

plt.title("Uśredniony zero-crossing rate dla zbiorów utworów")
plt.xlabel=("Okno czasowe utworu")
plt.ylabel=("Wartość ZCR")

metal = [0] * 1172
classic = [0]*1172

for file in metal_arr:
    y, sr = librosa.load(file, sr=var.FOURIER_SAMPLES, duration=30.0)
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    metal = [x + y for x,y in zip(metal, zcr)]
    #plt.plot(range(len(zcr)), zcr, color='red')

for file in classic_arr:
    y, sr = librosa.load(file, sr=var.FOURIER_SAMPLES, duration=30.0)
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    classic = [x + y for x, y in zip(classic, zcr)]
    #plt.plot(range(len(zcr)), zcr, color='green')

metal = [x/10 for x in metal]
classic = [x/10 for x in classic]

plt.plot(range(len(metal)),
         metal, label="Metal")
plt.plot(range(len(classic)),
         classic, label="Muzyka klasyczna")
plt.legend(loc="upper left")
plt.show()

file = "../data/wav/Czesław Niemen - Ach, jakie oczy [Official Audio].wav"
file2 = "../data/wav/Daria Zawiałow - Helsinki (Official Video).wav"

y, sr = librosa.load(file, sr=var.FOURIER_SAMPLES, duration=30.0)
y2, sr2 = librosa.load(file2, sr=var.FOURIER_SAMPLES, duration=30.0)
zcr = librosa.feature.rms(y)[0]
zcr2 = librosa.feature.rms(y2)[0]
plt.title("RMS dla wybranych utworów")
plt.xlabel=("Okno czasowe utworu")
plt.ylabel=("Wartość RMS")
plt.plot(range(len(zcr)),
         zcr, label="Czesław Niemen - Ach, jakie oczy")
plt.plot(range(len(zcr2)),
         zcr2, label="Daria Zawiałow - Helsinki")
plt.legend(loc="upper left")
plt.show()
print(len(zcr))
'''

metal_arr = ["../data/wav/Daria Zawiałow - Płynne Szczęście.wav"]

classic_arr = ["../data/wav/Kanye West - Diamonds From Sierra Leone.wav"]

pop_arr = ["../data/wav/AC_DC - Whole Lotta Rosie (Live At River Plate, December 2009).wav"]

plt.xlabel=("Okno czasowe utworu")
plt.ylabel=("Wartość RMS")

metal = [0] * 1172
classic = [0]*1172
pop = [0]*1172

for file in metal_arr:
    y, sr = librosa.load(file, sr=var.FOURIER_SAMPLES, duration=30.0)
    zcr = librosa.feature.rms(y)[0]
    metal = [x + y for x,y in zip(metal, zcr)]
    #plt.plot(range(len(zcr)), zcr, color='red')

for file in classic_arr:
    y, sr = librosa.load(file, sr=var.FOURIER_SAMPLES, duration=30.0)
    zcr = librosa.feature.rms(y)[0]
    classic = [x + y for x, y in zip(classic, zcr)]
    #plt.plot(range(len(zcr)), zcr, color='green')

for file in pop_arr:
    y, sr = librosa.load(file, sr=var.FOURIER_SAMPLES, duration=30.0)
    zcr = librosa.feature.rms(y)[0]
    pop = [x + y for x, y in zip(classic, zcr)]
    #plt.plot(range(len(zcr)), zcr, color='green')


metal = [x/len(metal_arr) for x in metal]
classic = [x/len(classic_arr) for x in classic]
pop = [x/len(pop_arr) for x in pop]

plt.plot(range(len(metal)),
         metal, label="Pop")
plt.plot(range(len(classic)),
         classic, label="Hip Hop")
plt.plot(range(len(pop)),
         pop, label="Metal")
plt.legend(loc="upper left")
plt.show()

'''
y, sr = librosa.load("../data/wav/Ed Sheeran-Little Bird Lyrics.wav", sr=var.FOURIER_SAMPLES, duration=30.0)
zcr = librosa.feature.rms(y)[0]


plt.plot([x/512.0 for x in range(len(y))],
         y, label="Dźwięk")
plt.plot(range(len(zcr)),
         zcr, label="RMS")
plt.legend(loc="upper left")
plt.show()
'''