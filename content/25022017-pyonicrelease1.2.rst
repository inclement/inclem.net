Pyonic interpreter 1.2 released: Now supports Python 3.6 and input functions
############################################################################

:date: 2017-02-25 22:15
:tags: python, android, kivy, pyonic
:category: kivy
:slug: pyonic_interpreter_1_2_released
:author: Alexander Taylor

I've just released Pyonic interpreter 1.2. As usual, you can get it
from Google Play, now for `Python 2.7
<https://play.google.com/store/apps/details?id=net.inclem.pyonicinterpreter>`__
or `Python 3.6
<https://play.google.com/store/apps/details?id=net.inclem.pyonicinterpreter3>`__.
The APKs can also de bownloaded directly `from Github
<https://github.com/inclement/Pyonic-interpreter/releases/tag/v.1.1.0>`__
(where the `source code
<https://github.com/inclement/Pyonic-interpreter>`__ is also
available).

.. figure:: {filename}/media/pyonic_1_2_input.png
   :alt: Pyonic interpreter showing docstring and autocompletion options
   :align: center
   :width: 300px

This is the first release to target Python 3.6 on Android (not just
Python 3.5), which is made possible by recent additions to
python-for-android. I expect to do a separate python-for-android
release to announce this shortly.

The main change to the app this release is support for the ``input``
and (in Python 2) ``raw_input`` functions. These would previously
crash as the interpreter isn't really being run in a shell, so the way
they try to take input doesn't work. They are now overridden with new
replacements, which should hopefully behave the same way as the
originals are supposed to but via a more convenient popup gui for the
text to be entered.

I'm still working on file editing and other Python management
functions, but there didn't seem to be any reason to delay a release
since according to the Google Play reviews people are trying and
failing to use the input functions.
