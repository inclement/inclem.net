Pyonic interpreter 0.7 released: Python for Android, now supports Python 3
##########################################################################

:date: 2016-11-05 10:30
:tags: python, android, kivy, pyonic
:category: kivy
:slug: pyonic_interpreter_0_7_released
:author: Alexander Taylor

Pyonic interpreter 0.7 has just been released. There are now two
versions on Google Play, one `for Python 2.7
<https://play.google.com/store/apps/details?id=net.inclem.pyonicinterpreter>`__
and one `for Python 3.5
<https://play.google.com/store/apps/details?id=net.inclem.pyonicinterpreter3>`__. The
APKs are also available directly `from Github
<https://github.com/inclement/Pyonic-interpreter/releases/tag/v0.7>`__. Other
features in this release include a new settings screen and improved
gui arrangement.

.. figure:: {filename}/media/pyonic_0_7_images.png
   :alt: Three screenshots of Pyonic interpreter.
   :align: center
   :width: 700px

The app is written in Python using Kivy, and uses exactly the same
code under both Python versions. This code is open source and
available online `on Github
<https://github.com/inclement/Pyonic-interpreter>`__.

This release includes most of the short term improvements I had
planned, since supporting Python 3 didn't raise any major issues. I
expect that development will now focus on adding a few more usability
tweaks, then working with the Python packaging to add features like
pip installs for new modules, code editing (rather than just the
interpreter interface), and support for GUI creation via Kivy.

