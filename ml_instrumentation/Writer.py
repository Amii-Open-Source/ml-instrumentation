import os
import time
import sqlite3
import logging
from collections import defaultdict
from typing import Any, Dict, List, NamedTuple, Set
from concurrent.futures import ThreadPoolExecutor, Future

logger = logging.getLogger('ml-instrumentation')

class Point(NamedTuple):
    exp_id: int | str
    metric: str
    frame: int
    data: Any

class SqlPoint(NamedTuple):
    frame: int
    id: int | str
    measurement: Any

class Writer:
    def __init__(
        self,
        db_path: str,
        low_watermark: int = 64,
        high_watermark: int = 256,
    ):
        # ------------
        # -- config --
        # ------------
        self._db_path = db_path

        self._lw = low_watermark
        self._hw = high_watermark

        # ---------------
        # -- externals --
        # ---------------
        self._exec = ThreadPoolExecutor(max_workers=1)
        self._con = sqlite3.connect(self._db_path, check_same_thread=False)
        self._con.row_factory = row_factory

        self._write_future: Future | None = None

        # -----------
        # -- state --
        # -----------
        self._i = 0
        self._buffer: Dict[str, Dict[int, Point]] = defaultdict(dict)
        self._built: Set[str] = set()

        self._avg_write_time = -1
        self._last_write_time = -1

        # -------------------------
        # -- load existing state --
        # -------------------------
        self._init_db()

    # ------------
    # -- IO API --
    # ------------
    def write(self, d: Point):
        self._buffer[d.metric][self._i] = d
        self._i += 1

        if self._i > self._hw:
            assert self._write_future is not None
            self._write_future.result()
            logger.warning(f'Buffer reached high watermark. (last write: {self._last_write_time}s, avg write: {self._avg_write_time}s)')
            self.sync()

        elif self._i > self._lw:
            self.sync()

    def sync(self):
        if self._write_future is not None and not self._write_future.done():
            return

        data = self._buffer
        self._buffer = defaultdict(dict)
        self._i = 0
        self._write_future = self._exec.submit(self._sync_async, data)

    def sync_now(self):
        if self._write_future is not None:
            self._write_future.result()

        self.sync()
        assert self._write_future is not None
        self._write_future.result()

    def read_metric(self, metric: str, exp_id: int | str | None = None) -> List[SqlPoint]:
        self.sync_now()

        cond = ''
        if exp_id is not None:
            cond = f'WHERE id={maybe_quote(exp_id)}'

        cur = self._con.cursor()
        cur = cur.execute(f'SELECT * FROM "{metric}" {cond}')
        res = cur.fetchall()
        return res

    def close(self):
        self.sync_now()
        self._con.close()

    # -----------------
    # -- Utility API --
    # -----------------
    def metrics(self):
        buffered_keys = set(self._buffer.keys())
        return buffered_keys | self._built

    # -------------------
    # -- Backend logic --
    # -------------------
    def _sync_async(self, d: Dict[str, Dict[int, Point]]):
        sql_d = {}
        for m, sub in d.items():
            sql_d[m] = [
                SqlPoint(p.frame, p.exp_id, p.data) for p in sub.values()
            ]

        cur = self._con.cursor()
        start = time.perf_counter()

        for m in sql_d:
            self._setup_table(cur, m)
            self._write_many(cur, m, sql_d[m])

        self._con.commit()
        cur.close()
        elapsed = time.perf_counter() - start

        self._last_write_time = elapsed
        if self._avg_write_time < 0:
            self._avg_write_time = elapsed
        else:
            self._avg_write_time = 0.9 * self._avg_write_time + 0.1 * elapsed

    def _init_db(self):
        if not os.path.exists(self._db_path):
            return

        cur = self._con.cursor()
        res = cur.execute("SELECT name FROM sqlite_master")
        tables = set(r[0] for r in res.fetchall())
        self._built |= tables

    # ---------------------
    # -- utility methods --
    # ---------------------
    def _setup_table(self, cur: sqlite3.Cursor, name: str):
        if name in self._built:
            return

        cur.execute(f'CREATE TABLE "{name}"(frame INTEGER PRIMARY KEY ASC, id, measurement)')
        self._built.add(name)

    def _write_many(self, cur: sqlite3.Cursor, m: str, d: List[SqlPoint]):
        cur.executemany(f'INSERT INTO "{m}" (frame, id, measurement) VALUES (?,?,?)', d)


def row_factory(cur, d):
    return SqlPoint(*d)

def maybe_quote(x: int | str):
    if isinstance(x, str):
        return f'"{x}"'

    return x
