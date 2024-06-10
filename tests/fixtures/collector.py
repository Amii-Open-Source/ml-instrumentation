import pytest
from ml_instrumentation.Collector import Collector
from ml_instrumentation.Sampler import Identity, Ignore

@pytest.fixture
def basic_collector():
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
