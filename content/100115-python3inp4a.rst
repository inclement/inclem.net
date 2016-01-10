
python-for-android now supports python3
#######################################

:date: 2016-01-10 15:00
:tags: kivy, python, android
:category: kivy
:slug: python3_support_in_python_for_android
:author: Alexander Taylor
         

It's been a long time coming, but we can finally make the
announcement...python-for-android now supports python3 Android apps!
This includes Kivy, but also should work for anything else you can
package with python-for-android, such as apps made with pysdl2. Using
python3 remains experimental for now, but there should be no extra
application requirements (beyond actually being written for python3),
and remaining issues and optimisations will continue to be worked on.


Overview
--------

`python-for-android <https://github.com/kivy/python-for-android>`__ is
a packaging tool for turning Python applications into Android APKs. It
was originally created to make apps with the very cross-platform `Kivy
graphical framework <http://kivy.org/>`__ (though it didn't arise in a
vacuum, I think it built on on previous work by the `Ren'Py project
<http://www.renpy.org/>`__). However, the original python-for-android
had flaws including being quite inconvenient to modify for non-Kivy
apps (several other projects seem to have used modified versions, but
each was performing similar changes), hard to extend for multiple
architecture support, hard to extend internally (both in general and
from the perspective of new contributors, much of the toolchain was a
big shell script), and only supported building apps with Python 2.

We recently completed and released a fully revamped version of
python-for-android aimed at fixing all of these problems, as discussed
in several previous posts on this blog (originally `here
<{filename}/180715-p4arevamp.rst>`__). Almost all of the original
goals are now complete, with Python 3 support the major missing one,
though not for lack of trying. Some technical details and basic
instructions for testing the new support are given below, and you can
also see the `online documentation
<http://python-for-android.readthedocs.org/en/latest/>`__ for further
information.

The Python3 support depends on the prebuilt Python distributions
provided with the `CrystaX NDK <https://www.crystax.net/en>`__, a
drop-in replacement for Google's own Android NDK with many fixes and
improvements. The technical details of this choice are given below
(and we'll try to support a locally-built python3 option in the
future), but thanks to the CrystaX team for fixing this problem for
everyone!

Technical details
-----------------

python-for-android works by bundling a Python interpreter, compiled
for Android devices and architectures (usually arm, though other
choices are supported), into an Android APK. The APK includes a simple
Java bootstrap application, which mostly starts a Python script via
JNI. The script then runs essentially as normal, almost all of the
Python standard library is present and works fine, and
python-for-android supports including other modules (or non-Python
dependencies); pure Python modules will mostly work without special
treatment, though things requiring compilation require a special
recipe for python-for-android to compile them for Android. Many common
modules such as numpy and sqlalchemy are supported this way.
Following its revamp python-for-android is now designed to support
multiple kinds of java bootstrap, but the main support is for GUI apps
via pygame (for Kivy's old Android support) or SDL2 (both for Kivy and
for anything else that can use it); SDL2 in particular now does much
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
on Android). For python2, I think python-for-android's original
patches came from `here
<http://randomsplat.com/id5-cross-compiling-python-for-embedded-linux.html>`,
though extended with further modifications. However, the main thing
holding up my efforts to get python3 working was the inability to find
a similar working patchset; I tried a few sources, achieving a working
compilation using SL4A's `python3 patches
<https://github.com/kuri65536/python-for-android/tree/master/python3-alpha>`,
bu I couldn't get Python working on the device. I'm sure this was my
own technical mistakes, since other projects do have it working, but
it's what was holding up the feature.

I eventually resolved this by using the new Python on Android support
from the `CrystaX NDK <https://www.crystax.net/en`__. As mentioned
above, this is a drop-in replacement for Google's own NDK (the Native
Development Kit providing compilers etc for targeting Android with
non-Java code), including many improvements to the build
environment. As of version 10.3.0, they provide prebuilt Python
packages for Android on all architectures - and all of the NDK
improvements mean that Python no longer even needs patching for this
compilation to work. Python is provided as a zipped standard library
(Python can automatically load modules from zip files), and a folder
of the compiled components like ctypes (it's hard to dynamically load
from zip files. Supporting Python3 means modifying the build to load
CrystaX's prebuilt components (both in the Android project structure
and in python-for-android's support for compiling other modules), and
modifying the C initialisation code for python3 and for this package
structure which is different to that of the python2 support. This
takes some work, but all told was remarkably easy and the Python
bundles worked with no issues, so we owe a lot to CrystaX; thanks
again!

I'd still like to come back to the issue of local python3 compilation;
CrystaX's versions are fine, but I've learned a lot from making them
work, and have a much better idea of what I may have been doing
wrong.


Building apps with Python 3
---------------------------

Building python3 APKs is only supported in the new python-for-android
toolchain, which can be installed and used as described `in its
documentation
<http://python-for-android.readthedocs.org/en/latest/quickstart/>`__. If
you use Buildozer, it currently does not support this new toolchain,
though I think tito may be working on this and others have expressed
interest. There is also the new restriction that you must (for
obvious reasons) use the CrystaX NDK, which can be obtained `here
<https://www.crystax.net/en/download>`__; simply refer to its filepath
when setting the NDK directory, and everything else will work
automatically.

To build for python3, add the ``python3crystax`` recipe to the
requirements option,
e.g. :code:`--requirements=python3crystax,kivy`. Existing recipes
should work automatically. This mechanism may change in the future as
the python3 support becomes better integrated.


Future work
-----------

For now, this python3 support remains experimental. I anticipate no
major issues, but it's internally a quite different method to the
python2 support and needs further work to duplicate some of the old
optimisations, and undoubtedly to fix bugs in the toolchain that will
appear as it stabilises. Amongst other things, python3 shared
libraries are not currently collected and merged (with python2 we did
this originally to get around an Android limit but also for
optimisation), python files are not precompiled to bytecode (it can
make a big loading speed difference), and some features of the old
pygame bootstrap have not yet been implemented in SDL2. All this and
more will come in the future, but shouldn't be hard to add now that
the toolchain all works.

I've also phrased this as python2 (built locally) vs python3 (from
CrystaX), but actually CrystaX also supports python2.7 and I hope to
add this option in the near future. As discussed in the technical
details, it also should absolutely be possible to have a local python3
build, which I'd like to eventually come back to.


Other references
----------------

This post has focused on python3 packaging with python-for-android,
but if you're interested in Python on Android there are other projects
you may find interesting.
