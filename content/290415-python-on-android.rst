Python on Android
#################

:date: 2015-04-29 23:32
:tags: kivy, python, android, pyjnius, plyer
:category: kivy
:slug: python-on-android
:author: Alexander Taylor

         
There are an increasing number of resources about different ways of
running Python on Android. Kivy (and its subprojects) are commonly
mentioned, as one of the most mature and popular ways to do so, but
one thing that gets less attention is the details of what you can do
with Python itself once it's running on the device - what are the
limitations of this? Can we use any Python module? What about calling
Android APIs, can we perform all of the functions of a Java
application? These are all somewhat leading questions, they are things
addressed by Kivy or its associated projects, and in this post I'll
summarise some of the most interesting and important details.


python-for-android
==================

Before anything else, let's look quickly at the tool Kivy actually
uses to get Python on Android; the unimaginatively-named
`python-for-android project
<https://github.com/kivy/python-for-android>`__. The basic
functionality of this tool is to first build a *distribution*, an
Android project directory that includes all the components Kivy needs
to run, compiled for Android by its NDK. This includes in particular
the Python interpreter itself, plus Kivy and the libraries it depends
on - currently Pygame and SDL amongst others, although we are working
to modernise this bit. The distribution also includes a Java
bootstrap, a normal app structure whose job is to display Kivy's
OpenGL surface and to mediate between Kivy and Android. All these
components can then be bundled into an APK with the user's Python
script and different settings (icon, name, orientation etc.) to taste.

This is only the basic procedure, the APK can (and does) include much
more than just these essentials. Amongst other things, most of the
Python standard library is built in by default, and pure Python
modules can be included easily so in general you can perform tasks
using just the same libraries you would on the desktop. Libraries with
compiled components are more complex, but can be built and included as
long as python-for-android has a compilation recipe for them (or you
provide your own) - these are often quite simple, just setting some
compilation flags and running the normal build procedure, although
some modules need additional patching. Python-for-android includes
quite a few recipes by default, including very popular modules like
numpy, sqlite3, twisted and even django!

The above is the basics of how python-for-android works but is far from
the whole story, and you can check the documentation for more
information about building your own APKs - in particular, we recommend
using `Buildozer <https://github.com/kivy/buildozer>`__, which gives
python-for-android a more convenient interface and can manage some
dependencies (in particular the Android SDK and NDK)
automatically. This is also quite focused on Kivy itself, but we're
trying to move to make it easier for other projects to use the same
toolchain - the core process of building and including Python should
be similar, but there's no need for the bootstrap app at the end to
support only Kivy's specific needs.


Calling Android APIs with PyJNIus
=================================

In normal Android application development, interaction with the
Android API is an important part of how your app behaves - getting
sensor data, creating notifications, vibrating, pausing and
restarting, or just about anything else. Kivy takes care of the
essentials for you, but many of these are things you'll still want to
manage yourself from Python. For this reason we have the `PyJNIus
<https://github.com/kivy/pyjnius>`__ project, also developed under the
Kivy organisation, which automatically wraps Java code in a Python
interface.

As a simple example, here's the Python code to have an Android device
vibrate for 10s:

.. code-block:: python

     from jnius import autoclass
     
     # We need a reference to the Java activity running the current
     # application, this reference is stored automatically by
     # Kivy's PythonActivity bootstrap:
     PythonActivity = autoclass('org.renpy.android.PythonActivity')
     activity = PythonActivity.mActivity

     Context = autoclass('android.content.Context')
     vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)

     vibrator.vibrate(10000)  # the argument is in milliseconds
     
If you're familiar with the Android API, you'll notice that this is
very similar to the Java code you'd use for the same task; PyJNIus
just lets us call the same API directly from Python. Most of the
Android API can be called from Python in the same way, letting you
achieve the same things as a normal Java application.

The main disadvantages of using PyJNIus directly are that it requires
some understanding of how the Android API is structured, and that it
is quite verbose - though the latter just reflects the nature of the
equivalent Java code. For this reason, the Kivy project set includes
*Plyer*.


Plyer: A platform-independent API for platform-specific features
================================================================

The `Plyer <https://github.com/kivy/plyer>`__ project takes a step
back from the specific implementation details of individual platforms
in order to try to create a simple, pythonic interface for a subset of
(mostly) shared functionality. For instance, the vibration example
above would become

.. code-block:: python

    from plyer.vibrator import vibrate
    vibrate(10)  # in Plyer, the argument is in seconds
    
Further, Plyer is not just for Android but would try to do something
appropriate on any of its supported platforms - currently Android,
iOS, Linux, Windows and OS X (on iOS, `PyOBJus
<https://github.com/kivy/plyer>`__ fulfils a similar role to PyJNIus
on Android). The vibrator is actually a bad example as only Android is
currently implemented, but other APIs such as checking the battery
(:code:`from plyer import battery; print(battery.status)`) or
text-to-speech (:code:`from plyer import tts; tts.speak('hello
world')`) would already work on both desktop and mobile devices, and
others such as the compass or gyroscope sensors or sending SMS
messages would work on both Android and iOS.

Plyer is very much under development, with new API wrapper
contributions very welcome, and is the subject of a (second) GSoC
project this year. We hope that it will become increasingly
feature-complete.


Not just for Kivy
=================

All of these tools have been shaped in their current form by the needs
of Kivy, but are really more generic Python tools; Plyer specifically
avoids any Kivy dependency, and PyJNIus only makes an assumption about
how to access the JNI environment on Android. We hope that these tools
can be more generally useful to anyone running Python on Android; for
instance, you can already experiment with PyJNIus using the `QPython
Android app
<https://play.google.com/store/apps/details?id=com.hipipal.qpyplus>`__. Python-for-android
is more tied to Kivy's current toolchain but this is a detail under
review, and we're happy to discuss the details of Android compilation
with anyone interested.

Overall, a lot is possible with Python on Android, despite how
different the Python environment is to the Java development that is
directly targeted. But there's much more that could be done - if
you're interested, now is a great time to dive in!
