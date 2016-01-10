
python-for-android now supports Python 3 APKs
############################################

:date: 2016-01-10 15:00
:tags: kivy, python, android
:category: kivy
:slug: python3_support_in_python_for_android
:author: Alexander Taylor
         

It's been a long time coming, but we can finally make the
announcement...python-for-android now supports Python 3 Android apps!
This naturally includes Kivy, but also should work for anything else
you can package with python-for-android, such as apps made with
PySDL2. Using Python 3 remains experimental for now, but there should
be no extra application requirements (beyond actually being written
for Python 3), and remaining issues and optimisations will continue to
be worked on.


Overview
--------

`python-for-android <https://github.com/kivy/python-for-android>`__ is
a packaging tool for turning Python applications into Android APKs. It
was originally created to make apps with the very cross-platform `Kivy
graphical framework <http://kivy.org/>`__ (though it didn't arise in a
vacuum, I think it built in particular on previous work by the `Ren'Py project
<http://www.renpy.org/>`__). However, the original python-for-android
had flaws including being quite inconvenient to modify for non-Kivy
apps (several other projects seem to have used modified versions, but
each was performing similar changes), hard to extend for multiple
architecture support, hard to extend internally (both in general and
from the perspective of new contributors, as much of the toolchain was a
big shell script), and only supported building apps with Python 2.

We recently completed and released a fully revamped version of
python-for-android aimed at fixing all of these problems, as discussed
in several previous posts on this blog (originally `here
<{filename}/180715-p4arevamp.rst>`__). Almost all of the original
goals are now complete, with Python 3 support the major missing one
until now, though not for lack of trying. Some technical details and
basic instructions for testing the new support are given below, and
you can also see the `online documentation
<http://python-for-android.readthedocs.org/en/latest/>`__ for further
information.

Our Python 3 support depends on the prebuilt Python distributions
provided with the `CrystaX NDK <https://www.crystax.net/en>`__, a
drop-in replacement for Google's own Android NDK with many fixes and
improvements. The technical details of this choice are given below,
and we'll try to further support a locally-built Python 3 option in the
future. Thanks to the CrystaX team for making it so (relatively) easy!


Technical details
-----------------

python-for-android works by bundling a Python interpreter, compiled
for Android devices and architectures (usually arm, though other
choices are supported), into an Android APK. The APK includes a simple
Java bootstrap application, which mostly starts a Python script via
JNI. The script then runs essentially as normal, almost all of the
Python standard library is present and works fine, and
python-for-android supports including other modules or non-Python
dependencies; pure Python modules will mostly work without special
treatment, though things requiring compilation require a special
recipe. Many common modules such as numpy and sqlalchemy are supported
this way.  Following its revamp python-for-android is now designed to
support multiple kinds of java bootstrap, but the main support is for
GUI apps via Pygame (for Kivy's old Android support) or SDL2 (both for
Kivy and for anything else that can use it); SDL2 also now does much
of the heavy lifting of handling events etc itself, via its own
Android support.

The main problems with compiling and including Python are first that
it must be patched to compile (as Android's libc doesn't
support some things very well or at all), and second that it must be
unpacked and started on the device via its C API. The second point is
fiddly but ultimately not that different to working this way on the
desktop. The first is (in my opinion) harder because it needs some
understanding of Python's internals, of Android's limitations, of
appropriate fixes, and of how to test and debug these
problems. 

Such patches have been made by a number of different people for
different Android versions, and I believe there has been activity on
Python itself to fix some issues (including `this current issue
<http://bugs.python.org/issue23496>`__ to make Python build natively
on Android). For Python 2, I think python-for-android's original
patches came from `here
<http://randomsplat.com/id5-cross-compiling-python-for-embedded-linux.html>`__,
though extended with further modifications. However, the main thing
holding up my efforts to get Python 3 working was the inability to find
a similar working patchset; I tried a few sources, achieving a working
compilation using SL4A's `python3 patches
<https://github.com/kuri65536/python-for-android/tree/master/python3-alpha>`__,
but I couldn't get Python working on the device. I'm sure this was my
own technical mistakes, since other projects do have it working, but
it's what was holding up the feature.

I eventually resolved this by using the new Python on Android support
from the `CrystaX NDK <https://www.crystax.net/en>`__. As mentioned
above, this is a drop-in replacement for Google's own NDK (the Native
Development Kit providing compilers etc for targeting Android with
non-Java code), including many improvements to the build
environment. As of version 10.3.0, they provide prebuilt Python
packages for Android on all architectures - and all of their NDK
improvements mean that Python no longer even needs patching for this
compilation to work. Python is provided as a zipped standard library
(Python can automatically load modules from zip files), and a folder
of the compiled components like ctypes (as it's hard to dynamically
load from zips). From the perspective of python-for-android,
supporting Python 3 means modifying the build to load CrystaX's
prebuilt components (both in the Android project structure and in
python-for-android's support for compiling other modules), and
modifying the C initialisation code for Python 3. This takes some
work, but all told wasn't very hard and the Python bundles worked with
no issues, so we owe a lot to CrystaX; thanks again.

I'd still like to come back to the issue of local python3 compilation;
CrystaX's versions are fine, but I've learned a lot from making them
work, and have a much better idea of what I may have been doing
wrong. However, the focus for now will be on resolving the remaining
issues with what's already working.


Building apps with Python 3
---------------------------

Building Python 3 APKs is only supported in the revamped
python-for-android toolchain which was merged to the master branch a
while ago. It can be installed and used as described `in its
documentation
<http://python-for-android.readthedocs.org/en/latest/quickstart/>`__. If
you use Buildozer, it currently does not support this new toolchain,
though tito has been working on this. There is also the new
restriction that you must (for obvious reasons) use the CrystaX NDK,
which can be obtained `here <https://www.crystax.net/en/download>`__;
simply refer to its filepath when setting the NDK directory, and
everything else should work automatically.

To build for Python 3, add the ``python3crystax`` recipe to the
requirements option,
e.g. :code:`--requirements=python3crystax,kivy`. It should work
automatically with all existing recipes (though at this stage there
may be bugs or problems with a few). The exact syntax may change
in the future as the python3 support becomes better integrated, but
not significantly.

There's also one big change whose importance I'm not sure about; the
Python 3 mechanism doesn't currently build a local python3 to use as a
hostpython, instead using the system python. This means that you must
have python3.5 installed locally (and in your $PATH) in order for
python-for-android to build Python 3 APKs. This will be fixed soon,
adding a hostpython3 build (to avoid weird bugs with system-specific
differences), but you need to bear it in mind for now.


Future work
-----------

For now, this Python 3 support remains experimental. I anticipate no
major issues, but it's internally a quite different method to the
Python 2 support and needs further work to duplicate some of the old
optimisations, and undoubtedly to fix bugs in the toolchain that will
appear as it stabilises. Amongst other things, Python 3 shared
libraries are not currently collected and merged (with Python 2 we did
this originally to get around an Android limit but also for
optimisation), python files are not precompiled to bytecode (it can
make a big loading speed difference), and some features of the old
pygame bootstrap have not yet been implemented in SDL2. All this and
more will come in the future, but shouldn't be hard to add now that
the toolchain all works.

The SDL2 bootstrap is also missing a few features that users of the
old toolchain will be used to, like the splash screen image and at
least one Kivy-specific function. These too are being actively worked
on, especially as more people start to move their apps to SDL2.

I've also phrased this as Python 2 (built locally) vs Python 3 (from
CrystaX), but actually CrystaX also supports Python 2.7 and I hope to
add this option in the near future. As discussed in the technical
details, it also should absolutely be possible to have a local Python 3
build, which I'd like to eventually come back to.
