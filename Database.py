import sqlite3
from sqlite3 import Error as sqlError
import os

DATABASE_FILE = 'data/database.db'
QUERY_DIR = 'data/sql'
INIT_QUERY = 'init.sql'
GET_SOUND_NAMES = 'get_sound_names.sql'
ADD_SOUND_NAME = 'add_sound_name.sql'
ADD_FFT_AND_TEMPO = 'add_fft_and_tempo.sql'
NOT_FFTED_SOUND = 'get_not_ffted_sound.sql'
NEW_ID_PAIRS = 'not_existings_correlations.sql'
FFT_BY_ID = 'get_fft_by_id.sql'
NEW_CORRELATION = 'add_correlation.sql'

def _load_sql_query(query_filename: str) -> str:
    try:
        res = ''
        with open(os.path.join(QUERY_DIR, query_filename), 'r') as file:
             for line in file:
                 res += line
        return res
    except FileNotFoundError:
        return ""

def _execute_query(query: str):
    conn = None
    res = []
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        res = cur.fetchall()
    except sqlError as e:
        print(e, ' --- ', query)
    finally:
        if conn:
            conn.close()
        return res

def _execute_query_with_param(query: str, param):
    conn = None
    res = []
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        cur.execute(query, param)
        res = cur.fetchall()
        conn.commit()
    except BaseException as e:
        print(e, ' --- ', query)
    finally:
        if conn:
            conn.close()
        return res

def init():
    for query in _load_sql_query(INIT_QUERY).split(';'):
        _execute_query(query+';')


def get_sound_names() -> list:
    query = _load_sql_query(GET_SOUND_NAMES)
    return _execute_query(query)

def get_not_ffted_sound() -> list:
    query = _load_sql_query(NOT_FFTED_SOUND)
    return [x[0] for x in _execute_query(query)]

def add_new_sound(filename):
    query = _load_sql_query(ADD_SOUND_NAME)
    _execute_query_with_param(query, param=(filename,))

def add_fft_and_tempo(id, tempo, fft):
    queries = _load_sql_query(ADD_FFT_AND_TEMPO).split(';')
    _execute_query_with_param(queries[0] + ';', param=(id, tempo))
    _execute_query_with_param(queries[1] + ';', param=(id, fft))

def get_new_id_pairs() -> list:
    query = _load_sql_query(NEW_ID_PAIRS)
    return _execute_query(query)

def get_data_from_pair(pair: tuple) -> list:
    query = _load_sql_query(FFT_BY_ID)
    res = _execute_query_with_param(query, pair)
    return res

def add_correlation(first: int, second: int, value: float):
    query = _load_sql_query(NEW_CORRELATION)
    _execute_query_with_param(query, (first, second, value))
