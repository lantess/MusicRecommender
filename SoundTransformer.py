import os
import struct
import librosa
import scipy.fft as fft
import numpy as np

import SoundDictionary as sd
import CorrelationCalculator as cc
from WindowManager import WindowManager as wm

MAIN_DIR = 'data'
FFT_DIR = os.path.join(MAIN_DIR, 'fft')
WAV_DIR = os.path.join(MAIN_DIR, 'wav')
META_FILE = os.path.join(MAIN_DIR, 'meta.csv')
LEGEND_FILE = os.path.join(MAIN_DIR, 'matrix.legend')
MATRIX_FILE = os.path.join(MAIN_DIR, 'matrix.dat')
FOURIER_SAMPLES = 640000
FFT_LEN = int(FOURIER_SAMPLES / 2 + 1)

class SoundTransformer:
    def _load_metadata(self):
        if os.path.exists(META_FILE):
            with open(META_FILE, 'r') as file:
                for line in file:
                    name = line[:line.find(';')].strip()
                    sd.put(name)
                    data = sd.get(name)
                    line = line[line.find(';') + 1:]
                    data.fft_len = int(line[:line.find(';')])
                    line = line[line.find(';')+1:]
                    data.tempo = float(line[:line.find(';')])

    def _find_new_files(self):
        for file in os.listdir(WAV_DIR):
            if file.strip() not in sd.get_names():
                self._new_files.append(file.strip())

    def _fourier_new_files(self, window):
        i = 0
        max = len(self._new_files)
        window['-PERCENT-'].update(value='Fouriering sounds (' + str(int(i / max * 100)) + '%)')
        window['-PROGRESS-'].update(current_count=0, max=max)
        for filename in self._new_files:
            sd.put(filename)
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
            window['-PERCENT-'].update(value='Fouriering sounds (' + str(int(i / max * 100)) + '%)')
            window['-PROGRESS-'].update(current_count=i)

    def _add_to_metafile(self, window):
        i = 0
        max = len(sd.get_names())
        window['-PERCENT-'].update(value='Updating metadata (' + str(int(i / max * 100)) + '%)')
        window['-PROGRESS-'].update(current_count=i, max=max)
        open(META_FILE, 'w+').close()
        for name in sd.get_names():
            data = sd.get(name)
            out = open(META_FILE, 'a+')
            out.writelines([name, ';', str(data.fft_len), ';', str(data.tempo), ';\n'])
            out.close()
            i += 1
            window['-PERCENT-'].update(value='Updating metadata (' + str(int(i / max * 100)) + '%)')
            window['-PROGRESS-'].update(current_count=i)

    def _update_matrix_legend(self, window):
        window['-PERCENT-'].update(value='Updating matrix legend (0%)')
        window['-PROGRESS-'].update(current_count=0, max=1)
        for line in open(LEGEND_FILE, 'r'):
            self._matrix_filelist.append(line.replace('\n', ''))
        new_to_add = ['[NEW]'+s for s in sd.get_names() if s not in self._matrix_filelist]
        self._matrix_filelist = ['[DEL]'+s if s not in sd.get_names() else '[OLD]'+s for s in self._matrix_filelist]
        for line in new_to_add:
            self._matrix_filelist.append(line)
        window['-PERCENT-'].update(value='Updating matrix legend (100%)')
        window['-PROGRESS-'].update(current_count=1)

    def _load_matrix(self, window):
        window['-PERCENT-'].update(value='Loading matrix (0%)')
        window['-PROGRESS-'].update(current_count=0, max=1)
        dim = len([s for s in self._matrix_filelist if s.find('[NEW]') == -1])
        if dim == 0:
            return
        input = open(MATRIX_FILE, 'rb')
        raw_data = input.read()
        input.close()
        self._matrix = np.array(struct.unpack("f"*int(dim*dim), raw_data))
        cc.initialize(self._matrix, dim)
        window['-PERCENT-'].update(value='Loading matrix (100%)')
        window['-PROGRESS-'].update(current_count=1)

    def _compute_correlation(self, window):
        i = 0
        max = len(self._matrix_filelist)**2
        window['-PERCENT-'].update(value='Computing correlations (' + str(int(i / max * 100)) + '%)')
        window['-PROGRESS-'].update(current_count=i, max=max)
        for file in self._matrix_filelist:
            for com_file in self._matrix_filelist:
                if file != com_file:
                    cc.compute(file, com_file)
                    i += 1
                window['-PERCENT-'].update(value='Computing correlations (' + str(int(i / max * 100)) + '%)')
                window['-PROGRESS-'].update(current_count=i)

    def __init__(self):
        self._new_files = []
        self._matrix_filelist = []
        self._matrix = [[]]
        self._load_metadata()
        self._find_new_files()

    def update_soundbase(self, window):
        window.Finalize()
        self._fourier_new_files(window)
        self._add_to_metafile(window)
        self._update_matrix_legend(window)
        self._load_matrix(window)
        self._compute_correlation(window)
        window.close()
        print('DEBUG: soundbase updated.')

    def has_new_files(self):
        return len(self._new_files) > 0