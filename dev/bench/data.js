window.BENCHMARK_DATA = {
  "lastUpdate": 1721667408985,
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
      },
      {
        "commit": {
          "author": {
            "email": "andnpatterson@gmail.com",
            "name": "andnp",
            "username": "andnp"
          },
          "committer": {
            "email": "160795226+andy-amii@users.noreply.github.com",
            "name": "andy-amii",
            "username": "andy-amii"
          },
          "distinct": true,
          "id": "caed571ab688139893f412ce001452d378975f70",
          "message": "feat: add ability to merge collectors across processes",
          "timestamp": "2024-07-11T12:44:49-06:00",
          "tree_id": "51285e63c5d8f32ad4c05622eea6fae1e1e7881f",
          "url": "https://github.com/Amii-Open-Source/ml-instrumentation/commit/caed571ab688139893f412ce001452d378975f70"
        },
        "date": 1720723520452,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_write_path1[basic_collector]",
            "value": 139.00268502401903,
            "unit": "iter/sec",
            "range": "stddev: 0.0022567175370788338",
            "extra": "mean: 7.194105637795447 msec\nrounds: 127"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_write_path1[disk_collector]",
            "value": 95.69376474059906,
            "unit": "iter/sec",
            "range": "stddev: 0.0024195118710011107",
            "extra": "mean: 10.450001655914994 msec\nrounds: 93"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_read1[basic_collector]",
            "value": 357.4004371174527,
            "unit": "iter/sec",
            "range": "stddev: 0.0010885219658171696",
            "extra": "mean: 2.7979820284085704 msec\nrounds: 352"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_read1[disk_collector]",
            "value": 352.60356063552604,
            "unit": "iter/sec",
            "range": "stddev: 0.0012016543726832854",
            "extra": "mean: 2.8360462333324676 msec\nrounds: 360"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "49699333+dependabot[bot]@users.noreply.github.com",
            "name": "dependabot[bot]",
            "username": "dependabot[bot]"
          },
          "committer": {
            "email": "160795226+andy-amii@users.noreply.github.com",
            "name": "andy-amii",
            "username": "andy-amii"
          },
          "distinct": true,
          "id": "682c13e6b6b09fe85eba408a002d9ca3d6a72168",
          "message": "chore(deps): update numpy requirement in the python-deps group\n\nUpdates the requirements on [numpy](https://github.com/numpy/numpy) to permit the latest version.\n\nUpdates `numpy` to 2.0.1\n- [Release notes](https://github.com/numpy/numpy/releases)\n- [Changelog](https://github.com/numpy/numpy/blob/main/doc/RELEASE_WALKTHROUGH.rst)\n- [Commits](https://github.com/numpy/numpy/compare/v1.26.0...v2.0.1)\n\n---\nupdated-dependencies:\n- dependency-name: numpy\n  dependency-type: direct:production\n  dependency-group: python-deps\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>",
          "timestamp": "2024-07-22T10:56:21-06:00",
          "tree_id": "c294e8b3ae6d4c434da0ab5217de754a289f68aa",
          "url": "https://github.com/Amii-Open-Source/ml-instrumentation/commit/682c13e6b6b09fe85eba408a002d9ca3d6a72168"
        },
        "date": 1721667408551,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_write_path1[basic_collector]",
            "value": 138.36177212591835,
            "unit": "iter/sec",
            "range": "stddev: 0.0021185483294214927",
            "extra": "mean: 7.227429835821515 msec\nrounds: 134"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_write_path1[disk_collector]",
            "value": 100.05517730354283,
            "unit": "iter/sec",
            "range": "stddev: 0.001934956009587043",
            "extra": "mean: 9.994485312501578 msec\nrounds: 64"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_read1[basic_collector]",
            "value": 364.821072358596,
            "unit": "iter/sec",
            "range": "stddev: 0.0011709479415729562",
            "extra": "mean: 2.741069734637103 msec\nrounds: 358"
          },
          {
            "name": "tests/performance/test_Collector.py::test_benchmark_read1[disk_collector]",
            "value": 362.4850488361858,
            "unit": "iter/sec",
            "range": "stddev: 0.0010336888491414135",
            "extra": "mean: 2.7587344725269483 msec\nrounds: 364"
          }
        ]
      }
    ]
  }
}