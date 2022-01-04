import os
import struct
import librosa
import numpy as np
import threading

from WindowManager import WindowManager as wm
import Database as db
import CorrelationCalculator as cc
import Variables as var
from Variables import SQLQuery as query


class SoundTransformer:

    def _find_new_files(self):
        db.execute_queries_with_no_params(query.INIT)
        in_dir_files = os.listdir(var.WAV_DIR)
        old_files = [x[0] for x in db.execute_query(query.GET_SONG_NAMES)]
        new_files = [x for x in in_dir_files if x not in old_files]
        del_files = [x for x in old_files if x not in in_dir_files]
        if len(new_files) > 0:
            self._new_files = True
        for file in new_files:
            db.execute_query(query.ADD_SONG, params=(file,))
        for file in del_files:
            print('DEL:', file)
            db.execute_query(query.DELETE_SONG, params=(file,))

    def _find_analyse_absence(self):
        ids = [x[0] for x in db.execute_query(query.GET_ALL_SONG_ID)]
        for q in query.GET_ALL_IDS:
            data = db.execute_query(q)
            data = [x for x in ids if x not in data]
            if len(data) > 0:
                self._new_files = True
                return

    def _fft(self, y, sr) -> bytes:
        ff = np.abs(librosa.stft(y, n_fft=int(sr)))
        res = [np.average(x) for x in ff]
        fft_data = struct.pack('f' * len(res), *res)
        return fft_data

    def _rms(self, y, sr) -> (bytes, int):
        rms = librosa.feature.rms(y=y, frame_length=sr)[0]
        rms_data = struct.pack('f' * len(rms), *rms)
        return rms_data, len(rms)

    def _zcr(self, y):
        zcr = librosa.feature.zero_crossing_rate(y + 0.0001)
        return np.average(zcr[0])

    def _range_fft(self, fft_data, length) -> bytes:
        data = list(struct.unpack('f' * length, fft_data))
        res = []
        for r in var.FFT_AVG_RANGES:
            res.append(np.average(data[r[0]:r[1]]))
        return struct.pack('f' * var.FFT_AVG_LEN, *res)

    def _analyze_thread(self, id, filename):
        file = os.path.join(var.WAV_DIR, filename)
        y, sr = librosa.load(file, sr=var.FOURIER_SAMPLES)

        fft_data = self._fft(y, sr)
        db.execute_query(query.ADD_FFT, params=(id, fft_data))

        fft_avg = self._range_fft(fft_data, var.FFT_LEN)
        db.execute_query(query.ADD_AVG_FFT, params=(id, fft_avg))

        tempo = librosa.beat.tempo(sr=sr, onset_envelope=librosa.onset.onset_strength(y, sr=sr))
        db.execute_query(query.ADD_TEMPO, params=(id, tempo))

        rms, length = self._rms(y, sr)
        db.execute_query(query.ADD_RMS, params=(id, rms, length))

        zcr = self._zcr(y)
        db.execute_query(query.ADD_ZCR, params=(id, zcr))

        self._i += 1

    def _analyze_new_files(self, window):
        new_files = db.execute_query(query.GET_SONG_IDS_NOT_IN_FFT)
        self._i = 0
        max = 1 if len(new_files) == 0 else len(new_files)
        wm.updateProgressWindow(window, 'Fouriering sounds', self._i, max)
        for id, filename in new_files:
            thread = threading.Thread(target=self._analyze_thread,
                                      args=(id, filename))
            thread.start()
            while thread.is_alive():
                wm.updateProgressWindow(window, 'Fouriering sounds', self._i, max)


    def __init__(self):
        self._new_files = False
        self._i = 0
        self._find_new_files()
        self._find_analyse_absence()

    def update_soundbase(self, window=None):
        if window is not None:
            window.Finalize()
        self._analyze_new_files(window)
        if window is not None:
            window.close()

    def has_new_files(self):
        return self._new_files
