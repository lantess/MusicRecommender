#TODO: Tu narazie jest ściernisko, ale będzie neuronisko

'''

probability_model = tf.keras.Sequential([model,
                                         tf.keras.layers.Softmax()])
        Wtedy zwraca prawdopodobieństwo a nie jeden gówniak

np.argmax(predictions[0]) - index największego elementu

labele do oddzielnej klasy pls

normalizer = tf.keras.layers.Normalization(axis=-1) - normalizacja

WARSTWY: ADAM SKUP SIĘ KURWA, TO WAŻNE
    INPUT - opisać trochę ten wektor, przynajmniej shape
    No jakaś normalizacja czy coś by się przydała

'''

import tensorflow as tf
from tensorflow.keras import layers, models, metrics
import pandas as pd
import numpy as np
import Variables as var

csv_data = pd.read_csv(var.LEARNING_DATA, names=['tempo', 'weekday', 'month', 'weekend', 'hour',
                'year', 'listened', 'skipped', 'zcr', '0-60Hz', '60-250Hz',
                '250-500Hz', '500-2000Hz', '2-4kHz', '4-6kHz', '6-20kHz',
                'fft_corr', 'hm_fft_corr', 'rms_corr', 'song_id', 'rate'])
labels = csv_data.pop('rate')
song_ids = csv_data.pop('song_id')
data = np.array(csv_data)


model = models.Sequential()
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(20))
model.add(layers.Dense(1))
model.add(layers.Softmax())

model.compile(optimizer='adamax',
              loss=tf.keras.losses.MeanSquaredLogarithmicError(),
              metrics=['accuracy'])

history = model.fit(data, labels, epochs=30, validation_split=0.1)