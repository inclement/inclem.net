Pyonic interpreter 1.1 released: Python 2/3 interpereter for Android, now with autocompletion
#############################################################################################

:date: 2016-12-11 23:05
:tags: python, android, kivy, pyonic
:category: kivy
:slug: pyonic_interpreter_1_1_released
:author: Alexander Taylor

I've just released Pyonic interpreter 1.1. As usual, you can get it
from Google Play for `Python 2.7
<https://play.google.com/store/apps/details?id=net.inclem.pyonicinterpreter>`__
or `Python 3.5
<https://play.google.com/store/apps/details?id=net.inclem.pyonicinterpreter3>`__,
or download the APKs directly `from Github
<https://github.com/inclement/Pyonic-interpreter/releases/tag/v.1.1.0>`__
(where the `source code
<https://github.com/inclement/Pyonic-interpreter>`__ is also
available).

.. figure:: {filename}/media/pyonic_1_1_jedi.png
   :alt: Pyonic interpreter showing docstring and autocompletion options
   :align: center
   :width: 300px

The major feature in this release is autocompletion support via the
excellent `jedi library <https://github.com/davidhalter/jedi>`__, as
is used by many editors and IDEs. Pyonic now automatically gives
a list of autocompletion options as you write Python code, any of
which can be selected by tapping it. There's also a new help button,
which when pressed shows the call signature and docstring of the
Python object reference currently under the cursor.

As a further bonus, I've reduced the size of the Python 3 APK by a
further ~25%, it's now around 11MB. This is probably still a little
larger than it needs to be, but is much better than the massive 19MB
version that I first published! I'll continue to try to improve this
with tweaks in python-for-android's Python 3 build process.

For the next release, I intend to go back to improving Pyonic's
process handling, and from there to add support for pip installation
of new modules and file editing. The latter of these will also benefit
from the new autocompletion integration.
