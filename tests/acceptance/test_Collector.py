import pickle
import pytest

from ml_instrumentation.Collector import Collector
from tests.fixtures.collector import basic_collector, disk_collector, simulate_run, SimMetric

"""
User should be able to:
1. Build a collector object
2. Add data into the collector (possibly sparsely)
3. Interrupt the program flow and serialize the collector to disk
4. Load the collector from disk
5. Continue execution of the code and data collection
6. Load all results of collection for later manipulation

The above should be able to run with in-memory collection and disk-backed collection.
"""
@pytest.mark.parametrize('collector_fixture', [basic_collector, disk_collector])
def test_collector1(collector_fixture, tmp_path, request):
    collector: Collector = request.getfixturevalue(collector_fixture.__name__)
    collector.set_experiment_id(0)

    metrics = [
        SimMetric(
            metric='m1',
            pred=lambda i: i % 100 == 0,
            value=lambda i: i,
        ),
        SimMetric(
            metric='m2',
            pred=lambda i: i % 33 == 0,
            value=lambda i: f'test string {i}',
        )
    ]

    # execute the first half of the program
    expected_1 = simulate_run(
        collector,
        start=0, end=50_000,
        metrics=metrics,
    )

    # serialize/deserialize
    with open(tmp_path / 'chk.pkl', 'wb') as f:
        pickle.dump(collector, f)

    del collector

    with open(tmp_path / 'chk.pkl', 'rb') as f:
        collector = pickle.load(f)

    # execute the second half of the program
    expected_2 = simulate_run(
        collector,
        start=50_000, end=100_000,
        metrics=metrics,
    )

    # load all data for evaluation
    a = collector.get('m1', experiment_id=0)
    assert len(a) == 1_000

    expected_a = expected_1['m1'] + expected_2['m1']
    assert a == expected_a

    b = collector.get('m2', experiment_id=0)
    assert len(b) == 3_031

    expected_b = expected_1['m2'] + expected_2['m2']
    assert b == expected_b
