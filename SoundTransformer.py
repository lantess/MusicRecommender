import os
import struct
import librosa
import numpy as np

from WindowManager import WindowManager as wm
import Database as db
import CorrelationCalculator as cc
import Variables as var
from Variables import SQLQuery as query

class SoundTransformer:

    def _find_new_files(self):
        db.execute_queries_with_no_params(query.INIT)
        old_files = [x[0] for x in db.execute_query(query.GET_SONG_NAMES)]
        new_files = [x for x in os.listdir(var.WAV_DIR) if x not in old_files]
        if len(new_files) > 0:
            self._new_files = True
        for file in new_files:
            db.execute_query(query.ADD_SONG, params=(file,))

    def _fft(self, y, sr) -> list:
        ff = np.abs(librosa.stft(y, n_fft=int(sr)))
        res = [np.average(x) for x in ff]
        return res

    def _rms(self, y, sr) -> list:
        rms = librosa.feature.rms(y=y, frame_length=sr)[0]
        return rms

    def _analyze_new_files(self, window):
        new_files = db.execute_query(query.GET_SONG_IDS_NOT_IN_FFT)
        i = 0
        max = 1 if len(new_files) == 0 else len(new_files)
        wm.updateProgressWindow(window, 'Fouriering sounds', i, max)
        for id, filename in new_files:
            file = os.path.join(var.WAV_DIR, filename)
            y, sr = librosa.load(file, sr=var.FOURIER_SAMPLES)
            yf = self._fft(y, sr)
            fft_data = struct.pack('f'*len(yf), *yf)
            tempo = librosa.beat.tempo(sr=sr,
                                       onset_envelope=librosa.onset.onset_strength(y, sr=sr))
            rms = self._rms(y, sr)
            rms_data = struct.pack('f'*len(rms), *rms)
            db.execute_query(query.ADD_FFT, params=(id, fft_data))
            db.execute_query(query.ADD_TEMPO, params=(id, tempo))
            db.execute_query(query.ADD_RMS, params=(id, rms_data, len(rms)))
            i += 1
            wm.updateProgressWindow(window, 'Fouriering sounds', i, max)

    def _load_matrix(self, window):
        pair_list = db.execute_query(query.GET_NOT_EXISTING_CORRELATIONS)
        i = 0
        max = 1 if len(pair_list) == 0 else len(pair_list)
        wm.updateProgressWindow(window, 'Updating matrix', i, max)
        for pair in pair_list:
            data = db.execute_query(query.GET_FFT_BY_ID, params=pair)
            value = cc.calculate_correlation(data[0][0], data[1][0])
            db.execute_query(query.ADD_CORELATION, params=(pair[0], pair[1], value))
            i += 1
            wm.updateProgressWindow(window, 'Updating matrix', i, max)

    def __init__(self):
        self._new_files = True #TODO: Zmienić na False przy ostatecznych testach
        self._find_new_files()

    def update_soundbase(self, window):
        window.Finalize()
        self._analyze_new_files(window)
        self._load_matrix(window)
        window.close()

    def has_new_files(self):
        return self._new_files