def test_collector_setup1(basic_collector):
    assert basic_collector.keys() == set()
    assert basic_collector.experiment_ids() == set()

    # non-existent metrics and/or experiment_ids should give empty lists
    assert basic_collector.get('m1', 0) == []
