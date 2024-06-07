import pytest
from ml_instrumentation.Collector import Collector
from ml_instrumentation.Sampler import Identity, Ignore

@pytest.fixture
def collector():
    c = Collector(
        tmp_file=':memory:',
        config = {
            'm1': Identity()
        },
        default=Ignore()
    )
    yield c
    c.close()

def test_collector1(collector):
    assert collector.keys() == set()
    assert collector.experiment_ids() == set()

    # non-existent metrics and/or experiment_ids should give empty lists
    assert collector.get('m1', 0) == []
