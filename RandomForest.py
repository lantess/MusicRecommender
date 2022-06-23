import glob
import numpy as np
from sklearn import model_selection as ms
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

def iterateFiler(parent: str, rate):
    data = []
    labels = []
    for file in glob.iglob('data/'+parent+'/**/*.bin', recursive=True):
        arr = np.fromfile(file, dtype=np.float32)
        data.append(arr)
        labels.append(rate)
        #arr = arr.reshape((size, -1))
        #print(len(arr), " ", len(arr[0]))
    return data, labels


def main():
    sr = 22050
    n_fft = 4096
    size = 1024
    n_mfcc = 20
    p_data, p_labels = iterateFiler("Pozytywne", 1)
    n_data, n_labels = iterateFiler("Negatywne", -1)
    p_data.extend(n_data)
    p_labels.extend(n_labels)

    data = np.asarray(p_data)
    labels = np.asarray(p_labels)

    data_train, data_test, labels_train, labels_test = ms.train_test_split(data, labels, test_size=0.3)

    for n in [10, 20, 50, 100, 200, 500, 1000]:
        forest = RandomForestClassifier(criterion='gini',
                                        n_estimators=n)
        forest.fit(data_train, labels_train)
        #labels_pred = forest.predict(data_test)
        print(n, " drzew: ", forest.score(data_test, labels_test)*100, "%")
        #print(n, "trees accuracy: ", accuracy_score(labels_test, labels_pred))

if __name__ == "__main__":
    main()