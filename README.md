# ml-instrumentation

[![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](./CONTRIBUTING.md)

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
The collector stores some context---the current experiment id and current timestep---and associates collected data with this context.
The collector object is the primary front-end of the library.

#### `__init__`
```python
from ml_instrumentation.Collector import Collector

collector = Collector(
  # [optional] - location of the backing storage for collected data.
  # If not specified, defaults to the special string `:memory:` meaning an in-memory db.
  # If a file path: `/tmp/slurm/experiment_id/data.db`, will create a disk-backed db.
  tmp_file=':memory:',

  # [optional] - a dictionary of preprocessors for each metric of interest.
  # If a metric is not specified in this config, a default preprocessor will be assigned.
  config={
    'metric_name_1': Ignore(),
    'metric_name_2': Subsample(100),
  },

  # [optional] - the default preprocessor for metrics not specified above.
  # If not given, will use the `Identity()` preprocessor which records everything.
  default=Ignore(),

  #[optional] - the id for the currently running experiment. This can be specified
  # here or mutated on the object after creation. Accepts string ids or integer ids.
  experiment_id=0,
)
```

#### `set_experiment_id(id: str | int)`
Mutates the collector object with a new experiment id.
There should generally be few experiment ids and many frames.
Changing the experiment restarts the frame counter.
```python
collector.set_experiment_id(0)
```

#### `get_experiment_id() -> str | int`
Returns the current experiment id, raises an exception if an id has not yet been set.

#### `next_frame()`
Increments the reference frame for the collector, associating all incoming data with a new frame id.
Think of this as the timestep of the experiment---in fact, in most cases the frame and the timestep should be identical.
On every timestep, you might collect 5 different pieces of data (`loss`, `prediction`, `reward`, `action_taken`, `stable_rank`) each coming from disparate parts of the codebase.
Instead of gathering these into a centralized location---which usually requires cross-contamination of agent and environment code---the collector uses a global `frame` to associate these different pieces of data with the timestep that they were generated.

Frames can be incremented "leading-edge" (before gathering data) or "trailing-edge" (after gathering data).
Both strategies are translated to "leading-edge" internally, so both give identical results with the first timestep always labeled `frame=0`.

```python
for t in range(timesteps):
  collector.next_frame()
  # ... do a bunch of stuff
  collector.collect('metric_name', data)
```

#### `reset()`
If reusing the same collector object across multiple sequential experiments, a `reset()` is optional between experiments.
This allows stateful sampling strategies (e.g. the `WindowAverage`) an opportunity to report their final ending state.
The ending state will be associated with one final frame.
If an experiment runs for `1_000` steps, then there may be `1_001` total frames (`[0, 1_000]` inclusive on both ends).

Note: if you do not call `reset()` between experiments, then you will not create the final end-state frame, leading to a `1_000` step experiment having exactly `1_000` possible frames.
This may be desirable for certain use-cases and is supported by the library.

```python
for exp_id in experiment_ids:
  collector.set_experiment_id(exp_id)

  run_the_experiment(collector, ...)

  # gather the final state of stateful subsamplers
  collector.reset()
```

#### `close()`
The `collector` object may have in-flight data being written to the backing storage (e.g. to disk).
To ensure this in-flight data is not corrupted or lost, need to `close()` the collector before process termination.
Good practice to register this using the `atexit` built-in module.

```python
import atexit
atexit.register(collector.close)
```

#### `collect(name: str, value: Any)`
The primary ingress method to bring data into the collector.
Values passed to the collector via the `collect` method will first be handed to the
relevant preprocessor.
Preprocessors may choose to toss out collected data (e.g. the `Ignore()` preprocessor tosses out all data), may modify their internal state using the collected data and storing their internal state (e.g. mutating and storing the running average with `MovingAverage(0.99)`), or may pass the raw data through to storage (e.g. the `Identity()` preprocessor stores all data as-is).

```python
# associates both values with frame=0. E.g. resulting in this dataframe:
# frame   metric-1       metric-2
#     0        0.0   'hello world'
collector.collect('metric-1', 0.0)
collector.collect('metric-2', 'hello world')

collector.next_frame()

# associates values with frame=1. Resulting dataframe:
# frame   metric-1       metric-2
#     0        0.0   'hello world'
#     1        1.0           None
collector.collect('metric-1', 1.0)
# don't collect metric-2 on this timestep
```

#### `evaluate(name: str, lmbda: Callable[[], Any])`
An alternative data ingress strategy for when the data collection process itself takes a nontrivial amount of computation and should be called sparingly.
For example: computing statistics about a neural network's representation, performing offline evaluation rollouts in RL, computing validation set statistics in SL, etc.

Takes a 0-arg evaluation function returning the value to be collected.
By default, this function is called on every frame---eliminating the stated purpose of sparse evaluation.
Instead, this is most powerfully combined with subsampling preprocessor strategies such as `Subsample(100)` which would call the evaluation function once every 100 frames.

```python
collector = Collector(
  config={
    # Subsample is a leading-edge subsampler
    'validation_accuracy': Subsample(100),
  }
)
...

for epoch in range(1000):
  collector.next_frame()

  do_the_learning()

  collector.evaluate(
    'validation_accuracy',
    lambda: calculate_validation_accuracy(model, val_X, val_Y),
  )

val_accuracies = collector.get('validation_accuracy', experiment_id=0)
assert len(val_accuracies) == 10 # 1000 frames / 100 subsampling

collected_frames = [point.frame for point in val_accuracies]
assert collected_frames == [0, 99, 199, 299, 399, 499, 599, 699, 799, 899, 999]
```

#### `get(metric: str, experiment_id: int | str) -> List[SqlPoint]`
The primary retrieval method for getting back data that has been written into the collector.
Retrieves data metric-by-metric and for a specified experiment_id.
Returns a list of tuples of type `(frame, id, measurement)`.
```python
collector.set_experiment_id(1)
collector.collect('a', 22)
collector.next_frame()
collector.collect('a', 44)

collector.set_experiment_id(1)
collector.collect('a', 33)

a = collector.get('a', 0)
assert a == [
  # frame, experiment_id, value
  (     0,             0,    22),
  (     1,             0,    44),
]
```

### Sampling
The collection process is controlled through `Sampler` objects specified in the configuration of the collector.
These `Sampler`s intercept incoming data, mutate their internal state, then return a value to be collected (or `None` to skip collection).

Creating a custom `Sampler` is straightforward, the `Sampler` base class contains no logic and is simply an interface class.
```python
class Sampler:
    def next(self, v: float) -> float | None: ...
    def next_eval(self, c: Callable[[], float]) -> float | None: ...
    def end(self) -> float | None: ...
```

Implementations of this interface class need to provide three methods:
- `next(v: float) -> float | None` - called whenever a value is `collect`'ed. Receives the collected value and returns the modified value to be stored (or `None` to skip storing on this frame).
- `next_eval(c: Callable[[], float]) -> float | None` - same as `next`, except called whenever `collector.evaluate(...)` is called. Can selectively call the function `c` to obtain a raw value, then perform arbitrary operations to the raw value to return the value to be stored (or `None` to skip storage on this frame).
- `end() -> float | None` - called whenever `collector.reset()` is called between experiments. This method allows the `Sampler` instantiation to return any lingering stateful data or `None` if there is no data to be associated with the final frame.


This library provides several concrete `Sampler` implementations that are commonly used.

#### `Window(size: int)`
Computes a trailing-edge window average of specified size.
Intermediate frames are empty.
```python
collector = Collector(
  config={
    # Window average over bins of 3 collected values
    'm1': Window(3),
  }
)

# first collection is skipped
collector.collect('m1', 0)
assert collector.get('m1', 0) == []

# second is skipped
collector.next_frame()
collector.collect('m1', 1)
assert collector.get('m1', 0) == []

# third yields the average of [0, 1, 2]
# notice this average is associated with frame=2 (trailing-edge)
collector.next_frame()
collector.collect('m1', 2)
assert collector.get('m1', 0) == [
  # frame, experiment_id, value
  (     2,             0,   1.5),
]
```

#### `Subsample(freq: int)`
Only collect a value every `freq` number of `collect` calls (leading-edge).

```python
collector = Collector(
  config={
    # Store every second collected value
    'm1': Subsample(2),
  }
)

collector.collect('m1', 'hi')
assert collector.get('m1', 0) == [
  # frame, experiment_id, value
  (     0,             0,  'hi'),
]

# on the next collection, the value is not stored
collector.next_frame()
collector.collect('m1', 'there')
assert collector.get('m1', 0) == [
  # frame, experiment_id, value
  (     0,             0,  'hi'),
]

# on the third collection, the value is stored
collector.next_frame()
collector.collect('m1', 'friend')
assert collector.get('m1', 0) == [
  # frame, experiment_id,    value
  (     0,             0,     'hi'),
  (     2,             0, 'friend'),
]
```

#### `MovingAverage(decay: float)`
A simple moving average over numerical data.
The configuration parameter is the decay-rate of the average.
That is, `MovingAverage(0.99)` can be interpreted as "take 99% contribution from the current average, and 1% contribution from the next value."

Unlike the `Window` average, this method is **not** sparse and will return a stored value on every collection call.

```python
collector = Collector(
  config={
    # keep a moving average over ~100 consecutive collected values
    'm1': MovingAverage(0.99),
  }
)

collector.collect('m1', 0)
assert collector.get('m1', 0) == [
  # frame, experiment_id, value
  (     0,             0,     0),
]

collector.next_frame()
collector.collect('m1', 1)
assert collector.get('m1', 0) == [
  # frame, experiment_id, value
  (     0,             0,     0),
  (     1,             0,  0.01),
]
```

#### `Pipe(*args: Sampler)`
This is a meta-sampler that takes 1+ samplers as arguments, then "pipes" collected values through these samplers in left->right order.
If any sampler returns `None` for a given frame, the over result is `None` and no value is collected.
A common use-case is to combine `MovingAverage` and `Subsample` to result in a sparse averaged representation, similar to a `Window` average but with fewer calls to the `evaluate` function.

**Note**: the order of `Sampler`s matters here. `Subsample` then `MovingAverage` would result in a moving average over every 100th value.

```python
collector = Collector(
  config={
    # keep a moving average over ~100 consecutive collected values
    # and only store every 100th MovingAverage value
    'm1': Pipe(
      MovingAverage(0.99),
      Subsample(100),
    ),
  }
)

collector = Collector(
  config={
    # A silly, but demonstrative, example.
    # Would store every 10 * 100 = 1000 collected samples.
    # Both m1 and m2 would be stored on the same frames
    #   (assuming both always collected at the same time)
    'm1': Pipe(
      Subsample(10),
      Subsample(100),
    ),
    'm2': Subsample(1000),
  }
)
```
