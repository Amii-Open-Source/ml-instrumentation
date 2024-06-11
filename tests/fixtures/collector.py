import pytest
from collections import defaultdict
from typing import Any, Callable, Dict, List, NamedTuple, Sequence
from ml_instrumentation.Collector import Collector
from ml_instrumentation.Sampler import Identity, Ignore
from ml_instrumentation.Writer import SqlPoint

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


@pytest.fixture
def disk_collector(tmp_path):
    c = Collector(
        tmp_file=str(tmp_path / 'test.db'),
        config = {
            'm1': Identity(),
            'm2': Identity(),
        },
        default=Ignore()
    )
    yield c
    c.close()

# ----------------------
# -- Simulation Tools --
# ----------------------
class SimMetric(NamedTuple):
    metric: str
    pred: Callable[[int], bool]
    value: Callable[[int], Any]


def simulate_run(collector: Collector, start: int, end: int, metrics: Sequence[SimMetric]):
    expected: Dict[str, List[SqlPoint]] = defaultdict(list)

    exp_id = collector.get_current_experiment_id()

    for i in range(start, end):
        collector.next_frame()

        for m in metrics:
            if m.pred(i):
                v = m.value(i)
                collector.collect(m.metric, v)
                expected[m.metric].append(SqlPoint(frame=i, id=exp_id, measurement=v))

    return expected
