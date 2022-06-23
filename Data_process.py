import os
import struct
import glob

import librosa
import numpy as np

def resize_arrays(arr: list, size: int) -> list:
    if size > len(arr):
        padding = [0]*len(arr[0])
        return [x for x in arr] + [padding]*(size-len(arr))
    else:
        ratio = size / len(arr)
        res = []
        for i in range(size):
            res.append([])
        for i in range(len(arr)):
            index = (int)(np.floor(i * ratio))
            res[index].append(arr[i])
        for i in range(size):
            res[i] = np.mean(res[i], axis=0)
        return res

def to_fft(y, n_fft, size):
    fft = np.transpose(np.abs(librosa.stft(y=y, n_fft=n_fft)))
    res = resize_arrays(fft, size)
    return res

def to_mfcc(y, sr, n_mfcc, size):
    res = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return resize_arrays(np.transpose(res), size)

def to_zcr(y, n_fft, size):
    zcr = librosa.feature.zero_crossing_rate(y, frame_length=n_fft)[0]
    if size > len(zcr):
        padding = [0]
        return [x for x in zcr] + [padding]*(size-len(zcr))
    else:
        ratio = size / len(zcr)
        res = []
        for i in range(size):
            res.append([])
        for i in range(len(zcr)):
            index = (int)(np.floor(i * ratio))
            res[index].append(zcr[i])
        for i in range(size):
            res[i] = sum(res[i])/len(res[i])
        return res

def to_rms(y, n_fft, size):
    rms = librosa.feature.rms(y, frame_length=n_fft)[0]
    if size > len(rms):
        padding = [0]
        return [x for x in rms] + [padding] * (size - len(rms))
    else:
        ratio = size / len(rms)
        res = []
        for i in range(size):
            res.append([])
        for i in range(len(rms)):
            index = (int)(np.floor(i * ratio))
            res[index].append(rms[i])
        for i in range(size):
            res[i] = sum(res[i]) / len(res[i])
        return res

def main():
    sr = 22050
    n_fft = 4096
    size = 1024
    n_mfcc = 20
    for file in glob.iglob('data/**/*.wav', recursive=True):
        out_file = file.replace(".wav", ".bin")
        if not os.path.exists(out_file):
            print(file)
            y, sr = librosa.load(file, sr=sr)
            fft = to_fft(y, n_fft, size)
            zcr = to_zcr(y, n_fft, size)
            rms = to_rms(y, n_fft, size)
            mfcc = to_mfcc(y, sr, n_mfcc, size)
            params = []
            for i in range(size):
                p = []
                p.extend(fft[i])
                p.extend(mfcc[i])
                p.append(zcr[i])
                p.append(rms[i])
                params.append(p)
            fout = open(out_file, "wb")
            try:
                for p in params:
                    fout.write(struct.pack("f"*len(p), *p))
                fout.close()
            except:
                fout.close()
                os.remove(file)
                os.remove(out_file)



if __name__ == "__main__":
    main()
