# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from gimp import pdb


def _get_histogram_percentile(drawable, histogram_channel, start_range, end_range):
  normalized_percentile = pdb.gimp_histogram(
    drawable, histogram_channel, start_range, end_range)[5]
  
  return normalized_percentile * 100.0


def binary_search(sequence, value):
  index, left_value, right_value = _bisect_right_function(
    lambda index, *args: sequence[index], value, 0, len(sequence), 0.0, 100.0)
   
  if index == 0:
    return 0
  elif index == len(sequence):
    return index - 1
   
  if value <= (left_value + right_value) / 2.0:
    # Value is closer to the left value or in the middle.
    return index - 1
  else:
    # Consecutive values to the right may be equal. It is needed to determine
    # the last index of this value. Therefore, another search is performed,
    # using the value to the right.
    index, unused_, unused_ = _bisect_right_function(
      lambda index, *args: sequence[index], right_value, 0, len(sequence), 0.0, 100.0)
    return index - 1


_BISECT_MODES = _BISECT_LEFT, _BISECT_RIGHT = (0, 1)


def _bisect_right_function(
      sequence_retrieval_func, value, min_index, max_index,
      min_value=None, max_value=None):
  """
  This is a modified implementation of `bisect_right` from the `bisect`
  standard module. Instead of a fixed sequence, a function is passed
  that retrieves a value from a sequence.
  
  This approach may be preferred in situations where each call to retrieve a
  value from the sequence is expensive performance-wise.
  
  Parameters:
  
    * `sequence_retrieval_func` - The function to retrieve a value from a
      sequence.
      Function arguments:
    
        * index from which to retrieve the value
        * current lowest index
        * current highest index
        * the `value` parameter of this function
  
    * `value` - Value to search for.
    * `min_index` - Lowest index to start the search from.
    * `max_index` - Highest index to start the search from.
    * `min_value` - Value at the lowest index.
    * `max_value` - Value at the highest index.
  
  Returns:
  
    * `index` - Index at which `value` could be inserted. This is the same value
      that the `bisect_right` function from the `bisect` module returns.
    
    * `left_value` - The closest value to `index` from the left. `left_value`
      equals `min_value` if `index` equals `min_index`.
    
    * `right_value` - The closest value to `index` from the right. `right_value`
      equals `max_value` if `index` equals `max_index`.
  """
  
  return _bisect_function(
    sequence_retrieval_func, value, _BISECT_RIGHT, min_index, max_index,
    min_value, max_value)


def _bisect_left_function(
      sequence_retrieval_func, value, min_index, max_index,
      min_value=None, max_value=None):
  """
  This is a modified implementation of `bisect_left` from the `bisect`
  standard module. Instead of a fixed sequence, a function is passed
  that retrieves a value from a sequence.
  
  This approach may be preferred in situations where each call to retrieve a
  value from the sequence is expensive performance-wise.
  """
  
  return _bisect_function(
    sequence_retrieval_func, value, _BISECT_LEFT, min_index, max_index,
    min_value, max_value)
  

def _bisect_function(
      sequence_retrieval_func, value, bisect_mode, min_index, max_index,
      min_value=None, max_value=None):
  
  def _compare_values_bisect_left(middle_value, value):
    return middle_value < value
  
  def _compare_values_bisect_right(middle_value, value):
    return middle_value <= value
  
  if bisect_mode == _BISECT_LEFT:
    compare_values = _compare_values_bisect_left
  elif bisect_mode == _BISECT_RIGHT:
    compare_values = _compare_values_bisect_right
  else:
    raise ValueError(
      "invalid bisect mode, must be one of {0}".format(_BISECT_MODES))
  
  left_value = min_value
  right_value = max_value
  low_index = min_index
  high_index = max_index
  
  while low_index < high_index:
    middle_index = (low_index + high_index) // 2
    middle_value = sequence_retrieval_func(middle_index, low_index, high_index, value)
    
    if compare_values(middle_value, value):
      low_index = middle_index + 1
      left_value = middle_value
    else:
      high_index = middle_index
      right_value = middle_value
  
  index = low_index
  return index, left_value, right_value


def _new_get_white_point(drawable, histogram_channel, clip_percent_white):
  
  def _get_percentile_white_point(point, *args):
    return _get_histogram_percentile(drawable, histogram_channel, 0, point)
  
  min_point = 0
  max_point = 255
  min_percentile = 0.0
  max_percentile = 100.0
  desired_percentile = max_percentile - clip_percent_white
  
  white_point, left_value, right_value = _bisect_right_function(
    _get_percentile_white_point, desired_percentile, min_point, max_point,
    min_percentile, max_percentile)
  
  if white_point == min_point:
    return white_point
  elif white_point == max_point:
    return white_point - 1
  
  if desired_percentile <= (left_value + right_value) / 2.0:
    # Value is closer to the left value or in the middle.
    return white_point - 1
  else:
    # Consecutive values to the right may be equal. We need to determine the
    # last index of this value - therefore, another search is performed, using
    # the value to the right.
    white_point, unused_, unused_ = _bisect_right_function(
      _get_percentile_white_point, right_value, min_point, max_point,
      min_percentile, max_percentile)
    return white_point - 1
