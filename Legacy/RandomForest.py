import pandas as pd
import numpy as np
import Variables as var
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, roc_auc_score, roc_curve, f1_score

csv_data = pd.read_csv(var.LEARNING_DATA, names=['tempo', 'weekday', 'month', 'weekend', 'hour',
                                                 'year', 'listened', 'skipped', 'language', 'zcr', '0-60Hz', '60-250Hz',
                                                 '250-500Hz', '500-2000Hz', '2-4kHz', '4-6kHz', '6-20kHz',
                                                 'fft_corr', 'hm_fft_corr', 'rms_corr', 'song_id', 'rate'])
labels = csv_data.pop('rate')
song_ids = csv_data.pop('song_id')
data = pd.get_dummies(csv_data)
data = np.array(data)

train_features, test_features, train_labels, test_labels = train_test_split(data, labels, test_size=0.2)

for n in range(100, 1001, 20):
    rf = RandomForestClassifier(n_estimators=n)
    rf.fit(train_features, train_labels)

    predictions = rf.predict(test_features)
    predictions = list(predictions)

    print(n, ':', accuracy_score(test_labels, predictions))