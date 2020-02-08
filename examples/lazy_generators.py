#!/usr/bin/env python
"""
    This examples shows the use of typeclasses on Python generators. It allows
    for lazy computation of streaming data in a functional way.

    * First, we create to dummy "Process Shards", which are just meant to
    replicate distributed workers of some sort. We make 3 shards.
    * The stream starts by generating a stream of random integers in [1, 4].
    * Then, for each integer `n`, it explodes it into a stream of `n` ones. So
    the stream `(3, 2)` would become `((1, 1, 1), (1, 1))`. Then it "flattens"
    that back out into a single stream of ones like `(1, 1, 1, 1, 1)`.
    * The stream is then batched into lists of each 3 consecutive value. So
    the stream `(1, 1, 1, 1, 1, 1...)` would become
    `([1, 1, 1], [1, 1, 1]...)`.
    * The batches in this stream are enumerated, so that
    the stream `([1, 1, 1], [1, 1, 1] ...)` becomes
    `((0, [1, 1, 1]), (1, [1, 1, 1]) ...)`
    * With the enumeration, we send every third batch to one of the three
    process shards to be "handled". Here it just prints out a debug string.

    The output of this program with default parameters:
        Shard 0 processing batch 0: [1, 1, 1]
        Shard 1 processing batch 1: [1, 1, 1]
        Shard 2 processing batch 2: [1, 1, 1]
        Shard 0 processing batch 3: [1, 1, 1]
        Shard 1 processing batch 4: [1, 1, 1]
        Shard 2 processing batch 5: [1, 1, 1]
        Shard 0 processing batch 6: [1, 1, 1]
        Shard 1 processing batch 7: [1, 1, 1]
        Shard 2 processing batch 8: [1, 1, 1]
        Shard 0 processing batch 9: [1, 1, 1]

    Note that since everything is lazily evaluated, you can increase the
    `stream_length` value to some arbitrarily large number and everything
    works. This is why functional programming with streaming data becomes
    important when working with scalable processes.

"""
import random

import pycats.instances  # noqa: F401


class ProcessShard:
    """ Simple executor to process batches of data. """

    def __init__(self, shard):
        self.shard = shard

    def process(self, index, batch):
        """ Dummy function for imitating 'doing work'. """
        print(f"Shard {self.shard} processing batch {index}: {batch}")


def generate_integers(num_of_ints, seed=0):
    """ Generate `num_of_ints` random integers in [1, 4]. """
    random.seed(seed)
    for _ in range(num_of_ints):
        yield random.randint(1, 4)


def explode_int(num):
    """ Given an int `n`, return a generator of `n` 1's. """
    for _ in range(num):
        yield 1


def batch_values(stream, batch_size):
    """ Batch values in a stream into lists of length `batch size`. """
    count = 0
    values = list()
    for item in stream:
        values.append(item)
        count += 1
        if count == batch_size:
            yield values
            count = 0
            values = list()


def enum_stream(stream):
    """ Enumerate the values in a stream. """
    for i, x in enumerate(stream):
        yield i, x


if __name__ == "__main__":
    # Parameters
    stream_length = 10
    batch_size = 3
    num_shards = 3

    # Create 3 'distributed shards' for processing data.
    shards = {x: ProcessShard(x) for x in range(num_shards)}

    # Create the stream, but note that no values are computed yet.
    stream = (
        generate_integers(stream_length)
        .flat_map(explode_int)
        .pipe(lambda stream: batch_values(stream, batch_size))
        .pipe(enum_stream)
        .map(lambda x: shards[x[0] % num_shards].process(*x))
    )

    # Now run the stream.
    _ = list(stream)
