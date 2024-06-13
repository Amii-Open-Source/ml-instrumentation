window.BENCHMARK_DATA = {
  "lastUpdate": 1718298161664,
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
      }
    ]
  }
}