from sklearn.ensemble import RandomForestClassifier

'''
    - utwór jest pobierany, następnie przetwarzany i dodwany do bazy danych, a potem 
        identyfikowany jako id bazie
    - najpierw skrócone FFT dl tych co mają wartości +- jak badana piosenka
    - potem wybieram z nich id
    - potem korelacja
    - potem przerabiam to na wiersz i bajlando, bajlando
'''
import struct
import numpy as np

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
            print(rms_id, main_id)
            rms, rms_len = db.execute_query(query.GET_RMS_BY_ID, params=(rms_id,))[0]
            corr = cc.calculate_correlation_from_different_length(main_rms, main_rms_len, rms, rms_len) #TODO: obliczanie korelacji na podstawie różnych długości
            rmss[rms_id] = corr
        return rmss

    def _remove_last_played(self, similar_ids: list) -> list:
        return similar_ids#TODO: FILTER LAST PLAYED SONGS FROM RECOMMENDATION TO PREVENT LOOPING

    def _transform_to_rows(self, ids: list, dicts: tuple) -> list:
        res_matrix = []
        for r_id in ids:
            res = list(db.execute_query(query.GET_FEATURES_BY_ID, params=(r_id,)))
            for dict in dicts:
                res.append(dict[r_id])
            res_matrix.append(res)
        return res_matrix #SKONCZE RANO, TAK MYSLE
                            #UPDATE 1:27 - zdecydowanie skończę rano xD
                            #UPDATE 1:56 - jednak dzisiaj xD

    def __init__(self):
        self._dataset = db.execute_query(query.GET_ALL_FROM_AVG_FFT)

    def process_to_datarow(self, main_id: int):
        similar_ids = self._filter_similar(main_id)
        not_last_played_ids = self._remove_last_played(similar_ids)
        fft_dict = self._fft_similar(main_id, not_last_played_ids)
        rms_dict = self._rms_similar(main_id, not_last_played_ids)
        hm_fft_dist = self._fft_similar(main_id, not_last_played_ids)
        rows = self._transform_to_rows(similar_ids, (fft_dict, rms_dict, hm_fft_dist))
        print(len(similar_ids))


rec = Recommender()
rec.process_to_datarow(666)
