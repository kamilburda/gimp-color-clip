Color Clip
==========

Color Clip is a [GIMP](https://www.gimp.org/) plug-in that darkens/brightens a
given percentage of the darkest/brightest pixels in a drawable. The drawable can
be a layer, layer mask or a channel.

Color Clip works similarly to the GIMP's built-in tool Normalize
(`Colors -> Auto -> Normalize`), except that the black and white clip percentages
are adjustable. In fact, Color Clip with the percentages set to 0% achieves the
same effect as Normalize.


Installation
------------

Copy the `color_clip.py` file to
`[your home folder]\.gimp-[GIMP version]\plug-ins`.

Example of an installation directory: 
* Windows: `C:\Users\khalim\.gimp-2.8\plug-ins`
* Linux: `/home/khalim/.gimp-2.8/plug-ins`
* OS X: `/Users/khalim/Library/Application Support/GIMP/2.8/plug-ins`


Usage
-----

Open an image in GIMP, select `Colors -> Color Clip...` and adjust the clip
percentages as desired.


Support
-------

You can report issues, ask questions or request new features:
* on the [GitHub issues page]
  (https://github.com/khalim19/gimp-plugin-color-clip/issues)
* via email: khalim19 AT gmail DOT com


License
-------

Color Clip is licensed under the
[GNU GPLv3](http://www.gnu.org/licenses/gpl-3.0.html) license.
