
python-for-android status update
################################

:date: 2015-12-06 14:00
:tags: kivy, python, android
:category: kivy
:slug: python_for_android_update
:author: Alexander Taylor
         
It's been a while since Kivy's `python-for-android project
<https://github.com/kivy/python-for-android>`_ was revamped, so here's
a quick status update.

There have since been well over 200 commits from 15 different
contributors, cleaning up the missing pieces of the new toolchain and
adding new features that weren't previously possible. Thanks to
everyone who has contributed.

These fixes include progress on the remaining major goals of the
python-for-android revamp. In particular, compilation is now supported
for multiple target architectures - in principle anything targeted by
the Android SDK (i.e. ARM, ARMv7a, x86, x86_64 and MIPS options),
though I've tested only with the ARM and x86 ones. This means that
Kivy applications, or other Python projects built with these tools,
can be built for devices with e.g. intel atom processors. Even without
this compilation it was often possible to run Kivy apps as many
devices include libhoudini, but directly targeting them means such
apps should now always work. A further advantage is that Kivy apps can
be built for and tested on the Android emulator, which was not
previously possible.

The architecture target support does need some more work to create
fully multiarch APKs (i.e. including .so files for each target, so a
single APK can work on different types of device). The problem here is
that we need to duplicate as little as possible, as Kivy APKs are
already made large by including the python interpreter, and it is
undesirable to include two or more copies of everything. Using a
single python installation and loading the .so dependencies as
appropriate should be possible but needs more work. However, this is
not a problem if uploading an APK to a store like Google Play; in this
case you can include multiple APKs, one for each arch target, and the
user will receive one that is appropriate.

Another important feature that I've worked on, but unfortunately
unsuccessfully so far, is support for python3 APKs. The problem to be
solved is to patch the interpreter to compile for Android (it cannot
do so by default, due to problems with the Android platform like poor
locale support), to modify the python-for-android bootstrap to load it
correctly (it builds things a little differently to python2), and to
modify the initialisation code to have it start successfully. I've
only partially succeeded with the first two of these; using `patches
from the SL4A python-for-android tools
<https://github.com/kuri65536/python-for-android/tree/master/python3-alpha/patches>`_
(plus extras for our own modifications to python loading) allows the
interpreter to be built, but it fails during Py_Initialize when run on
the device, apparently raising an exception when calculating the
python install path. Work on this will continue, but it's hard to know
how long it might take to resolve this error. If you know of any other
projects patching python3.4+ for Android, I'd love to heard about it
to compare their methods.
