import os
import librosa
import ffmpeg
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

def convert_to_wav():
    for file in os.listdir('data'):
        in_path = os.path.join('data', file)
        out_path = os.path.join('data', file[:file.rfind('.')] + '.wav')
        stream = ffmpeg.input(in_path)
        stream = ffmpeg.output(stream, out_path)
        ffmpeg.run(stream, quiet=True)
        os.remove(in_path)

def to_fft(y, n_fft, size):
    fft = np.transpose(np.abs(librosa.stft(y=y, n_fft=n_fft)))
    res = resize_arrays(fft, size)
    return res

def to_mfcc(y, sr, n_mfcc, size):
    res = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return resize_arrays(np.transpose(res), size)

def to_zcr(y, n_fft, size):
    zcr = librosa.feature.zero_crossing_rate(y, frame_length=n_fft)
    if size > len(zcr):
        padding = [0]
        return [x for x in zcr] + [padding]*(size-len(zcr))
    else:
        ratio = size / len(zcr)
        res = []
        '''for i in range(size):
            res.append([])
        for i in range(len(zcr)):
            index = (int)(np.floor(i * ratio))
            res[index].append(zcr[i])
        for i in range(size):
            res[i] = sum(res[i])/len(res[i])'''
        return res


def main():
    sr = 22050
    n_fft = 4096
    size = 1024
    n_mfcc = 20
    for file in os.listdir('data'):
        y, sr = librosa.load('data/'+file, sr=sr)
        #fft = to_fft(y, n_fft, size)
        zcr = to_zcr(y, n_fft, size)
        #RMS
        #mfcc = to_mfcc(y, sr, n_mfcc, size)



if __name__ == "__main__":
    main()
