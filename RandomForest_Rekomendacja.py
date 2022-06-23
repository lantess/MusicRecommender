import glob
import numpy as np
from sklearn import model_selection as ms
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

def iterateFiler(parent: str, rate):
    data = []
    labels = []
    filenames = []
    for file in glob.iglob('data/'+parent+'/**/*.bin', recursive=True):
        arr = np.fromfile(file, dtype=np.float32)
        data.append(arr)
        labels.append(rate)
        filenames.append(file)
        #arr = arr.reshape((size, -1))
        #print(len(arr), " ", len(arr[0]))
    return data, labels, filenames


def main():
    sr = 22050
    n_fft = 4096
    size = 1024
    n_mfcc = 20
    p_data, p_labels, p = iterateFiler("Pozytywne", 1)
    n_data, n_labels, n = iterateFiler("Negatywne", -1)
    r_data, r_labels, filenames = iterateFiler("Nieocenione", 0)
    p_data.extend(n_data)
    p_labels.extend(n_labels)

    data = np.asarray(p_data)
    labels = np.asarray(p_labels)

    n = 250
    forest = RandomForestClassifier(criterion='gini',
                                    n_estimators=n)
    forest.fit(data, labels)
    l = forest.predict(r_data)
    fout = open("bloodyCegla.txt", "w")
    for i in range(len(r_data)):
        if l[i] == 1:
            try:
                fout.write(filenames[i])
                fout.write('\n')
            except:
                print(filenames[i])
    fout.close()
    print("% sugerowanych: ", len([x for x in l if x == 1])/len(l))

if __name__ == "__main__":
    main()