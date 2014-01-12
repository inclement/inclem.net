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
your Kivy app for Android. Both use Kivy's `python-for-android
<https://github.com/kivy/python-for-android>`_ project, and actually
the first method is to use this directly by calling its component
scripts with the right command line options. You can find the basic
instructions for this on the linked github page.

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


