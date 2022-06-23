import sqlite3
from sqlite3 import Error as sqlError
import Variables as var

def execute_query(query: str, params: tuple = None) -> list:
    conn = None
    res = []
    try:
        conn = sqlite3.connect(var.DB_FILE)
        cur = conn.cursor()
        if params is None:
            cur.execute(query)
        else:
            cur.execute(query, params)
        conn.commit()
        res = cur.fetchall()
    except sqlError as e:
        print(e, ' --- ', query)
    finally:
        if conn:
            conn.close()
        return res


def execute_queries_with_no_params(queries_list: list):
    for query in queries_list:
        execute_query(query)
