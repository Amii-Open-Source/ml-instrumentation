import pickle
import pytest
from ml_instrumentation.Collector import Collector
from ml_instrumentation.Sampler import Identity, Ignore
from ml_instrumentation.Writer import SqlPoint

@pytest.fixture
def collector():
    c = Collector(
        tmp_file=':memory:',
        config = {
            'm1': Identity(),
            'm2': Identity(),
        },
        default=Ignore()
    )
    yield c
    c.close()

def test_collector_setup1(collector):
    assert collector.keys() == set()
    assert collector.experiment_ids() == set()

    # non-existent metrics and/or experiment_ids should give empty lists
    assert collector.get('m1', 0) == []

def test_collector_rw1(collector):
    collector.set_experiment_id(0)
    collector.next_frame()

    collector.collect('m1', 0)
    assert collector.get('m1', 0) == [
        SqlPoint(frame=0, id=0, measurement=0)
    ]

    collector.next_frame()
    collector.collect('m1', 2)
    collector.collect('m2', 1)
    assert collector.get('m1', 0) == [
        SqlPoint(frame=0, id=0, measurement=0),
        SqlPoint(frame=1, id=0, measurement=2),
    ]

    assert collector.get('m2', 0) == [
        SqlPoint(frame=1, id=0, measurement=1),
    ]


def test_collector_serde(collector):
    collector.set_experiment_id(0)
    collector.next_frame()

    collector.collect('m1', 0)
    collector.next_frame()
    collector.collect('m1', 1)

    byts = pickle.dumps(collector)
    collector2: Collector = pickle.loads(byts)

    data1 = collector.get('m1', 0)
    data2 = collector2.get('m1', 0)
    assert data1 == data2 == [
        SqlPoint(frame=0, id=0, measurement=0),
        SqlPoint(frame=1, id=0, measurement=1),
    ]

    collector2.close()
