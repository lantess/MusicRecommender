import glob
import os
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

def convert_to_wav(ext: str):
    for file in glob.iglob('data/**/*.'+ext, recursive=True): #os.listdir('data'):
        in_path = file
        out_path = file[:file.rfind('.')] + '.wav'
        print(in_path)
        stream = ffmpeg.input(in_path)
        stream = ffmpeg.output(stream, out_path)
        ffmpeg.run(stream, quiet=True)
        os.remove(in_path)


def main():
    convert_to_wav("mp3")
    convert_to_wav("flac")



if __name__ == "__main__":
    main()
