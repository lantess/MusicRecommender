import glob
import numpy as np
from sklearn import model_selection as ms
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation

def configGPU():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            tf.config.experimental.set_virtual_device_configuration(gpus[0],
                                                                    [tf.config.experimental.VirtualDeviceConfiguration(
                                                                        memory_limit=7168)])
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            print(e)

def disableGPU():
    try:
        tf.config.set_visible_devices([], 'GPU')
        visible_devices = tf.config.get_visible_devices()
        for device in visible_devices:
            assert device.device_type != 'GPU'
    except:
        pass

def iterateFiler(parent: str, rate):
    data = []
    labels = []
    for file in glob.iglob('data/'+parent+'/**/*.bin', recursive=True):
        arr = np.fromfile(file, dtype=np.float32)
        arr = arr.reshape((1024, -1))
        data.append(arr)
        labels.append(rate)
    return data, labels


def main():
    #configGPU()
    disableGPU()

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

    model = Sequential()
    model.add(tf.keras.layers.Conv1D(128, kernel_size=(16, ), activation='sigmoid'))
    model.add(tf.keras.layers.AveragePooling1D((4,)))
    model.add(tf.keras.layers.Conv1D(256, kernel_size=(16,), activation='sigmoid'))
    model.add(tf.keras.layers.AveragePooling1D((4,)))
    model.add(tf.keras.layers.Conv1D(512, kernel_size=(16,), activation='sigmoid'))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation='sigmoid'))
    model.add(tf.keras.layers.Dense(1, activation='softmax'))


    model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError(), metrics=['accuracy'])
    model.fit(data_train, labels_train, epochs=10, validation_data=(data_test, labels_test))


if __name__ == "__main__":
    main()