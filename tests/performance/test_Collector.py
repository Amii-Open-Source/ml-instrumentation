import pytest
from tests.fixtures.collector import basic_collector, disk_collector

from ml_instrumentation.Collector import Collector

@pytest.mark.parametrize('collector_fixture', [basic_collector, disk_collector])
def test_benchmark_write_path1(collector_fixture, request, benchmark):
    collector: Collector = request.getfixturevalue(collector_fixture.__name__)
    collector.set_experiment_id(0)

    def _inner():
        for i in range(1_000):
            collector.next_frame()
            collector.collect('m1', i)
            collector.collect('m2', f'test string {i}')

        # force any in-flight data to be sync'd
        # normally would close() the collector, but collector
        # will be reused for this test
        collector._writer.sync_now()

    benchmark(_inner)

@pytest.mark.parametrize('collector_fixture', [basic_collector, disk_collector])
def test_benchmark_read1(collector_fixture, request, benchmark):
    collector: Collector = request.getfixturevalue(collector_fixture.__name__)
    collector.set_experiment_id(0)
    for i in range(1_000):
        collector.next_frame()
        collector.collect('m1', i)
        collector.collect('m2', f'test string {i}')

    collector._writer.sync_now()

    def _inner():
        d = collector.get('m1', 0)
        assert len(d) == 1_000

        d = collector.get('m2', 0)
        assert len(d) == 1_000

    benchmark(_inner)
