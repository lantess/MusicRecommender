import os

MAIN_DIR = 'data'
FFT_DIR = os.path.join(MAIN_DIR, 'fft')
WAV_DIR = os.path.join(MAIN_DIR, 'wav')
NEW_WAV_DIR = os.path.join(MAIN_DIR, 'wav.new')

DB_FILE = os.path.join(MAIN_DIR, 'database.db')

FOURIER_SAMPLES = 20000
FFT_LEN = int(FOURIER_SAMPLES / 2 + 1)
MAG_BORDER = 0.1
FFT_AVG_RANGES = [(0, 60), (60, 250),
                  (250, 500), (500, 2000),
                  (2000, 4000), (4000, 6000),
                  (6000, FFT_LEN)]
FFT_AVG_LEN = len(FFT_AVG_RANGES)

CORR_MAX = 500.0
CORR_APPEND_PERCENT = 1.1
CORR_N_MIN = 1000
CORR_N_MAX = 1500

START_VOLUME = 75

class SQLQuery:
    INIT = ['CREATE TABLE IF NOT EXISTS song '
                '(id INTEGER PRIMARY KEY, '
                'filename TEXT NOT NULL UNIQUE, '
                'url TEXT);',
            'CREATE TABLE IF NOT EXISTS tempo '
                '(id INTEGER PRIMARY KEY, '
                'val REAL NOT NULL, '
                'FOREIGN KEY(id) REFERENCES song(id));',
            'CREATE TABLE IF NOT EXISTS fft '
                '(id INTEGER PRIMARY KEY, '
                'data BLOB NOT NULL, '
                'FOREIGN KEY(id) REFERENCES song(id));',
            'CREATE TABLE IF NOT EXISTS rms '
                '(id INTEGER PRIMARY KEY, '
                'data BLOB NOT NULL, '
                'len INTEGER NOT NULL, '
                'FOREIGN KEY(id) REFERENCES song(id));',
            'CREATE TABLE IF NOT EXISTS log '
                '(id INTEGER PRIMARY KEY, '
                'timestamp REAL NOT NULL, '
                'rate INTEGER, '
                'listening_time REAL NOT NULL, '
                'skipped INTEGER NOT NULL,'
                'language_code TEXT,'
                'FOREIGN KEY(id) REFERENCES song(id));',
            'CREATE TABLE IF NOT EXISTS zcr '
                '(id INTEGER PRIMARY KEY, '
                'val REAL NOT NULL, '
                'FOREIGN KEY(id) REFERENCES song(id));',
            'CREATE TABLE IF NOT EXISTS avg_range_fft '
                '(id INTEGER PRIMARY KEY, '
                'data BLOB NOT NULL);']

    GET_SONG_NAMES = 'SELECT filename FROM song;'
    GET_SONG_IDS_NOT_IN_FFT = 'SELECT id, filename FROM song ' \
                              'WHERE id NOT IN (SELECT id FROM fft);'
    GET_NOT_EXISTING_CORRELATIONS = 'SELECT DISTINCT f.id, s.id FROM song f ' \
                                    'INNER JOIN song s ON f.id!=s.id ' \
                                    'EXCEPT ' \
                                    'SELECT firstId, secondId FROM correlation ' \
                                    'EXCEPT ' \
                                    'SELECT secondId, firstId FROM correlation;'
    GET_NOT_EXISTING_HIGH_MAG_CORRELATIONS = 'SELECT DISTINCT f.id, s.id FROM song f ' \
                                    'INNER JOIN song s ON f.id!=s.id ' \
                                    'EXCEPT ' \
                                    'SELECT firstId, secondId FROM high_mag_correlation ' \
                                    'EXCEPT ' \
                                    'SELECT secondId, firstId FROM high_mag_correlation;'
    GET_FFT_BY_ID = 'SELECT data FROM fft WHERE id = ?;'
    GET_RMS_BY_ID = 'SELECT data, len FROM rms WHERE id = ?;'
    GET_ALL_SONG_ID = 'SELECT id FROM song;'
    GET_SONG_ID_BY_NAME = 'SELECT id FROM song WHERE filename = ?'
    GET_SONG_NAME_BY_ID = 'SELECT filename FROM song WHERE id = ?'
    GET_ALL_IDS = ['SELECT DISTINCT id FROM tempo;',
                   'SELECT DISTINCT id FROM fft;',
                   'SELECT DISTINCT id FROM rms;',
                   'SELECT DISTINCT id FROM zcr;',
                   'SELECT DISTINCT id FROM avg_range_fft']
    GET_ALL_FROM_AVG_FFT = 'SELECT id, data FROM avg_range_fft;'
    GET_FEATURES_BY_ID = 'SELECT tempo.val, zcr.val, log.timestamp, ' \
            'log.rate, log.listening_time, log.skipped, log.language_code ' \
            'FROM tempo INNER JOIN zcr ON tempo.id = zcr.id ' \
            'INNER JOIN log ON tempo.id = log.id ' \
            'WHERE tempo.id = ?;'
    GET_RANDOM_SONG = 'SELECT id, filename FROM song ORDER BY RANDOM() LIMIT 1;'
    GET_SONG_DURATION_BY_ID = 'SELECT duration FROM song WHERE id = ?;'

    ADD_SONG = 'INSERT INTO song (filename, duration) VALUES (?, ?);'
    ADD_RMS = 'INSERT INTO rms(id, data, len) VALUES (?, ?, ?);'
    ADD_CORRELATION = 'INSERT INTO correlation (firstId, secondId, val) VALUES (?, ?, ?);'
    ADD_HIGH_MAG_CORRELATION = 'INSERT INTO high_mag_correlation (firstId, secondId, val) ' \
                              'VALUES (?, ?, ?);'
    ADD_FFT = 'INSERT INTO fft (id, data) VALUES (?,?);'
    ADD_AVG_FFT = 'INSERT INTO avg_range_fft (id, data) VALUES (?,?);'
    ADD_TEMPO = 'INSERT INTO tempo (id, val) VALUES (?,?);'
    ADD_ZCR = 'INSERT INTO zcr (id, val) VALUES (?,?);'
    ADD_LISTEN_LOG = 'INSERT INTO log (id, timestamp, rate, listening_time, skipped, language_code)' \
                     ' VALUES (?,?,?,?,?,?);'

    DELETE_SONG = 'DELETE FROM song WHERE filename = ?;'
    DELETE_IDS = ['DELETE FROM tempo WHERE id = ?;',
                  'DELETE FROM fft WHERE id = ?;',
                  'DELETE FROM rms WHERE id = ?;',
                  'DELETE FROM zcr WHERE id = ?;',
                  'DELETE FROM avg_range_fft WHERE id = ?;']

