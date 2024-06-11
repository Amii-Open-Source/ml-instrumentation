import pickle
from ml_instrumentation.Collector import Collector
from ml_instrumentation.Writer import SqlPoint

def test_collector_rw1(basic_collector):
    basic_collector.set_experiment_id(0)
    basic_collector.next_frame()

    basic_collector.collect('m1', 0)
    assert basic_collector.get('m1', 0) == [
        SqlPoint(frame=0, id=0, measurement=0)
    ]

    basic_collector.next_frame()
    basic_collector.collect('m1', 2)
    basic_collector.collect('m2', 1)
    assert basic_collector.get('m1', 0) == [
        SqlPoint(frame=0, id=0, measurement=0),
        SqlPoint(frame=1, id=0, measurement=2),
    ]

    assert basic_collector.get('m2', 0) == [
        SqlPoint(frame=1, id=0, measurement=1),
    ]

def test_collector_rw_trailing_edge1(basic_collector):
    basic_collector.set_experiment_id(0)

    # note: no next_frame call here, it will go after
    basic_collector.collect('m1', 0)
    assert basic_collector.get('m1', 0) == [
        SqlPoint(frame=0, id=0, measurement=0),
    ]

    basic_collector.next_frame()

    # next_frame can also go in between collect and get
    basic_collector.collect('m1', 1)
    basic_collector.next_frame()
    assert basic_collector.get('m1', 0) == [
        SqlPoint(frame=0, id=0, measurement=0),
        SqlPoint(frame=1, id=0, measurement=1),
    ]


def test_collector_serde(basic_collector):
    basic_collector.set_experiment_id(0)
    basic_collector.next_frame()

    basic_collector.collect('m1', 0)
    basic_collector.next_frame()
    basic_collector.collect('m1', 1)

    byts = pickle.dumps(basic_collector)
    collector2: Collector = pickle.loads(byts)

    data1 = basic_collector.get('m1', 0)
    data2 = collector2.get('m1', 0)
    assert data1 == data2 == [
        SqlPoint(frame=0, id=0, measurement=0),
        SqlPoint(frame=1, id=0, measurement=1),
    ]

    collector2.close()
