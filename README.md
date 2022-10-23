Color Clip
==========

Color Clip is a [GIMP](https://www.gimp.org/) plug-in that darkens/brightens a
given percentage of the darkest/brightest pixels in a drawable. The drawable can
be a layer, layer mask or channel.

Color Clip works similarly to the GIMP's built-in tool Normalize
(`Colors -> Auto -> Normalize`), except that the black and white clip percentages
are adjustable. In fact, Color Clip with the percentages set to 0% achieves the
same effect as Normalize.


Installation
------------

1. In GIMP, locate the folder containing GIMP plug-ins - open GIMP and go to Edit → Preferences → Folders → Plug-Ins.
2. Copy `color_clip.py` to the to one of the folders identified in step 1.

For Windows, make sure you have GIMP installed with support for Python scripting.

For Linux, make sure you use a GIMP installation bundled as Flatpak (which can be downloaded from the [official GIMP page](https://www.gimp.org/downloads/)) or AppImage.

For macOS, make sure you have Python 2.7 installed.


Usage
-----

Open an image in GIMP, select `Colors -> Color Clip...` and adjust the clip percentages as desired.


Support
-------

You can report issues, ask questions or request new features on the [GitHub issues page](https://github.com/khalim19/gimp-plugin-color-clip/issues).


License
-------

Color Clip is licensed under the [BSD 3-Clause](LICENSE) license.
