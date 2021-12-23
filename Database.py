import sqlite3
from sqlite3 import Error as sqlError
import os

DATABASE_FILE = 'data/database.db'
QUERY_DIR = 'data/sql'
INIT_QUERY = 'init.sql'

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
        print(e)
    finally:
        if conn:
            conn.close()
        return res

def init():
    queries = _load_sql_query(INIT_QUERY)
    for query in queries.split(';'):
        _execute_query(query+';')
