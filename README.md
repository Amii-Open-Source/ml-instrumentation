# ml-instrumentation
A frame-based data collection utility in python, specifically designed for instrumentation of machine learning experiment code.
This means that this library will strive for first-class compatibility with common machine learning frameworks, and is written with common HPC best-practices in mind.
This library aims to have a high-performance write path, off-loading as much data wrangling as possible to asynchronous background workers.

## Installation
```bash
pip install git+https://github.com/Amii-Open-Source/ml-instrumentation.git
```

## Usage example
```python
from ml_instrumentation.Collector import Collector
from ml_instrumentation.Sampler import Identity, Ignore, MovingAverage, Subsample, Window

collector = Collector(
  # a dictionary mapping keys -> data preprocessors
  config={
    # for instance performing fixed-window averaging
    'return': Window(100),
    # or subsampling 1 of every 100 values
    'reward': Subsample(100),
    # or moving averages
    'error': MovingAverage(0.99),
    # or ignored entirely
    'special': Ignore(),
  },
  # by default, if a key is not mentioned above it is stored as-is
  # however this can be changed by passing a default preprocessor
  default=Identity()
)

# tell the collector which experiment we are currently processing
collector.set_experiment_id(0)

for step in range(exp.max_steps):
  # tell the collector to increment the frame
  collector.next_frame()

  # these values will be associated with the current idx and frame
  collector.collect('reward', r)
  collector.collect('error', delta)

  # not all values need to be stored at each frame
  if step % 100 == 0:
    collector.collect('special', 'test value')
```

## API Documentation
### Collector
The collector stores some context---current experiment ID, current timestep, etc.---and associates collected data with this context.
