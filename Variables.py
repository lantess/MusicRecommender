import os

MAIN_DIR = 'data'
FFT_DIR = os.path.join(MAIN_DIR, 'fft')
WAV_DIR = os.path.join(MAIN_DIR, 'wav')
NEW_WAV_DIR = os.path.join(MAIN_DIR, 'wav.new')
FOURIER_SAMPLES = 20000
FFT_LEN = int(FOURIER_SAMPLES / 2 + 1)
