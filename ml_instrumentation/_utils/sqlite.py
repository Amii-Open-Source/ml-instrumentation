from sqlite3 import Cursor
from typing import Set

def get_tables(cur: Cursor) -> Set[str]:
    cur.row_factory = None
    res = cur.execute("SELECT name FROM sqlite_master")
    return set(r[0] for r in res.fetchall())
