Pyonic interpreter
##################

Pyonic interpreter is a Python interface app for Android. It supports
both Python 2 and Python 3 in the same codebase, and is itself written
in Python using the `Kivy graphical framework
<https://kivy.org/#home>`__. The code is open source and available `on
Github <https://github.com/inclement/Pyonic-interpreter>`__.

Pyonic can be downloaded for Android devices via Google Play, for each
of `Python 2
<https://play.google.com/store/apps/details?id=net.inclem.pyonicinterpreter>`__
and `Python 3
<https://play.google.com/store/apps/details?id=net.inclem.pyonicinterpreter3>`__. You
can also download the APKs for each release `from Github
<https://github.com/inclement/Pyonic-interpreter/releases>`__.  These
APKs should work on any Android device with Android 3.0+ (building for
earlier versions should also work but hasn't been tested). Pyonic also
runs on desktop platforms, although the UI is designed primarily for
touch interaction.

The goal of Pyonic is to provide a convenient Python interface adapted
for mobile use, rather than a plain terminal emulator. It also serves
as a test project for the `python-for-android build tools
<https://github.com/kivy/python-for-android>`__. The app currently
provides an interface to a single Python interpreter instance (which
can be restarted or interrupted). Targeted features for the future
include support for multiple interpreter sessions, file editing, pip
management of the local Python distribution, and support for different
ways of running scripts (e.g. supporting graphics via Kivy).

.. figure:: {filename}/media/pyonic_0_7_images.png
   :alt: Three screenshots of Pyonic interpreter 0.7.
   :align: center
   :width: 700px
    
Technical details
-----------------

Pyonic interpreter is written in Python using Kivy, which is a
cross-platform graphical framework primarily supporting Windows,
Linux, OS X, Android and iOS. As such, Pyonic also works on desktop
platforms, and could probably work on iOS with only a small amount of
work to handle the interpreter abstraction.

On desktop platforms, the Python interpreter is managed as a
subprocess. On Android, it instead runs in a Service. In both cases,
communication with the Pyonic GUI is managed over sockets using the
osc protocol, which is quite crude but works well. This mechanism may
be improved in the future.

Pynoic runs on Android via `python-for-android
<https://github.com/kivy/python-for-android>`__, a packaging tool to
turn Python projects into APKs. It does not need any special treatment
to be compiled this way, and works fine with both Python 2 and Python
3 builds. Information about how to compile an APK can be found `in the
README <https://github.com/inclement/Pyonic-interpreter#building>`__.
