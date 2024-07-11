from functools import partial
import sqlite3
from ml_instrumentation.Writer import Point, SqlPoint, Writer
from multiprocessing.pool import Pool

def test_write1(writer):
    d = Point(
        metric='measurement-1',
        exp_id=0,
        frame=0,
        data=1.1,
    )
    writer.write(d)

    # should get back a list of datapoints for this measurement
    points = writer.read_metric('measurement-1')
    assert points == [
        SqlPoint(frame=0, id=0, measurement=1.1),
    ]

    d = Point(
        metric='measurement-1',
        exp_id=0,
        frame=1,
        data=2.2
    )
    writer.write(d)

    points = writer.read_metric('measurement-1')
    assert points == [
        SqlPoint(0, 0, 1.1),
        SqlPoint(1, 0, 2.2),
    ]

def test_write2(writer):
    for i in range(1_000):
        d = Point(
            metric='measurement-1',
            exp_id=0,
            frame=i,
            data=i * 1.1,
        )
        writer.write(d)

        if i % 3 == 0:
            d2 = d._replace(metric='measurement-2')
            writer.write(d2)

    points = writer.read_metric('measurement-1')
    assert len(points) == 1_000
    for i in range(1_000):
        assert points[i].frame == i
        assert points[i].measurement == i * 1.1

    points = writer.read_metric('measurement-2')
    assert len(points) == 334


def test_merge1(tmp_path):
    w1 = Writer(
        db_path=str(tmp_path / 'w1.db'),
    )

    w2 = Writer(
        db_path=':memory:',
    )

    for i in range(10):
        w1.write(Point(exp_id=0, metric='a', frame=i, data=i))
        w2.write(Point(exp_id=1, metric='a', frame=i, data=100+i))

    w1.merge(str(tmp_path / 'total.db'))
    w2.merge(str(tmp_path / 'total.db'))

    con = sqlite3.connect(tmp_path / 'total.db')
    cur = con.cursor()

    cur.execute('SELECT * FROM a WHERE id=0 ORDER BY frame')
    res = cur.fetchall()
    assert len(res) == 10
    assert [r[2] for r in res] == [i for i in range(10)]

    cur.execute('SELECT * FROM a WHERE id=1 ORDER BY frame')
    res = cur.fetchall()
    assert len(res) == 10
    assert [r[2] for r in res] == [100+i for i in range(10)]

    cur.execute('SELECT * FROM a')
    res = cur.fetchall()
    assert len(res) == 20

    w1.close()
    w2.close()


def test_merge_parallel1(tmp_path):
    pool = Pool(10)
    pool.map(partial(_test_merge_parallel1, tmp_path=tmp_path), range(20))

    con = sqlite3.connect(tmp_path / 'total.db')
    cur = con.cursor()

    for i in range(20):
        cur.execute(f'SELECT * FROM a WHERE id={i} ORDER BY frame')
        res = cur.fetchall()
        assert len(res) == 100
        assert [r[2] for r in res] == [2*j + i for j in range(100)]

        cur.execute(f'SELECT * FROM b where id={i} ORDER BY frame')
        res = cur.fetchall()
        assert len(res) == 100
        assert [r[2] for r in res] == [f'{j} - {i}' for j in range(100)]

    cur.execute('SELECT * FROM a')
    res = cur.fetchall()
    assert len(res) == 20 * 100


def _test_merge_parallel1(i: int, tmp_path):
    writer = Writer(db_path=str(tmp_path / f'w{i}.db'))

    for j in range(100):
        writer.write(Point(exp_id=i, metric='a', frame=j, data=2*j + i))
        writer.write(Point(exp_id=i, metric='b', frame=j, data=f'{j} - {i}'))

    writer.merge(str(tmp_path / 'total.db'))
