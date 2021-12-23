import sqlite3
from sqlite3 import Error as sqlError
import os

DATABASE_FILE = 'data/database.db'
QUERY_DIR = 'data/sql'

def _load_sql_query(query_filename: str) -> str:
    try:
        res = ''
        with open(os.path.join(QUERY_DIR, query_filename), 'r') as file:
             for line in file:
                 res += line
        return res
    except FileNotFoundError:
        return ""

def init():
    print(_load_sql_query('init.sql'))
    pass