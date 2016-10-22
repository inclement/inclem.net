PyDE interpreter: A Python interpreter GUI for Android, written in Python
#########################################################################

:date: 2016-10-17 23:06
:tags: python, android, kivy
:category: kivy
:slug: pyde_interpreter_0_5_released
:author: Alexander Taylor

I've just released a new app, `PyDE Python 2 interpreter <>`__.  PyDE
interpreter is a Python interpreter app for Android, providing a
convenient gui adapted to mobile devices. The app itself is written
entirely in Python using `Kivy <https://kivy.org/#home>`__.

.. figure:: {filename}/media/pyde_android_small.png
   :alt: Screenshot of the interpreter app.
   :align: center

I put this together because I've always thought it would be nice to
have a Python interpreter app that is itself written in Python, and in
principle Kivy should let this happen. In practice this worked even
better than I expected, Kivy handled almost everything perfectly - I
actually underestimated its maturity here! As part of the project,
I've tried to round a number of corners that Kivy apps sometimes tend
to have, creating an app that (hopefully) behaves smoothly in all
situations.

This has also been a great stimulus for working on `python-for-android
<http://python-for-android.readthedocs.io/en/latest/>`__; I've fixed
a number of bugs, added several new features, and improved
documentation in several places, just thanks to needing these things
in a real app.

On a technical level, PyDE interpreter runs under Python 2, consisting
of the app itself and a background Service running a second instance
of the interpreter. I'll be working on Python 3 support next, in fact
I originally wrote the app using Python 3 but switched to Python 2 due
to incompatibilities in Kivy's osc library (see below) - these should
be easily fixed or avoided by just using a better communication
library.

When the user enters input, it is passed to the background Python
process where it is parsed as ast and compiled in 'exec' or 'single'
mode as appropriate to replicate the output printing behaviour of the
normal Python interpreter. Doing things this way is quite awkward and
feels like reinventing the wheel, although I'm not sure how to better
achieve the same thing. An alternative might be to just call the
python binary in a subprocess and manipulate its stdin/stdout - I'll
be looking into this option, but it may need some small changes in
python-for-android, and I'll need to check if/how android imposes any
limits on subprocessing.

In the short term future, I expect to work to release a Python 3
version, and then to investigate some of these technical
questions. I'd like to look into iOS support, as everything should
work almost the same way there, but I don't have the hardware or
developer mempership for iOS development; if anyone would like to try
it, let me know. Longer term, PyDE interpreter is hopefully the first
step in creating a larger suite of mobile Python tools, in tandem with
using this experience to improve python-for-android. There are many
features to be added directly to the interpreter, but I'd also like to
add surrounding tools including a full code editor, the ability to use
pip to install other modules locally, and user-defined GUI
functionality via additional Kivy activities.
