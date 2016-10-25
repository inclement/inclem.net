Pyonic interpreter: a Python interpreter GUI for Android, written in Python
###########################################################################

:date: 2016-10-17 23:06
:tags: python, android, kivy
:category: kivy
:slug: pyonic_interpreter_0_6_released
:author: Alexander Taylor

I've just released a new app, `Pyonic Python 2 interpreter
<https://play.google.com/store/apps/details?id=net.inclem.pyonicinterpreter>`__.
Pyonic interpreter is a Python interpreter app for Android, providing
a convenient interface adapted to mobile devices. The app itself is
written entirely in Python using `Kivy <https://kivy.org/#home>`__.

.. figure:: {filename}/media/pyonic_android_small.png
   :alt: Screenshot of the interpreter app.
   :align: center

I put this together because I've always thought it would be nice to
have a Python interpreter app that is itself written in Python, and in
principle Kivy and `python-for-android
<http://python-for-android.readthedocs.io/en/latest/>`__ provide all
the necessary components. In practice this worked even better than I
expected, Kivy handled almost everything perfectly - I actually
underestimated its maturity here! As part of the project, I've tried
to round a number of corners that Kivy apps sometimes can to have, so
that the interpreter (hopefully) behaves nicely in all
situations. Within the interpreter, all of the standard library is
available, and it's possible to interrupt execution (equivalent to the
normal ctrl+c behaviour) or to restart the interpreter process. No
external modules are included yet except those necessary for the app
to run, but I'll probably include some major ones like numpy in a
future release, and in the long term the aim is to support pip
installs of new modules.

This has also been a great stimulus for working on python-for-android;
I've fixed a number of bugs, added several new features, and improved
documentation in several places, just thanks to needing these things
in a real app.

On a technical level, Pyonic interpreter runs under Python 2,
consisting of the app itself and a background Service running a second
instance of the interpreter. I'll be working on Python 3 support in
the near future, in fact I originally wrote the app using Python 3 but
switched to Python 2 partly due to incompatibilities in Kivy's osc
library (which should be easily fixed or avoided by just using a
better communication library) and partly the more well-tested nature
of python-for-android's Python 2 build.

The interpreter works by passing submitted Python code to the
background Python process where it is parsed as ast and compiled in
'exec' or 'single' mode as appropriate to replicate the output
printing behaviour of the normal Python interpreter. Doing things this
way is a little awkward and feels like reinventing the wheel, although
I'm not sure how to better achieve the same thing. An alternative
might be to just call the python binary in a subprocess and manipulate
its stdin/stdout - I'll be looking into this option, but it doesn't
eliminate the need for message passing and may need some small changes
in python-for-android, assuming also that android doesn't impose any
important limits on subprocessing.

In the short term future, I expect to work first on releasing an
improved version that adds a number of useful settings options (sneak
peek in the image below), followed by working on a Python 3 version,
and then to investigate some of these technical questions. I'd like to
look into iOS support, as everything should work almost the same way
there, but I don't have the hardware or developer mempership for iOS
development; if anyone would like to try it, let me know. Longer term,
Pyonic interpreter is an experimental step towards creating a larger
suite of mobile Python tools, in tandem with using this experience to
improve python-for-android. There are many features to be added
directly to the interpreter, but I'd also like to add surrounding
tools including a full code editor, the ability to use pip to install
other modules locally, and GUI support via additional Kivy activities.

.. figure:: {filename}/media/pyonic_android_beta_settings_small.png
   :alt: Screenshot of the settings screen in the development version
         of Pyonic interpreter.
   :align: center

   Settings screen in development to appear in the next release.
