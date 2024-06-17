window.BENCHMARK_DATA = {
  "lastUpdate": 1718649879413,
  "repoUrl": "https://github.com/Amii-Open-Source/ml-instrumentation",
  "entries": {
    "Python Benchmark with pytest-benchmark": [
      {
        "commit": {
          "author": {
            "email": "andnpatterson@gmail.com",
            "name": "Andy Patterson",
            "username": "andnp"
          },
          "committer": {
            "email": "160795226+andy-amii@users.noreply.github.com",
            "name": "andy-amii",
            "username": "andy-amii"
          },
          "distinct": true,
          "id": "5049014b59c554c6ed7c082080d20bcdd5c36098",
          "message": "ci: push benchmarks into gh-pages",
          "timestamp": "2024-06-13T11:02:15-06:00",
          "tree_id": "8b34c77fa70098559431374bb1b8aeb80ea12ce7",
          "url": "https://github.com/Amii-Open-Source/ml-instrumentation/commit/5049014b59c554c6ed7c082080d20bcdd5c36098"
        },
        "date": 1718298161125,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_write_path1[basic_collector]",
            "value": 144.98093884797143,
            "unit": "iter/sec",
            "range": "stddev: 0.0014347900758641164",
            "extra": "mean: 6.897458437957908 msec\nrounds: 137"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_write_path1[disk_collector]",
            "value": 104.64880821124693,
            "unit": "iter/sec",
            "range": "stddev: 0.001252917912611502",
            "extra": "mean: 9.55577055384494 msec\nrounds: 65"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_read1[basic_collector]",
            "value": 369.06837517281303,
            "unit": "iter/sec",
            "range": "stddev: 0.0005970104384548531",
            "extra": "mean: 2.709525029154175 msec\nrounds: 343"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_read1[disk_collector]",
            "value": 362.963654617666,
            "unit": "iter/sec",
            "range": "stddev: 0.0007938075758886335",
            "extra": "mean: 2.755096790760957 msec\nrounds: 368"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "andnpatterson@gmail.com",
            "name": "Andy Patterson",
            "username": "andnp"
          },
          "committer": {
            "email": "160795226+andy-amii@users.noreply.github.com",
            "name": "andy-amii",
            "username": "andy-amii"
          },
          "distinct": true,
          "id": "8439febe6f545365174201861dc2084d6ec50b15",
          "message": "chore: use numpy 2.0 migration ruff rule",
          "timestamp": "2024-06-17T12:44:14-06:00",
          "tree_id": "033002aba43a7fe9739deef8d97dfd0cf54ed885",
          "url": "https://github.com/Amii-Open-Source/ml-instrumentation/commit/8439febe6f545365174201861dc2084d6ec50b15"
        },
        "date": 1718649879011,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_write_path1[basic_collector]",
            "value": 143.16270968817219,
            "unit": "iter/sec",
            "range": "stddev: 0.0017551819055799803",
            "extra": "mean: 6.985059183205848 msec\nrounds: 131"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_write_path1[disk_collector]",
            "value": 96.77237952375211,
            "unit": "iter/sec",
            "range": "stddev: 0.002402241308949498",
            "extra": "mean: 10.333527034483605 msec\nrounds: 58"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_read1[basic_collector]",
            "value": 364.10920336819726,
            "unit": "iter/sec",
            "range": "stddev: 0.0009785960796770926",
            "extra": "mean: 2.746428793201287 msec\nrounds: 353"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_read1[disk_collector]",
            "value": 354.8489703477283,
            "unit": "iter/sec",
            "range": "stddev: 0.001054841824145278",
            "extra": "mean: 2.818100328768227 msec\nrounds: 365"
          }
        ]
      }
    ]
  }
}