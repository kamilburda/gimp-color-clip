#! /usr/bin/env python

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import GObject

import procedure


def python_fu_color_clip(proc, run_mode, image, drawables, config, _data):
  dialog = None

  if run_mode == Gimp.RunMode.INTERACTIVE:
    dialog = GimpUi.ProcedureDialog(procedure=proc, config=config, title=None)
    dialog.fill(['clip-percent-black', 'clip-percent-white'])

    is_ok_pressed = dialog.run()
    if not is_ok_pressed:
      dialog.destroy()
      return Gimp.PDBStatusType.CANCEL

  linear_and_other_precisions = {
    Gimp.Precision.U8_NON_LINEAR: Gimp.Precision.U8_LINEAR,
    Gimp.Precision.U8_PERCEPTUAL: Gimp.Precision.U8_LINEAR,
    Gimp.Precision.U16_NON_LINEAR: Gimp.Precision.U16_LINEAR,
    Gimp.Precision.U16_PERCEPTUAL: Gimp.Precision.U16_LINEAR,
    Gimp.Precision.U32_NON_LINEAR: Gimp.Precision.U32_LINEAR,
    Gimp.Precision.U32_PERCEPTUAL: Gimp.Precision.U32_LINEAR,
    Gimp.Precision.HALF_NON_LINEAR: Gimp.Precision.HALF_LINEAR,
    Gimp.Precision.HALF_PERCEPTUAL: Gimp.Precision.HALF_LINEAR,
    Gimp.Precision.FLOAT_NON_LINEAR: Gimp.Precision.FLOAT_LINEAR,
    Gimp.Precision.FLOAT_PERCEPTUAL: Gimp.Precision.FLOAT_LINEAR,
    Gimp.Precision.DOUBLE_NON_LINEAR: Gimp.Precision.DOUBLE_LINEAR,
    Gimp.Precision.DOUBLE_PERCEPTUAL: Gimp.Precision.DOUBLE_LINEAR,
  }

  image.undo_group_start()

  orig_precision = None
  if image.get_precision() not in linear_and_other_precisions.values():
    orig_precision = image.get_precision()
    image.convert_precision(linear_and_other_precisions[orig_precision])

  for drawable in drawables:
    black_point, white_point = get_color_clip(
      drawable,
      config.get_property('clip-percent-black'),
      config.get_property('clip-percent-white'),
    )
    drawable.levels(
      Gimp.HistogramChannel.VALUE,
      black_point / 255,
      white_point / 255,
      False,
      1.0,
      0.0,
      1.0,
      False,
    )

  if orig_precision is not None:
    image.convert_precision(orig_precision)

  image.undo_group_end()

  if dialog is not None:
    dialog.destroy()

  return Gimp.PDBStatusType.SUCCESS


def get_color_clip(drawable, clip_percent_black, clip_percent_white):
  """Determines the black and white points based on the specified clip
  percentages.

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


def _get_color_clip(drawable, clip_percent_black, clip_percent_white):
  """
  Determine the black and white points based on the specified clip percentages.
  
  For layers and layer groups, use the RGB pseudo-channel of the histogram.
  For channels and layer masks, use the value channel of the histogram.
  """

  min_point = 0
  max_point = 255
  
  black_point = _get_black_point(drawable, clip_percent_black, min_point, max_point)
  white_point = _get_white_point(drawable, clip_percent_white, min_point, max_point)
  
  return black_point, white_point


def _get_black_point(drawable, clip_percent_black, min_point, max_point):
  return _get_color_point(
    drawable,
    clip_percent_black,
    min_point,
    max_point,
    initial_color_point=max_point,
    point_sequence=range(min_point, max_point + 1),
    get_percentile_from_histogram_func=get_black_point_histogram_percentile,
    get_next_point_func=lambda point: point - 1,
  )


def _get_white_point(drawable, clip_percent_white, min_point, max_point):
  return _get_color_point(
    drawable,
    clip_percent_white,
    min_point,
    max_point,
    initial_color_point=min_point,
    point_sequence=range(max_point, -1, -1),
    get_percentile_from_histogram_func=get_white_point_histogram_percentile,
    get_next_point_func=lambda point: point + 1,
  )


def _get_color_point(
      drawable,
      clip_percent,
      min_point,
      max_point,
      initial_color_point,
      point_sequence,
      get_percentile_from_histogram_func,
      get_next_point_func,
):
  desired_percentile = 100.0 - clip_percent
  color_point = initial_color_point
  
  for point in point_sequence:
    current_percentile = get_percentile_from_histogram_func(drawable, point, min_point, max_point)
    
    if current_percentile < desired_percentile:
      color_point = get_next_point_func(point)
      break
  
  return color_point


def get_black_point_histogram_percentile(drawable, point, _min_point, max_point):
  return _get_histogram_percentile(drawable, point, max_point)


def get_white_point_histogram_percentile(drawable, point, min_point, _max_point):
  return _get_histogram_percentile(drawable, min_point, point)


def _get_histogram_percentile(drawable, start_range, end_range):
  if isinstance(drawable, Gimp.Channel):
    normalized_percentile = drawable.histogram(
      Gimp.HistogramChannel.VALUE, start_range / 255, end_range / 255).percentile
    return normalized_percentile * 100.0
  else:
    # Use the RGB pseudo-channel which combines the individual red, green and
    # blue channels.
    histogram_red = drawable.histogram(
      Gimp.HistogramChannel.RED, start_range / 255, end_range / 255)
    histogram_green = drawable.histogram(
      Gimp.HistogramChannel.GREEN, start_range / 255, end_range / 255)
    histogram_blue = drawable.histogram(
      Gimp.HistogramChannel.BLUE, start_range / 255, end_range / 255)

    return (
      (histogram_red.count + histogram_green.count + histogram_blue.count)
      / (histogram_red.pixels + histogram_green.pixels + histogram_blue.pixels)
    ) * 100.0


_plugin_help = (
  "If the sum of the specified percentages is higher than 100, one or both "
  "of the percentages are automatically adjusted to prevent color inversion "
  "(e.g. 70% black clip and 40% white clip is treated as 60% black "
  "and 40% white clip).")


procedure.register_procedure(
  python_fu_color_clip,
  procedure_type=Gimp.ImageProcedure,
  arguments=[
    [
      'double',
      'clip-percent-black',
      'Black clip percentage',
      'Black clip percentage',
      0.0,
      100.0,
      0.0,
      GObject.ParamFlags.READWRITE,
    ],
    [
      'double',
      'clip-percent-white',
      'White clip percentage',
      'White clip percentage',
      0.0,
      100.0,
      0.0,
      GObject.ParamFlags.READWRITE,
    ],
  ],
  menu_label='Color Clip...',
  menu_path='<Image>/Colors',
  image_types="RGB*, GRAY*",
  documentation=(
    'Darkens/brightens a given percentage of the darkest/brightest pixels in the drawable.',
    f'The drawable can be a layer, layer mask or a channel.\n{_plugin_help}',
  ),
  attribution=('Kamil Burda', 'Kamil Burda', '2015'),
  sensitivity_mask=(
    Gimp.ProcedureSensitivityMask.DRAWABLE
    | Gimp.ProcedureSensitivityMask.DRAWABLES),
)


procedure.main()
