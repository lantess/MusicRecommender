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

    def _correlate_similar(self, main_id: int, similar_ids: list) -> list:
        main_fft = db.execute_query(query.GET_FFT_BY_ID, params=(main_id,))[0][0]
        ffts = {}
        for fft_id in similar_ids:
            fft = db.execute_query(query.GET_FFT_BY_ID, params=(fft_id,))[0][0]
            corr = cc.calculate_correlation(main_fft, fft)
            ffts[fft_id] = corr #TODO: filtrowanie podobnych
        return ffts

    def _remove_last_played(self, similar_ids: list) -> list:
        return similar_ids#TODO: FILTER LAST PLAYED SONGS FROM RECOMMENDATION TO PREVENT LOOPING

    def _transform_to_rows(self, similar_ids: list) -> list:
        res_matrix = []
        for s_id in similar_ids:
            res = [s_id]
        return similar_ids #SKONCZE RANO, TAK MYSLE

    def __init__(self):
        self._dataset = db.execute_query(query.GET_ALL_FROM_AVG_FFT)

    def process_to_datarow(self, main_id: int):
        similar_ids = self._filter_similar(main_id)
        corr_ids = self._correlate_similar(main_id, similar_ids)
        not_last_played_ids = self._remove_last_played(corr_ids)
        #TODO: rms
        #TODO: high mag correlation
        rows = self._transform_to_rows(not_last_played_ids)


rec = Recommender()
rec.process_to_datarow(666)
