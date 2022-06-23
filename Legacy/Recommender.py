from sklearn.ensemble import RandomForestClassifier

'''
    - utwór jest pobierany, następnie przetwarzany i dodwany do bazy danych, a potem 
        identyfikowany jako id bazie
    - najpierw skrócone FFT dl tych co mają wartości +- jak badana piosenka
    - potem wybieram z nich id
    - potem korelacja
    - potem przerabiam to na wiersz i bajlando, bajlando
'''
import time
import csv

import Database as db
from Variables import SQLQuery as query
import Variables as var
import CorrelationCalculator as cc


class Recommender:

    def _filter_similar(self, main_id: int) -> list:
        main_dataset = [x[1] for x in self._dataset if x[0] == main_id][0]
        avg_fft_corrs = {}
        for id, set in self._dataset:
            if id == main_id:
                continue
            corr = cc.calculate_correlation(main_dataset, set, length=var.FFT_AVG_LEN)
            avg_fft_corrs[id] = corr
        border = var.CORR_MAX
        corr_filtered = {k: v for (k, v) in avg_fft_corrs.items() if v < border}
        while len(corr_filtered) >= var.CORR_N_MAX:
            border /= var.CORR_APPEND_PERCENT
            corr_filtered = {k: v for (k, v) in avg_fft_corrs.items() if v < border}
        while len(corr_filtered) <= var.CORR_N_MIN:
            border *= var.CORR_APPEND_PERCENT
            corr_filtered = {k: v for (k, v) in avg_fft_corrs.items() if v < border}
        return [k for (k, v) in corr_filtered.items()]

    def _fft_similar(self, main_id: int, similar_ids: list) -> dict:
        main_fft = db.execute_query(query.GET_FFT_BY_ID, params=(main_id,))[0][0]
        ffts = {}
        for fft_id in similar_ids:
            fft = db.execute_query(query.GET_FFT_BY_ID, params=(fft_id,))[0][0]
            corr = cc.calculate_correlation(main_fft, fft)
            ffts[fft_id] = corr
        return ffts

    def _fft_high_mag_similar(self, main_id: int, similar_ids: list) -> dict:
        main_fft = db.execute_query(query.GET_FFT_BY_ID, params=(main_id,))[0][0]
        ffts = {}
        for fft_id in similar_ids:
            fft = db.execute_query(query.GET_FFT_BY_ID, params=(fft_id,))[0][0]
            corr = cc.calculate_correlation_from_mag(main_fft, fft, var.MAG_BORDER)
            ffts[fft_id] = corr
        return ffts

    def _rms_similar(self, main_id: int, similar_ids: list) -> dict:
        main_rms, main_rms_len = db.execute_query(query.GET_RMS_BY_ID, params=(main_id,))[0]
        rmss = {}
        for rms_id in similar_ids:
            rms, rms_len = db.execute_query(query.GET_RMS_BY_ID, params=(rms_id,))[0]
            corr = cc.calculate_correlation_from_different_length(main_rms, main_rms_len, rms, rms_len) #TODO: obliczanie korelacji na podstawie różnych długości
            rmss[rms_id] = corr
        return rmss

    def _remove_last_played(self, similar_ids: list) -> list:
        return similar_ids#TODO: FILTER LAST PLAYED SONGS FROM RECOMMENDATION TO PREVENT LOOPING

    def _get_range_fft_dict(self, similar_ids: list) -> dict:
        ffts = {}
        dataset = db.execute_query(query.GET_ALL_FROM_AVG_FFT)
        for data in dataset:
            if data[0] in similar_ids:
                ffts[data[0]] = data[1]
        return ffts

    def _timestamp_to_time_data(self, timestamp: float) -> tuple:
        tdata = time.localtime(timestamp)
        return (tdata.tm_wday,
                tdata.tm_mon,
                1 if tdata.tm_wday > 4 else 0,
                tdata.tm_hour,
                tdata.tm_year)

    def _transform_to_rows(self, ids: list, dicts: tuple, range_ffts: dict) -> tuple:
        '''
            label: id, rate
            data: tempo, time(weekday, month, isWeekend, hour, year),
                % listened, isSkipped, language, zcr, avg_fft(7 els), fft_correlation,
                high_mag_fft_correlation, rms_correlation
            ROWS TO LEARN THE NETWORK    
        ''' #(fft_dict, rms_dict, hm_fft_dist),
        res_matrix = []
        label_matrix = []
        for r_id in ids:
            data_tuples = db.execute_query(query.GET_FEATURES_BY_ID, params=(r_id,))
            duration = db.execute_query(query.GET_SONG_DURATION_BY_ID, params=(r_id,))[0][0]
            for tempo, zrc, timestamp, rate, listening_time, skipped, language_code in data_tuples:
                tdata = self._timestamp_to_time_data(timestamp)
                res = [tempo, tdata[0], tdata[1], tdata[2], tdata[3], tdata[4],
                       listening_time/duration, skipped, language_code, zrc]
                       #listening_time / duration, skipped, zrc]
                res += range_ffts[r_id]
                for d in dicts:
                    res.append(d[r_id])
                res_matrix.append(res)
                label_matrix.append([r_id, rate])
        return res_matrix, label_matrix

    def save_to_csv(self, data: list, labels: list):
        '''res = [['tempo', 'weekday', 'month', 'weekend', 'hour', 'year',
               #'listened', 'skipped', 'language', 'zcr', '0-60Hz', '60-250Hz',
                'listened', 'skipped', 'zcr', '0-60Hz', '60-250Hz',
                '250-500Hz', '500-2000Hz', '2-4kHz', '4-6kHz', '6-20kHz',
                'fft_corr', 'hm_fft_corr', 'rms_corr', 'song_id', 'rate']]'''
        res = []
        for i in range(len(data)):
            res.append(data[i] + labels[i])
        with open(var.LEARNING_DATA, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(res)

    def __init__(self):
        self._dataset = db.execute_query(query.GET_ALL_FROM_AVG_FFT)

    def process_to_datarow(self, main_id: int):
        similar_ids = self._filter_similar(main_id)
        not_last_played_ids = self._remove_last_played(similar_ids)
        fft_dict = self._fft_similar(main_id, not_last_played_ids)
        rms_dict = self._rms_similar(main_id, not_last_played_ids)
        hm_fft_dist = self._fft_similar(main_id, not_last_played_ids)
        range_ffts = self._get_range_fft_dict(not_last_played_ids)
        labels, rows = self._transform_to_rows(similar_ids,
                                       (fft_dict, hm_fft_dist, rms_dict),
                                       range_ffts)
        return rows, labels


rec = Recommender()
labels, data = rec.process_to_datarow(666)
rec.save_to_csv(data, labels)

'''
    Dobra Adam skup się bo to ważne
    Generujesz drzewo/sieć na podstawie wszystkich danych o odsłuchach
    Potem zapisujesz je
    Potem dla wybranych nowych testujesz co i jak kolego, nic straconego
    Potem to kurwa trochę bez sensu
    Nie no dobra skup się kurwa proszę chociaż raz w życiu
    Dobra, to tak - chujnia trochę testować stare rzeczy i wgl, no ale cóż...
    No i tak nie nauczę sieci wszystkimi możliwymi danymi, więc będę musiał zrobić jakieś 10-20k próbek i na podstawie tego to zrobić
    No i bajlando, bo potem jest sens testować te 1k wierszy, bo nie będą koniecznie w lernówce
    Adam jesteś nie taki głupi jak myślałem że jesteś
    No i plan jest sprytny, bardzo sprytny, polecam serduszkiem
    Tylko sieć czy co, bo nie wiem???
    Chuj kurwa sieć neuronowa?
    Dobra, ryzyk fizyk Twoja stara orangutan
'''
