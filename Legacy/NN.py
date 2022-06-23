import tensorflow as tf
from sklearn.ensemble import RandomForestClassifier
from tensorflow.keras import layers, models, metrics
from statistics import mode
import pandas as pd
import numpy as np
import Variables as var
from Variables import SQLQuery as query
import Database as db
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def group_rates(rates) -> dict:
    res = {}
    rates = [(id, rate) for (id, rate) in rates if rate != 0]
    for id, rate in rates:
        if id not in res.keys():
            res[id] = []
        res[id].append(rate)
    return res

def avg_rates(rates: dict) -> dict:
    res = {}
    for id in rates.keys():
        res[id] = mode(rates[id])
    return res

csv_data = pd.read_csv(var.SCALED_FFT_DATA, header=None)\
    .to_numpy()
rates = db.execute_query(query.GET_ALL_RATES)
grouped_rates = group_rates(rates)
avg_rates = avg_rates(grouped_rates)

training_ids = []
training_rates = []
training_data = []

for id in avg_rates.keys():
    training_ids.append(id)
    training_rates.append(avg_rates.get(id))
    training_data.append([x for x in csv_data[id]])

test_ids = [x for x in range(len(csv_data)) if x not in training_ids]
test_data = []

for id in test_ids:
    test_data.append([x for x in csv_data[id]])

train_features, test_features, train_labels, test_labels = train_test_split(training_data, training_rates, test_size=0.15)

for n in range(10):
    rf = RandomForestClassifier(n_estimators=450)
    rf.fit(train_features, train_labels)

    predictions = rf.predict(test_features)
    predictions = list(predictions)

    print(n, ':', accuracy_score(test_labels, predictions))
    print([e.get_depth() for e in rf.estimators_])

'''
model = models.Sequential()
model.add(layers.Dense(10000, activation='relu'))
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(1))
model.add(layers.Softmax())

model.compile(optimizer='adamax',
              loss=tf.keras.losses.MeanSquaredError(),
              metrics=['accuracy'])

history = model.fit(training_data, training_rates, epochs=30)
'''
