import os
import struct
import librosa
import scipy.fft as fft
import numpy as np

import SoundDictionary as sd
import CorrelationCalculator as cc
from WindowManager import WindowManager as wm
import Database as db

MAIN_DIR = 'data'
FFT_DIR = os.path.join(MAIN_DIR, 'fft')
WAV_DIR = os.path.join(MAIN_DIR, 'wav')
META_FILE = os.path.join(MAIN_DIR, 'meta.csv')
LEGEND_FILE = os.path.join(MAIN_DIR, 'matrix.legend')
MATRIX_FILE = os.path.join(MAIN_DIR, 'matrix.dat')
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
            yf = np.abs(fft.rfft(y, n=FOURIER_SAMPLES))
            data = struct.pack('f'*len(yf), *yf)
            tempo = librosa.beat.tempo(sr=sr,
                                       onset_envelope=librosa.onset.onset_strength(y, sr=sr))
            db.add_fft_and_tempo(id, tempo, data)
            i += 1
            wm.updateProgressWindow(window, 'Fouriering sounds', i, max)
        ''' sd.put(filename)
            file = os.path.join(WAV_DIR, filename)
            y, sr = librosa.load(file, sr=None)
            yf = np.abs(fft.rfft(y, n=FOURIER_SAMPLES))
            out_file = os.path.join(FFT_DIR, filename.replace('.wav', '.bin'))
            out = open(out_file, "wb+")
            for cell in yf:
                out.write(struct.pack("f", cell))
            out.close()
            tempo = librosa.beat.tempo(sr=sr,
                                       onset_envelope=librosa.onset.onset_strength(y, sr=sr))
            filedata = sd.get(filename)
            filedata.tempo = tempo[0]
            filedata.fft_len = len(yf)
            i+=1
            wm.updateProgressWindow(window, 'Fouriering sounds', i, max)'''

    def _add_to_metafile(self, window):
        i = 0
        max = len(sd.get_names())
        wm.updateProgressWindow(window, 'Updating metadata', i, max)
        open(META_FILE, 'w+').close()
        for name in sd.get_names():
            data = sd.get(name)
            out = open(META_FILE, 'a+')
            out.writelines([name, ';', str(data.fft_len), ';', str(data.tempo), ';\n'])
            out.close()
            i += 1
            wm.updateProgressWindow(window, 'Updating metadata', i, max)

    def _update_matrix_legend(self, window):
        wm.updateProgressWindow(window, 'Updating matrix legend', 0, 1)
        for line in open(LEGEND_FILE, 'r'):
            self._matrix_filelist.append(line.replace('\n', ''))
        new_to_add = ['[NEW]'+s for s in sd.get_names() if s not in self._matrix_filelist]
        self._matrix_filelist = ['[DEL]'+s if s not in sd.get_names() else '[OLD]'+s for s in self._matrix_filelist]
        for line in new_to_add:
            self._matrix_filelist.append(line)
        wm.updateProgressWindow(window, 'Updating matrix legend', 1, 1)

    def _load_matrix(self, window):
        wm.updateProgressWindow(window, 'Loading matrix', 0, 1)
        dim = len([s for s in self._matrix_filelist if s.find('[NEW]') == -1])
        if dim == 0:
            return
        input = open(MATRIX_FILE, 'rb')
        raw_data = input.read()
        input.close()
        self._matrix = np.array(struct.unpack("f"*int(dim*dim), raw_data))
        cc.initialize(self._matrix, dim)
        wm.updateProgressWindow(window, 'Loading matrix', 1, 1)

    def _compute_correlation(self, window):
        i = 0
        max = len(self._matrix_filelist)**2
        wm.updateProgressWindow(window, 'Computing correlations', i, max)
        for file in self._matrix_filelist:
            for com_file in self._matrix_filelist:
                if file != com_file:
                    cc.compute(file, com_file)
                    i += 1
                wm.updateProgressWindow(window, 'Computing correlations', i, max)

    def __init__(self):
        self._new_files = True #TODO: Zmienić na False przy ostatecznych testach
        self._matrix_filelist = []
        self._matrix = [[]]
        self._find_new_files()

    def update_soundbase(self, window):
        window.Finalize()
        #self._fourier_new_files(window)
        #self._add_to_metafile(window)
        #self._update_matrix_legend(window)
        #self._load_matrix(window)
        #self._compute_correlation(window)
        window.close()
        print('DEBUG: soundbase updated.')

    def has_new_files(self):
        return self._new_files