
python-for-android revamped
###########################

:date: 2015-07-18 00:15
:tags: kivy, python, android
:category: kivy
:slug: python_for_android_revamped
:author: Alexander Taylor

I've recently been working on a significantly revamped version of
`python-for-android
<http://python-for-android.readthedocs.org/en/latest/>`_, the
`Kivy-project <http://kivy.org/#home>`_ tools that take a Python
program and package it - along with any dependencies and the Python
interpreter itself - into an Android APK that can be run and
distributed just like a normal Android app. This rewrite is driven by
the problem that although the current python-for-android is fairly
robust as far as the build process goes, it's quite set in its ways
and hard to modify to make large changes such as to support backends
other than Kivy. 

To this end, the revamp project has several major goals:

- Rewrite python-for-android to a fully Python toolchain that can be
  more easily modified and extended.
- Support multiple bootstrap targets for different kinds of Python
  scrips to run on Android, starting with a new SDL2 backend for Kivy
  applications.
- Support Python 3 on Android.
- Support some kind of binary distribution, enabling
  easier and cross-platform distribution...this should work on
  Windows!
- Be a standalone PyPI module with a more convenient and standard
  interface, potentially interfacing with setuptools.
- Support (less painfully) multiple Android architectures, or fat APKs
  supporting more than one.
  
Each of these is individually a popularly requested feature, and this
is a great opportunity to go for all of them at once!

I'm making this post to announce that the python-for-android revamp
project has reached a usable state, with several of these goals either
implemented or significantly advanced, and all of them at least made
much more accessible. The core change is that all of the original
toolchain has been rewritten in Python, with the initial structure
based on the recent Kivy-iOS rewrite. It's also much lighter, all
heavy pygame stuff is downloaded on demand instead of built in, and is
designed to be accessed by a single set of commands and the new
python-for-android executable rather than by the separate invocation
of different scripts in different places. I won't go into the
technical details here, but you can find the (WIP) documentation
temporarily hosted `here
<http://inclem.net/files/p4a_revamp_doc/>`_. If anyone would like to
test it you can try the instructions there, but the project is in an
experimental state right now and it's likely you may encounter bugs or
missing features, the current focus is ironing these out. I'm very
happy to discuss these on the `kivy-users mailing list
<https://groups.google.com/forum/#!forum/kivy-users>`_ or #kivy irc
channel on irc.freenode.net.

Another of the core goals of this rewrite was to support multiple app
backends; in Kivy's case in particular we want to move from Pygame to
a new SDL2 bootstrap, but this could also include support for other
Python module backends. As of now, the new python-for-android supports
the old Pygame bootstrap mostly as before, but also implements an SDL2
based PythonActivity that works very well with Kivy - highly anecdotal
testing found, amongst other things, app start time reduced to 60% of
what it was with Pygame. It also simplifies maintenance as SDL2's java
components fulfil the same role as those maintained in the Pygame
backend, but no longer require much special treatment as functionality
such as touch interaction and pausing are now accessed with the SDL2
api just as on desktop platforms.

Further, python-for-android can now build non-Kivy apps! The first
project with this support built in is the `Vispy scientific
visualisation library <http://vispy.org/>`_. This uses the same new
SDL2 backend but Kivy is not involved, and the build process does not
use Cython (unlike with Kivy); instead, SDL2 and OpenGL are called
entirely with ctypes, using `pysdl2
<https://pysdl2.readthedocs.org/en/latest/>`_ and Vispy's own gloo
wrapper respectively. I didn't even have to patch things much for
this, Vispy is mostly self contained and already quite platform
independent, barring a couple of possible small bugs and a hack to
avoid the lack of a supported font provider on Android. Vispy also
uses numpy heavily, but this was already supported by
python-for-android and seems to work fine. The Vispy support is itself
quite experimental and there are some performance issues that will
need resolving, but it was very simple to set up with the new
toolchain. Here's a screenshot of one of Vispy's 3D examples running
on Android - there are a few small visual artifacts, but I think these
are small bugs in Vispy's OpenGL ES 2 support that the Vispy team are
actively addressing:

.. figure:: {filename}/media/vispy_android_example.png
   :alt: Image of Vispy running on Android
   :align: center
           
Support for binary distribution and multiple architectures are both
partially implemented but (at the time of writing) not yet
working. However, the toolchain is built around them, so there should
be no major issues. The initial idea with binary distribution will be
to simply make available a number of prebuilt distributions 
(i.e. Android projects with the Python interpreter) that include
common dependencies, so that when the user adds modules as
requirements when calling python-for-android they can automatically be
checked and an appropriate choice downloaded, with this process being
transparent to the user and not requiring any special options. This
should not only make many builds faster but also work on Windows, one
of our most requested features but something that was not possible
when the toolchain required that everything be locally
compiled. Likewise, the toolchain has semi-implemented support for
multiple architectures internally, but none other than armeabi are yet
supported and there will be bugs to work out when more are
enabled. Still, these will (fingers crossed) be things to look forward
to in the relatively near future.

I should note here that this model of binary distribution is what I
initially targeted as a natural extension of python-for-android's
distribution system - although we never made much of it, the first
step is already to build a standalone android package which later can
be distributed separately and populated with app details by a user,
and the above just involves making such prebuilt distributions
available to download and use automatically. I found more recently the
method of the pybee project/Toga toolkit's `Python-Android-template
<https://github.com/pybee/Python-Android-template>`_. This is a
similar idea (built by a modified python-for-android) but implemented
much better as a standalone project with app details populated by
cookiecutter and the packaging of the user's Python modules taken care
of using ant itself, the normal APK build and deployment interface - I
didn't know this was even possible! This means that the user can just
write their Python code, drop it in place, and run the APK build, a
very neat process. It should be quite easy to modify
python-for-android's dist output to easily create such templates, its
dist system is functionally the same thing with a different and less
standard-Android interface, and I hope that doing so could make it
even more convenient for users to build and distribute different kinds
of Python apps. 

This leaves the elephant in the room, support for Python 3 on Android,
which is perhaps the most requested feature for Kivy itself. The new
toolchain makes significant progress on this in a couple of ways. The
first is by removing hardcoded use of Python 2, so that now (barring
remaining bugs) a Python 3 build should be well behaved once a recipe
and appropriate Android patch set are added. The second is that the
old Kivy Android bootstrap probably needed significant changes to
support Python 3, but this is sidestepped entirely by moving to the
new SDL2 backend which should have no issues supporting Python3 more
or less the same as on the desktop. However, the missing link here is
still actually being able to compile Python 3 for Android, and I don't
yet know how to do this. Some of Kivy's main Python 2 patches come
from `this site <http://randomsplat.com/>`_, but this has Python 3
patches only up to 3.2.2 and it would be ideal to target 3.4 or 3.5
(and to be able to support new versions as they appear). I've looked
around and seen a few different discussions of this, but I'm not sure
what's the best direction to try. If anyone has any information about
places to find more up to date patch sets I would be very
interested. I can't make any other predictions about this as I don't
know much about the Python compilation process or what difficulties
might be involved in doing the work we need.

That's all for now. I'll note again that this is an initial
announcement of the new toolchain; I hope that people may be
interested to look and try it, and it should support most of what the
old toolchain does when it comes to compiling Pygame APKs, but there
are likely to be bugs and missing features particularly surrounding
(but not limited to) the new additions. If you're interested in making
this toolchain work with other modules or backends, or just have any
questions, comments or criticisms, let us know! If you want to
keep informed, watch this space, I'll make further announcements as
things develop. If there is developer interest and people start
switching from the old toolchain, I hope development will speed up a
lot and quickly approach proper feature parity.

tl;dr (I was told I should have one): Kivy's python-for-android build
tools have been revamped to have a better interface, build apps based
on SDL2, build non-Kivy apps (currently Vispy apps), and be more
extensible. Further semi-complete features include binary
distribution, Windows support, and multiple architecture
targets. Python 3 is brought closer but needs direct compilation work.
