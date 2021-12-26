import os
import struct
import librosa
import scipy.fft as fft
import numpy as np

from WindowManager import WindowManager as wm
import Database as db
import CorrelationCalculator as cc


    #TODO: usuwanie z bazy nieistniejących piosenek
    #TODO: updejt przy każdym braku, nie tylko nowych plikach
    #TODO: odtwarzanie muzyki
    #TODO: historia odsłuchów
    #TODO: kompresja wavów na mp3
    #TODO: siec neuronowa klasyfikująca
    #TODO: przebudować bazę danych
    #TODO: transformata na poszczególnych częstotliwościach (dla różnych rodzajów dźwięków)
    #TODO: transformata na >10% mocy
    #TODO: MFCC (?)
    #TODO: RMS (librosa)
    #TODO: zero-crossing-rate (librosa)
    #TODO: frequency weighting
    #TODO: odtwarzanie muzyki z youtube'a


MAIN_DIR = 'data'
FFT_DIR = os.path.join(MAIN_DIR, 'fft')
WAV_DIR = os.path.join(MAIN_DIR, 'wav')
FOURIER_SAMPLES = 640000
FFT_LEN = int(FOURIER_SAMPLES / 2 + 1)

class SoundTransformer:

    def _find_new_files(self):
        db.init()
        old_files = [x[0] for x in db.get_sound_names()]
        new_files = [x for x in os.listdir(WAV_DIR) if x not in old_files]
        if len(new_files) > 0:
            self._new_files = True
        for file in new_files:
            db.add_new_sound(file)

    def _fourier_new_files(self, window):
        new_files = db.get_not_ffted_sound()
        i = 0
        max = 1 if len(new_files) == 0 else len(new_files)
        wm.updateProgressWindow(window, 'Fouriering sounds', i, max)
        for id, filename in new_files:
            file = os.path.join(WAV_DIR, filename)
            y, sr = librosa.load(file, sr=None)
            yf = np.abs(fft.rfft(y, n=FOURIER_SAMPLES, workers=os.cpu_count()))
            data = struct.pack('f'*len(yf), *yf)
            tempo = librosa.beat.tempo(sr=sr,
                                       onset_envelope=librosa.onset.onset_strength(y, sr=sr))
            db.add_fft_and_tempo(id, tempo, data)
            i += 1
            wm.updateProgressWindow(window, 'Fouriering sounds', i, max)

    def _load_matrix(self, window):
        pair_list = db.get_new_id_pairs()
        i = 0
        max = 1 if len(pair_list) == 0 else len(pair_list)
        wm.updateProgressWindow(window, 'Updating matrix', i, max)
        for pair in pair_list:
            data = db.get_data_from_pair(pair)
            value = cc.calculate_correlation(data[0][0], data[1][0])
            db.add_correlation(pair[0], pair[1], value)
            i += 1
            wm.updateProgressWindow(window, 'Updating matrix', i, max)
    def _compute_correlation(self, window):
        pass

    def __init__(self):
        self._new_files = True #TODO: Zmienić na False przy ostatecznych testach
        self._find_new_files()

    def update_soundbase(self, window):
        window.Finalize()
        self._fourier_new_files(window)
        self._load_matrix(window)
        self._compute_correlation(window)
        window.close()

    def has_new_files(self):
        return self._new_files