import os

MAIN_DIR = 'data'
FFT_DIR = os.path.join(MAIN_DIR, 'fft')
WAV_DIR = os.path.join(MAIN_DIR, 'wav')
NEW_WAV_DIR = os.path.join(MAIN_DIR, 'wav.new')

DB_FILE = os.path.join(MAIN_DIR, 'database.db')

FOURIER_SAMPLES = 20000
FFT_LEN = int(FOURIER_SAMPLES / 2 + 1)


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
            'CREATE TABLE IF NOT EXISTS correlation '
                '(firstId INTEGER, '
                'secondId INTEGER, '
                'val REAL NOT NULL, '
                'FOREIGN KEY(firstId) REFERENCES song(id), '
                'FOREIGN KEY(secondId) REFERENCES song(id), '
                'PRIMARY KEY(firstId, secondId));',
            'CREATE TABLE IF NOT EXISTS log '
                '(id INTEGER PRIMARY KEY, '
                'timestamp INTEGER, '
                'rate INTEGER, '
                'FOREIGN KEY(id) REFERENCES song(id));',
            'CREATE TABLE IF NOT EXISTS zcr '
                '(id INTEGER PRIMARY KEY, '
                'val REAL NOT NULL, '
                'FOREIGN KEY(id) REFERENCES song(id));']

    GET_SONG_NAMES = 'SELECT filename FROM song;'
    GET_SONG_IDS_NOT_IN_FFT = 'SELECT id, filename FROM song ' \
                              'WHERE id NOT IN (SELECT id FROM fft);'
    GET_NOT_EXISTING_CORRELATIONS = 'SELECT DISTINCT f.id, s.id FROM song f ' \
                                    'INNER JOIN song s ON f.id!=s.id ' \
                                    'EXCEPT ' \
                                    'SELECT firstId, secondId FROM correlation ' \
                                    'EXCEPT ' \
                                    'SELECT secondId, firstId FROM correlation;'
    GET_FFT_BY_ID = 'SELECT data FROM fft WHERE id IN (?, ?);'
    GET_SONG_ID_BY_NAME = 'SELECT id FROM song WHERE filename = ?'

    ADD_SONG = 'INSERT INTO song (filename) VALUES (?);'
    ADD_RMS = 'INSERT INTO rms(id, data, len) VALUES (?, ?, ?);'
    ADD_CORELATION = 'INSERT INTO correlation (firstId, secondId, val) VALUES (?, ?, ?);'
    ADD_FFT = 'INSERT INTO fft (id, data) VALUES (?,?);'
    ADD_TEMPO = 'INSERT INTO tempo (id, val) VALUES (?,?);'
    ADD_ZCR = 'INSERT INTO zcr (id, val) VALUES (?,?);'
    ADD_LISTEN_LOG = 'INSERT INTO log (id, timestamp, rate) VALUES (?,?,?);'
