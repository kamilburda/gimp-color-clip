# -*- coding: utf-8 -*-
#
# This file is part of Color Clip.
#
# Copyright (C) 2017 khalim19
#
# Color Clip is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Color Clip is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Color Clip.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

import mock

import color_clip

#===============================================================================


_histogram_percentiles_variable_black_max_white = [
  1.0, 1.0, 1.0, 0.999, 0.998, 0.998, 0.997, 0.995, 0.994, 0.992, 0.990, 0.988, 0.988,
  0.983, 0.980, 0.977, 0.974, 0.970, 0.967, 0.960, 0.960, 0.956, 0.951, 0.946, 0.941,
  0.935, 0.928, 0.928, 0.913, 0.905, 0.896, 0.887, 0.877, 0.866, 0.831, 0.831, 0.819,
  0.806, 0.794, 0.781, 0.769, 0.756, 0.756, 0.732, 0.720, 0.707, 0.695, 0.683, 0.671,
  0.648, 0.648, 0.636, 0.625, 0.613, 0.602, 0.591, 0.580, 0.580, 0.559, 0.549, 0.538,
  0.529, 0.519, 0.510, 0.491, 0.491, 0.483, 0.474, 0.466, 0.458, 0.450, 0.442, 0.442,
  0.428, 0.421, 0.414, 0.407, 0.401, 0.395, 0.383, 0.383, 0.377, 0.372, 0.366, 0.361,
  0.356, 0.351, 0.351, 0.342, 0.338, 0.333, 0.329, 0.325, 0.321, 0.314, 0.314, 0.310,
  0.304, 0.301, 0.298, 0.295, 0.293, 0.293, 0.288, 0.285, 0.283, 0.281, 0.278, 0.276,
  0.272, 0.272, 0.270, 0.268, 0.266, 0.265, 0.263, 0.261, 0.261, 0.258, 0.257, 0.255,
  0.253, 0.251, 0.249, 0.244, 0.244, 0.242, 0.240, 0.238, 0.237, 0.235, 0.233, 0.233,
  0.229, 0.227, 0.225, 0.223, 0.221, 0.219, 0.215, 0.215, 0.212, 0.210, 0.208, 0.205,
  0.203, 0.200, 0.200, 0.195, 0.193, 0.190, 0.188, 0.185, 0.182, 0.177, 0.177, 0.174,
  0.171, 0.169, 0.166, 0.160, 0.157, 0.157, 0.150, 0.147, 0.143, 0.140, 0.136, 0.133,
  0.126, 0.126, 0.123, 0.120, 0.117, 0.113, 0.110, 0.107, 0.107, 0.101, 0.098, 0.095,
  0.092, 0.089, 0.086, 0.080, 0.080, 0.077, 0.075, 0.072, 0.069, 0.067, 0.065, 0.065,
  0.060, 0.058, 0.055, 0.053, 0.051, 0.049, 0.045, 0.045, 0.043, 0.041, 0.039, 0.037,
  0.036, 0.034, 0.034, 0.030, 0.028, 0.027, 0.025, 0.024, 0.022, 0.019, 0.019, 0.018,
  0.017, 0.016, 0.015, 0.014, 0.013, 0.013, 0.011, 0.010, 0.010, 0.009, 0.008, 0.008,
  0.007, 0.007, 0.006, 0.006, 0.006, 0.005, 0.005, 0.005, 0.005, 0.004, 0.004, 0.003,
  0.003, 0.003, 0.002, 0.002, 0.002, 0.001, 0.001, 0.001, 0.001, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0]


_histogram_percentiles_min_black_variable_white = [
  0.0, 0.0, 0.0, 0.001, 0.001, 0.002, 0.004, 0.005, 0.007, 0.009, 0.011, 0.011,
  0.016, 0.019, 0.022, 0.025, 0.029, 0.032, 0.039, 0.039, 0.043, 0.048, 0.053, 0.058,
  0.064, 0.071, 0.071, 0.086, 0.094, 0.103, 0.112, 0.122, 0.133, 0.168, 0.168, 0.180,
  0.193, 0.205, 0.218, 0.230, 0.243, 0.243, 0.267, 0.279, 0.292, 0.304, 0.316, 0.328,
  0.351, 0.351, 0.363, 0.374, 0.386, 0.397, 0.408, 0.419, 0.419, 0.440, 0.450, 0.461,
  0.470, 0.480, 0.489, 0.508, 0.508, 0.516, 0.525, 0.533, 0.541, 0.549, 0.557, 0.557,
  0.571, 0.578, 0.585, 0.592, 0.598, 0.604, 0.616, 0.616, 0.622, 0.627, 0.633, 0.638,
  0.643, 0.648, 0.648, 0.657, 0.661, 0.666, 0.670, 0.674, 0.678, 0.685, 0.685, 0.689,
  0.695, 0.698, 0.701, 0.704, 0.706, 0.706, 0.711, 0.714, 0.716, 0.718, 0.721, 0.723,
  0.727, 0.727, 0.729, 0.731, 0.733, 0.734, 0.736, 0.738, 0.738, 0.741, 0.742, 0.744,
  0.746, 0.748, 0.750, 0.755, 0.755, 0.757, 0.759, 0.761, 0.762, 0.764, 0.766, 0.766,
  0.770, 0.772, 0.774, 0.776, 0.778, 0.780, 0.784, 0.784, 0.787, 0.789, 0.791, 0.794,
  0.796, 0.799, 0.799, 0.804, 0.806, 0.809, 0.811, 0.814, 0.817, 0.822, 0.822, 0.825,
  0.828, 0.830, 0.833, 0.839, 0.842, 0.842, 0.849, 0.852, 0.856, 0.859, 0.863, 0.866,
  0.873, 0.873, 0.876, 0.879, 0.882, 0.886, 0.889, 0.892, 0.892, 0.898, 0.901, 0.904,
  0.907, 0.910, 0.913, 0.919, 0.919, 0.922, 0.924, 0.927, 0.930, 0.932, 0.934, 0.934,
  0.939, 0.941, 0.944, 0.946, 0.948, 0.950, 0.954, 0.954, 0.956, 0.958, 0.960, 0.962,
  0.963, 0.965, 0.965, 0.969, 0.971, 0.972, 0.974, 0.975, 0.977, 0.980, 0.980, 0.981,
  0.982, 0.983, 0.984, 0.985, 0.986, 0.986, 0.988, 0.989, 0.989, 0.990, 0.991, 0.991,
  0.992, 0.992, 0.993, 0.993, 0.993, 0.994, 0.994, 0.994, 0.994, 0.995, 0.995, 0.996,
  0.996, 0.996, 0.997, 0.997, 0.997, 0.998, 0.998, 0.998, 0.998, 0.999, 0.999, 0.999,
  0.999, 1.0, 1.0, 1.0]


def _get_black_point_histogram_percentile(
      drawable, histogram_channel, point, min_point, max_point):
  return _histogram_percentiles_variable_black_max_white[point] * 100.0

  
def _get_white_point_histogram_percentile(
      drawable, histogram_channel, point, min_point, max_point):
  return _histogram_percentiles_min_black_variable_white[point] * 100.0


#===============================================================================


@mock.patch(
  "color_clip.get_black_point_histogram_percentile",
  new=_get_black_point_histogram_percentile)
@mock.patch(
  "color_clip.get_white_point_histogram_percentile",
  new=_get_white_point_histogram_percentile)
class TestGetColorClip(unittest.TestCase):
  
  def setUp(self):
    self.image = None
    self.drawable = None
  
  def test_nominal_cases(self):
    self._test_get_color_clip_with_data([
      ((0.0, 0.0), (2, 253)),
      ((0.0, 1.0), (2, 225)),
      ((1.0, 0.0), (10, 253)),
      ((1.0, 1.0), (10, 225)),
    ])
  
  def test_get_last_point_with_same_value(self):
    self._test_get_color_clip_with_data([
      ((0.2, 0.0), (5, 253)),
      ((0.0, 0.2), (2, 245)),
    ])
  
  def test_bound_clip_percentages(self):
    self._test_get_color_clip_with_data([
      ((-1.0, -1.0), (2, 253)),
      ((101.0, 0.0), (253, 253)),
      ((0.0, 101.0), (0, 0)),
    ])
  
  def test_prevent_color_inversion_from_clip_percentages(self):
    self._test_get_color_clip_with_data([
      ((100.0, 1.0), (225, 225)),
      ((1.0, 100.0), (10, 10)),
      ((51.0, 51.0), (63, 63)),
      ((100.0, 100.0), (63, 63)),
    ])
  
  def test_prevent_color_inversion_from_points(self):
    self._test_get_color_clip_with_data([
      ((50.0, 50.0), (63, 63)),
      ((100.0, 0.0), (253, 253)),
      ((0.0, 100.0), (0, 0)),
    ])
  
  def _test_get_color_clip_with_data(self, test_inputs_outputs):
    for clip_percentages, expected_color_points in test_inputs_outputs:
      self._test_get_color_clip(clip_percentages, expected_color_points)
  
  def _test_get_color_clip(self, clip_percentages, expected_color_points):
    self.assertEqual(
      color_clip.get_color_clip(self.image, self.drawable, *clip_percentages),
      expected_color_points)
