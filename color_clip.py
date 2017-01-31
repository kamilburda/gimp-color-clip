#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Color Clip - GIMP plug-in that clips the darkest and brightest pixels in a
# layer
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

"""
Color Clip darkens/brightens a given percentage of the darkest/brightest pixels
in a drawable. The drawable can be a layer, layer mask or a channel.

Color Clip works similarly to the GIMP's built-in tool Normalize
(Colors -> Auto -> Normalize), except that the black and white clip percentages
are adjustable. In fact, Color Clip with the percentages set to 0% achieves the
same effect as Normalize.
"""

#===============================================================================

import gimp
from gimp import pdb
import gimpfu
import gimpenums

#===============================================================================

# `gimpenums` doesn't seem to define an enum for the RGB histogram
# pseudo-channel.
HISTOGRAM_RGB = 5

#===============================================================================


def color_clip(image, drawable, clip_percent_black, clip_percent_white):
  """
  Clip a given percentage of the darkest and brightest pixels of a drawable.
  """
  
  black_point, white_point = get_color_clip(
    image, drawable, clip_percent_black, clip_percent_white)
  pdb.gimp_levels(drawable, 0, black_point, white_point, 1.0, 0, 255)


def get_color_clip(image, drawable, clip_percent_black, clip_percent_white):
  """
  Determine the black and white points based on the specified clip percentages.
  
  This is a wrapper for `_get_color_clip` to correct clip percentages and black
  and white points to prevent color inversion.
  """
  
  clip_percent_black = max(min(clip_percent_black, 100.0), 0.0)
  clip_percent_white = max(min(clip_percent_white, 100.0), 0.0)
  
  # Adjust percentages to prevent color inversion.
  if clip_percent_black + clip_percent_white > 100.0:
    if clip_percent_black > clip_percent_white:
      clip_percent_black = 100.0 - clip_percent_white
    elif clip_percent_white > clip_percent_black:
      clip_percent_white = 100.0 - clip_percent_black
    else:
      clip_percent_black = 50.0
      clip_percent_white = 50.0
  
  black_point, white_point = _get_color_clip(
    drawable, clip_percent_black, clip_percent_white)
  
  # Adjust black point to prevent color inversion.
  if black_point > white_point:
    black_point = white_point
  
  return black_point, white_point


#===============================================================================


def _get_color_clip(drawable, clip_percent_black, clip_percent_white):
  """
  Determine the black and white points based on the specified clip percentages.
  
  For layers and layer groups, use the RGB pseudo-channel of the histogram.
  For channels and layer masks, use the value channel of the histogram.
  """
  
  if isinstance(drawable, gimp.Channel):
    histogram_channel = gimpenums.HISTOGRAM_VALUE
  else:
    histogram_channel = HISTOGRAM_RGB
  
  min_point = 0
  max_point = 255
  
  black_point = _get_black_point(
    drawable, histogram_channel, clip_percent_black, min_point, max_point)
  white_point = _get_white_point(
    drawable, histogram_channel, clip_percent_white, min_point, max_point)
  
  return black_point, white_point


def _get_black_point(
      drawable, histogram_channel, clip_percent_black, min_point, max_point):
  return _get_color_point(
    drawable, histogram_channel, clip_percent_black, min_point, max_point,
    initial_color_point=max_point,
    point_sequence=range(min_point, max_point + 1),
    get_percentile_from_histogram_func=get_black_point_histogram_percentile,
    get_next_point_func=lambda point: point - 1)


def _get_white_point(
      drawable, histogram_channel, clip_percent_white, min_point, max_point):
  return _get_color_point(
    drawable, histogram_channel, clip_percent_white, min_point, max_point,
    initial_color_point=min_point,
    point_sequence=range(max_point, -1, -1),
    get_percentile_from_histogram_func=get_white_point_histogram_percentile,
    get_next_point_func=lambda point: point + 1)


def _get_color_point(
      drawable, histogram_channel, clip_percent, min_point, max_point,
      initial_color_point, point_sequence,
      get_percentile_from_histogram_func, get_next_point_func):
  desired_percentile = 100.0 - clip_percent
  color_point = initial_color_point
  
  for point in point_sequence:
    current_percentile = get_percentile_from_histogram_func(
      drawable, histogram_channel, point, min_point, max_point)
    
    if current_percentile < desired_percentile:
      color_point = get_next_point_func(point)
      break
  
  return color_point


def get_black_point_histogram_percentile(
      drawable, histogram_channel, point, min_point, max_point):
  return _get_histogram_percentile(drawable, histogram_channel, point, max_point)


def get_white_point_histogram_percentile(
      drawable, histogram_channel, point, min_point, max_point):
  return _get_histogram_percentile(drawable, histogram_channel, min_point, point)


def _get_histogram_percentile(drawable, histogram_channel, start_range, end_range):
  normalized_percentile = pdb.gimp_histogram(
    drawable, histogram_channel, start_range, end_range)[5]
  
  return normalized_percentile * 100.0


#===============================================================================

_plugin_help = (
  "If the sum of the specified percentages is higher than 100, one or both "
  "of the percentages are automatically adjusted to prevent color inversion "
  "(e.g. 70% black clip and 40% white clip is executed as 60% black "
  "and 40% white clip).")

gimpfu.register(
  proc_name="get_color_clip",
  blurb=(
    "Return the black and white points of a drawable based on the "
    "specified clip percentages."),
  help=_plugin_help,
  author="khalim19",
  copyright="khalim19",
  date="2017",
  label="",
  imagetypes="RGB*, GRAY*",
  params=[
    (gimpfu.PF_IMAGE, "image", "Input image (unused)", None),
    (gimpfu.PF_DRAWABLE, "drawable", "Input drawable", None),
    (gimpfu.PF_FLOAT, "clip_percent_black", "Black clip percentage", 0.0),
    (gimpfu.PF_FLOAT, "clip_percent_white", "White clip percentage", 0.0)],
  results=[
    (gimpfu.PF_INT, "black_point", "Black point"),
    (gimpfu.PF_INT, "white_point", "White point")],
  function=get_color_clip)

gimpfu.register(
  proc_name="color_clip",
  blurb=(
    "Darken/brighten a given percentage of the darkest/brightest pixels in the "
    "drawable"),
  help="The drawable can be a layer, layer mask or a channel.\n" + _plugin_help,
  author="khalim19",
  copyright="khalim19",
  date="2015",
  label="<Image>/Colors/Color Clip...",
  imagetypes="RGB*, GRAY*",
  params=[
    (gimpfu.PF_SLIDER, "clip_percent_black", "Black clip percentage", 0.0,
     (0.0, 100.0, 0.1)),
    (gimpfu.PF_SLIDER, "clip_percent_white", "White clip percentage", 0.0,
     (0.0, 100.0, 0.1))],
  results=[],
  function=color_clip)

#===============================================================================

if __name__ == "__main__":
  gimpfu.main()
