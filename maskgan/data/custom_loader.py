# Copyright 2017 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Custom data loader and helpers. Modified from
`ptb_loader.py` to work with custom dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os
# Dependency imports
import numpy as np

import tensorflow as tf

# Import utilities
from . import ptb_loader
EOS_INDEX = 0


def _read_words(filename):
    try:
        return ptb_loader._read_words(filename)
    except AttributeError:
        with open(filename, "r") as f:
            return f.read().replace("\n", " <eos> ").split()


def build_vocab(filename):
  data = _read_words(filename)

  counter = collections.Counter(data)
  count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

  words, _ = list(zip(*count_pairs))
  word_to_id = dict(zip(words, range(len(words))))
  print("<eos>:", word_to_id["<eos>"])
  global EOS_INDEX
  EOS_INDEX = word_to_id["<eos>"]

  return word_to_id


def _file_to_word_ids(filename, word_to_id):
  data = _read_words(filename)
  return [word_to_id[word] for word in data if word in word_to_id]


def custom_raw_data(train_path, valid_path, test_path):
  """Load custom raw data from data directory "data_path".
  Reads custom text files, converts strings to integer ids,
  and performs mini-batching of the inputs.
  Args:
    *path: string path to the text files containing input data.
  Returns:
    tuple (train_data, valid_data, test_data, vocabulary)
    where each of the data objects can be passed to
    `custom_loader.data_iterator`.
  """

  word_to_id = build_vocab(train_path)
  train_data = _file_to_word_ids(train_path, word_to_id)
  valid_data = _file_to_word_ids(valid_path, word_to_id)
  test_data = _file_to_word_ids(test_path, word_to_id)
  vocabulary = len(word_to_id)
  return train_data, valid_data, test_data, vocabulary


def custom_iterator(raw_data, batch_size, num_steps, epoch_size_override=None):
  """Iterate on the raw custom data.

  This generates batch_size pointers into the raw custom data, and allows
  minibatch iteration along these pointers.

  Args:
    raw_data: one of the raw data outputs from `custom_loader.load_raw_data`.
    batch_size: int, the batch size.
    num_steps: int, the number of unrolls.

  Yields:
    Pairs of the batched data, each a matrix of shape [batch_size, num_steps].
    The second element of the tuple is the same data time-shifted to the
    right by one.

  Raises:
    ValueError: if batch_size or num_steps are too high.
  """
  return ptb_loader.ptb_iterator(raw_data, batch_size, num_steps, epoch_size_override)
