Kivy Crash Course 2 - Building an Android APK
#############################################

:date: 2013-01-13 11:34
:tags: kivy, crash course, python, android
:category: Kivy Crash Course
:slug: kivy-crash-course-2_building_an_android_apk
:author: Alexander Taylor
:summary: Kivy crash course 2 - Building an Android APK


Introduction
============

In this writeup of my second Kivy Crash Course video, I describe how
to use the `buildozer <https://github.com/kivy/buildozer>`_ tool to
compile a Kivy application into a fully functional standalone Android
APK. For reference, you can find the original video `here
<https://www.youtube.com/watch?v=t8N_8WkALdE>`_.

This particular article may have some overlap/redundancy with the main
Kivy documentation on buildozer, but I wanted to write it up anyway as
a standalone guide. I'll also try to keep it up to date with any
future developments if necessary. For reference, the Kivy website has
its own page on `building an APK
<http://kivy.org/docs/guide/packaging-android.html>`_, including more
information on the tools and methods that I do not cover here.


Background information
======================

Before explaining the build procedure, I'd like to quickly explain a
few general things about the Kivy/Android build process. Feel free to
skip to the next section if you just want to get started, but this one
may contain useful information if you have any problems or would like
a little more general information.

Problems and support
--------------------

First, it's worth noting that you may hit some problems on the
way. You *shouldn't*, and don't worry about the possibility unless it
happens, but compiling for Android involves a lot of behind the scenes
stuff that can occasionally fail - including potentially for unusual
reasons that may be specific to your hardware. If you do happen to hit
some problem, don't panic, Kivy has a great community that's very good
at helping to fix these kinds of problem. In particular you may find
it useful to ask questions or report problems at:

- The kivy-users `mailing list
  <https://groups.google.com/forum/#!forum/kivy-users>`_.
- The #kivy irc channel on irc.freenode.net.
- The `github issue tracker
  <https://github.com/kivy/kivy/issues?milestone=22&state=open>`_ (for
  bugs in kivy itself or feature requests).

This information can also be found on the `Kivy website
<http://kivy.org/docs/contact.html>`_. 

Different ways to build
-----------------------

For the build process itself, there are effectively two ways to build
your Kivy app to a full standalone Android APK. Both use Kivy's
`python-for-android <https://github.com/kivy/python-for-android>`_
project, and actually the first method is to use this directly by
calling its component scripts with the right command line options. You
can find the basic instructions for this on the linked github page, or
on the Kivy website `APK building page
<http://kivy.org/docs/guide/packaging-android.html>`_. 

This method is fine, and some users make sole use of it, but I much
prefer to use the `buildozer <https://github.com/kivy/buildozer>`_
tool. This is another project from the Kivy developers, and actually
it calls python-for-android behind the scenes, but it adds a useful
configuration file layer for setting up all the parameters of your
app. It also can automatically download and link many of the Android
build dependencies (at least the SDK, NDK, plus python-for-android),
which you would have to do manually if using python-for-android
directly. This article will cover the basic use of buildozer.

There are also potentially a couple of other ways to run Kivy apps or
scripts on Android, most obviously the `Kivy Launcher
<https://play.google.com/store/apps/details?id=org.kivy.pygame>`_ app
that can run Kivy scripts uploaded to your sd card or user data
partition. This can be useful, but I find buildozer so streamlined
that it's actually easier to build and install a full APK that way -
plus that makes your app fully standalone and you can install/use your
own modules and advanced features that may not be built into the launcher.


Using buildozer
===============

So, let's make an APK with buildozer! The first thing to take care of
is installing the tool along with any dependencies it requires.

Before anything else, I need to note that buildozer is only confirmed
to run on Linux or OS X. It will not run on Windows, and probably
won't in the near future. If you're using Windows that means you have
a couple of options for using it; first, you could install a simple
Linux virtual machine, which I encourage anyway on general principle
but may not be convenient for you. Second, Kivy runs an `online cloud
builder <http://android.kivy.org/>`_ that uses python-for-android to
compile uploaded code with a few user parameters. This might be useful
and even sufficient for basic APK building, though it is probably less
flexible and robust than using the tools locally.

The Kivy project does provide a `virtual machine image
<http://kivy.org/docs/guide/packaging-android.html#testdrive>`_ with
python-for-android and the associated android build tools
preinstalled. You may find this useful, especially if newer to Linux,
but if you're using buildozer it doesn't offer much advantage over a
vanilla Linux distro since buildozer would already handle much of this
for you.

You'll also need to install a few dependencies for
buildozer/python-for-android to work. I think the main ones are:

- git, the version control software.
- A java jdk, openjdk7 should be good.
- pip, the python packing tool.

Both are standard and popular, and should be available in the
repositories of most Linux distros or easy to install on OS X.

At this point we can finally get around to installing buildozer
itself. You should be able to do this via pip (remember to prefix with
`sudo` if not running as root):

.. code-block:: bash

   pip install buildozer

Buildozer can change quite quickly so you may instead find it useful
to use its git repository directly. This is also very easy, even
knowing nothing about the details, with the following instructions:

.. code-block:: bash

   git clone https://github.com/kivy/buildozer.git
   cd buildozer
   sudo python2.7 setup.py install

This will install the current master version of buildozer straight to
your system.   

Now you can go to your app directory, wherever you saved your Kivy
application, such as the simple moving text program I made in the
`previous article
<{filename}/kivycrashcourse/1-making_a_simple_app.rst>`_. The 
first vital point is that you *must* name your main python file
`main.py`. That's because Android app will look for and run this file
when you start the app. You can use other python files and folders if
you want, but this `main.py` must exist and will always be the entry point.
