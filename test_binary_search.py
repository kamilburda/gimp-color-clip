# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

import binary_search

#===============================================================================

"""
TODO:
- specify test cases for _get_white_point
- test _get_white_point
- test _get_black_point
- test new _get_white_point
- test new _get_black_point
- remove TestBinarySearch since it should no longer necessary at this point
"""


def _left_value(a, b, coefficient=0.4):
  """
  Return a value between two specified values that is closer to the smaller value,
  using the specified coefficient.
  
  The coefficient must be in range (0, 0.5). The coefficient is 0.4 by default.
  """
  
  if a > b:
    a, b = b, a
  
  coefficient = max(0.0, min(coefficient, 0.5))
  
  return a + ((b - a) * coefficient)


def _middle_value(a, b):
  """
  Return a value in the middle of two specified values.
  """
  
  return (a + b) / 2.0


def _right_value(a, b, coefficient=0.4):
  """
  Return a value between two specified values that is closer to the greater value,
  using the specified coefficient.
  
  The coefficient must be in range (0, 0.5). The coefficient is 0.4 by default.
  """
  
  if a > b:
    a, b = b, a
  
  coefficient = max(0.0, min(coefficient, 0.5))
  
  return b - ((b - a) * coefficient)


#-------------------------------------------------------------------------------


_INDEX_MODES = _LEFTMOST_INDEX, _RIGHTMOST_INDEX = (0, 1)


def _get_list_with_unique_values_and_indexes(sequence, index_mode):
  """
  From an ordered sequence of numbers, return a list of unique values and
  indexes of each item.
  
  If `index_mode` is _RIGHTMOST_INDEX`, return the last item in the series of items of
  equal value. If `index_mode` is _LEFTMOST_INDEX`, return the first item in the series
  of items of equal value.
  
  For example, if the input list is
  
    [1, 3, 3, 5, 7, 8, 8, 8, 9]
  
  and `index_mode` is `_RIGHTMOST_INDEX`, the returned list will be
    
    [[1, 0], [3, 2], [5, 3], [7, 4], [8, 7], [9, 8]]
  
  If `index_mode` is `_LEFTMOST_INDEX`, the returned list will be
    
    [[1, 0], [3, 1], [5, 3], [7, 4], [8, 5], [9, 8]]
  
  """
  
  if index_mode == _RIGHTMOST_INDEX:
    # The index of the first item will be properly incremented on the first iteration.
    unique_list = [[sequence[0], -1]]
  else:
    unique_list = [[sequence[0], 0]]
  previous_value = sequence[0]
  
  for i, value in enumerate(sequence):
    if value != previous_value:
      unique_list.append([value, i])
    else:
      if index_mode == _RIGHTMOST_INDEX:
        # Update the index of the most recent item.
        unique_list[-1][1] += 1
    
    previous_value = value
  
  return unique_list


#===============================================================================


class TestBinarySearch(unittest.TestCase):
  
  def test_binary_search(self):
    sequence = [1, 1, 3, 4, 5, 10, 25, 50, 50, 50, 50, 90, 90]
    unique_list = _get_list_with_unique_values_and_indexes(sequence, _RIGHTMOST_INDEX)
    
    min_value = 0.0
    max_value = 100.0
    
    # Values matching items
    for value, index in unique_list:
      self.assertEqual(binary_search.binary_search(sequence, value), index)
     
    # Values lying between contiguous items, closer to the left item
    for i in range(1, len(unique_list)):
      current_value = unique_list[i][0]
      previous_value = unique_list[i - 1][0]
      previous_index = unique_list[i - 1][1]
      self.assertEqual(binary_search.binary_search(sequence, _left_value(current_value, previous_value)),
                       previous_index)
     
    # Values lying between contiguous items, precisely in the middle
    for i in range(1, len(unique_list)):
      current_value = unique_list[i][0]
      previous_value = unique_list[i - 1][0]
      previous_index = unique_list[i - 1][1]
      self.assertEqual(binary_search.binary_search(sequence, _middle_value(current_value, previous_value)),
                       previous_index)
    
    # Values lying between contiguous items, closer to the right item
    for i in range(1, len(unique_list)):
      current_value = unique_list[i][0]
      previous_value = unique_list[i - 1][0]
      current_index = unique_list[i][1]
      self.assertEqual(binary_search.binary_search(sequence, _right_value(current_value, previous_value)),
                       current_index)
    
    # Edge case: value less than the first item
    self.assertEqual(binary_search.binary_search(sequence, min_value), 0)
    self.assertEqual(binary_search.binary_search(sequence, _left_value(min_value, unique_list[0][0])), 0)
    self.assertEqual(binary_search.binary_search(sequence, _middle_value(min_value, unique_list[0][0])), 0)
    self.assertEqual(binary_search.binary_search(sequence, _right_value(min_value, unique_list[0][0])), 0)
    
    # Edge case: value greater than the last item
    self.assertEqual(binary_search.binary_search(sequence, _left_value(unique_list[-1][0], max_value)), unique_list[-1][1])
    self.assertEqual(binary_search.binary_search(sequence, _middle_value(unique_list[-1][0], max_value)), unique_list[-1][1])
    self.assertEqual(binary_search.binary_search(sequence, _right_value(unique_list[-1][0], max_value)), unique_list[-1][1])


#===============================================================================


class TestGetWhitePoint(unittest.TestCase):
  pass
  # Test cases - requirements:
    # number of points - 0 - 15
    # values - non-decreasing sequence - from 0.0 to 100.0
      # the first value must always be 0.0
      # the last value must always be 100.0 
    # values - specified manually?
    # getting the value - mock the `pdb.gimp_histogram` function call
      # simply retrieve the value from the list
    # white point - if there are consecutive equal values, take the first occurrence (the first index)
  
  # Test cases - classes:
    # whether there are equal values or not
      # all values are different from each other
      # some values are equal
    # if values are equal, where the equality takes place
      # beginning
        # second value it equal to the minimum
        # second and several subsequent values are equal to the minimum
      # end
        # second to last value it equal to the maximum
        # second to last and several more preceding values are equal to the maximum
      # middle
        # in the first half
        # in the second half
        # over the half
        # two series of equal values in both halves
        # first value the minimum, all other values the maximum
        # last value the maximum, all other values the minimum
    # where the match occurs
      # at the first element (the half)
      # the edges
      # elsewhere
    # input value
      # precise match found
      # input value is closer to the left value
      # input value is closer to the right value
  
  # Test cases:
    # ...
  