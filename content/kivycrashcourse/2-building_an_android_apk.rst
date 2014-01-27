Kivy Crash Course 2 - Building an Android APK
#############################################

:date: 2014-01-12 11:34
:tags: kivy, crash course, python, android
:category: Kivy Crash Course
:slug: 2_building_an_android_apk
:author: Alexander Taylor


Introduction
============

(`Original video <https://www.youtube.com/watch?v=t8N_8WkALdE>`_)

In this writeup of my second Kivy Crash Course video, I describe how
to use the `buildozer <https://github.com/kivy/buildozer>`_ tool to
compile a Kivy application into a fully functional standalone Android
APK. For reference, you can find the original video `here
<https://www.youtube.com/watch?v=t8N_8WkALdE>`__.

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

I'm also happy to hear about problems with this article, it's only a
quick write-up based on my own experiences and I'd like to improve it
to be more general if possible. You can let me know at
`alexanderjohntaylor@gmail.com <mailto:alexanderjohntaylor@gmail.com>`_.

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
- pip, the python package management tool.
- virtualenv, used internally by python-for-android

All are standard and popular, and should be available in the
repositories of most Linux distros or easy to install on OS X. You can
probably install virtualenv via pip.

At this point we can finally get around to installing buildozer
itself. You should be able to do this via pip (remember to prefix with
:code:`sudo` if not running as root):

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
<{filename}/kivycrashcourse/1-making_a_simple_app.rst>`_. The first
vital point is that you *must* name your main python file
:code:`main.py`. That's because Android app will look for and run this file
when you start the app. You can spread the rest of your app across
other python files and folders if you want, but this :code:`main.py` must
exist and will always be the entry point.

The second step is to create a basic buildozer.spec file, a
configuration file containing all the different parameters to use when
building your app. You can create the file using buildozer itself:

.. code-block:: bash

   buildozer init

This creates a file called buildozer.spec in the current directory,
populated with default values. 

Populating your buildozer.spec
------------------------------

Before creating the APK you'll need to go through your buildozer.spec
and set some of the values appropriately. In this section I'll quickly
explain some of the important values. This list is *not* exhaustive,
you can view more information in the comments of the file itself or in
buildozer and Kivy's own documentation, but it'll be plenty to compile
a simple app.

You should at least quickly skim through these settings, you *must*
change at least the version settings or your compilation will fail.

**title**: The name of your app, this will appear in (for instance)
your app drawer. I used 'Kivy Crash Course 2'.

**package.name**: A simple string identifier (no spaces etc.), which
along with :code:`package.domain` should be a unique identifier. I used 'kivycrash2'.

**package.domain**: Not a real domain name, but along with
:code:`package.name` should be a unique identifier. Using the default
org.test is fine for now, or more generally you might use a reversed
form of your own domain name.

**source.dir**: The directory containing your source code, including
the main.py file. The default '.' should be fine, this means 'the
current directory'.

**source.include_exts**: Buildozer will automatically include source
files with these extensions in your APK. That means you obviously want
to include py files so your python is loaded. By default, buildozer
includes a few image formats, 'kv' which is kv language (covered in a
future article). You can leave this as the default for now.

**source.exclude_exts**, **source.exclude_dirs**,
**source.exclude_patterns**: More options for controlling what files
are built into the APK. These are commented out by default, which is
fine for us.

**version.regex**, **version.filename**: These comprise the default
way to find your APK's declared version. Buildozer looks in the given
filename (your main.py by default) for a string of the form
:code:`__version__ = 'some_version'`. I did not add such a string in our
simple app from the first article, so you should *delete or comment
out* these two settings tokens as they will fail when they try to find
the version string.

**version**: This is another way to set your app version, and is
commented out by default. Unless you added a :code:`__version__` string (see
above), you should *uncomment* this line. The actual version number or
string isn't important, I left it at 1.0 for now.

**requirements**: This should be a comma separated list of
non-standard python modules to include in your app. You don't need to
change this to use most modules in the standard library, they are
included by default. Most pure-python modules will be installed via
pip if listed here, though modules with compilation steps need a
special compilation recipe in python-for-android. You can see the list
of existing recipes `here
<https://github.com/kivy/python-for-android/tree/master/recipes>`__. None
of this is important to our simple app, and we can leave only the
default entry 'kivy', but it's worth being aware of.

**presplash.filename**: The filename pointing at the image that will
be used on kivy's loading screen appearing when an app is first
run. It is commented out by default (which means it just uses the Kivy
logo), and that's fine for us now so you don't need to change it.

**icon.filename**: The filename pointing at the image to use as your
app icon in (for instance) your app drawer or launcher. Again, it's
commented out by default and just uses the Kivy logo, which is fine
for now so you don't need to change it.

**orientation**: The orientation of your app, either 'landscape',
'portrait', or 'all' which means the app is automatically rotated to match
how the device is currently being held. I set this to 'all' for our
simple app, but you can make your own choice. You can also dynamically
change the orientation from within your app if you want.

**fullscreen**: If set to 1 the app will fill as much of the screen as
possible (everything except a software navigation bar if there is
one), or if set to 0 it leaves the status bar visible. I set it to 0,
but either option is fine. At the time of writing this doesn't support
the new screen usage parameters introduced in Android 4.4, you only
have a binary choice.

After this there are lots of android options that we don't need to
worry about, the defaults are all fine. There are also iOS build
options that obviously aren't important for Android compilation,
though buildozer *can* perform part of the iOS build process if you're
interested. Actually, there's only one other important option:

**log_level**: This controls how much information is printed to your
screen as buildozer runs. It defaults to 1, basic information, but I
almost always set it to 2 to see more build information including a
lot more useful logs if something goes wrong.


Building the APK
----------------

That's it for the configuration file. Assuming you made the minor
changes I suggested, you're ready to build your APK!

The advantage of buildozer is that this part is *really easy*. All we
need to do is type and run in a shell:

.. code-block:: bash

   buildozer android debug

This calls buildozer, and tells it to build an Android APK in debug
mode. The debug part refers to the way the package is signed, it
doesn't need properly signing with a developer key (that isn't hard
but it's another topic) and you can immediately upload it to a device
and run it.

You'll find that the first time you run buildozer it has to download a
lot (the Android SDK and NDK plus some other tools), which are
hundreds or thousands of megabytes in size. This isn't really
avoidable if you want to build locally, but it will only happen once,
after which buildozer will always use the same ones. If you already
have the SDK/NDK installed, you can check out some of the buildozer
options I didn't mention that can point buildozer at the local copies
so it doesn't have to download them again.

If you have a device ready to run your app on, you may instead like
enable developer mode and adb in its settings (the method varies by
device, you can look it up), which lets your computer interact with
the phone to access logs, run commands, install apps etc. The last is
the most immediately important here, as it means we can plug the phone
into the building computer and run

.. code-block:: bash

   buildozer android debug deploy

The last argument, 'deploy', tells buildozer to automatically install
the APK onto your device when the build process is done.

That's literally everything. Assuming nothing goes wrong, your APK
will be built and placed in the 'bin' directory in the local path, and
you can do whatever you like with it. You can send it to your device
via email, adb, dropbox, or lots of other methods.

Debugging
---------

Even if the APK building works, your app may still have
problems. Common ones are stuff like forgetting to include images in
the APK so the app crashes when Kivy tries to access them. It's
extremely useful to debug this using the *logcat* tool that comes with
the Android SDK. You can run this with

.. code-block:: bash

   buildozer android logcat

to use the version buildozer installed as part of the build
process. More generally, if the SDK tools are in your `$PATH` you can
just run:

.. code-block:: bash

   adb logcat

Both of these will output the logcat log straight to your
terminal. This includes any standard output of your Python code, such
as print statements, plus any standard Python tracebacks and
errors. This is obviously extremely useful for working out what's
going wrong!

There are also logcat applications in the play store that can show the
log from on the device. I think they generally require root nowadays,
but they may be useful if you don't have a computer handy.

That's everything for this article. It's a pretty quick guide, but I
hope it covers everything you need to quickly and easily build your
first Android APK with buildozer. Once it's all working, you can
rebuild your app whenever you like with :code:`buildozer android debug`, and
it only takes a few seconds!

In the next article I'll go back to covering the features of kivy
itself, starting with some more interesting widget interactions.
