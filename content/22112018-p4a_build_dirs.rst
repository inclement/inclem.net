Cached and templated files in python-for-android builds
#######################################################

:date: 2018-11-22 22:00
:tags: python, android, kivy
:category: kivy
:slug: p4a_project_dirs
:author: Alexander Taylor

I've more than once seen people confused by how python-for-android
constructs an Android project that can be compiled into an APK.  Since
p4a uses various cached and templated files, it's easy to get confused
trying to edit things only to find your changes are overwritten when
you run p4a again.

Here's a quick summary of what's what.

Bootstraps
==========

The core project files are all in the `bootstraps directory
<https://github.com/kivy/python-for-android/tree/master/pythonforandroid/bootstraps>`__. A
bootstrap is basically an Android project, containing java sources,
JNI stuff to be compiled, and project management files like the
``AndroidManifest.xml`` and ``build.gradle``.

Note: Some of these files are built from templates, e.g. in the main
`SDL2 bootstrap
<https://github.com/kivy/python-for-android/tree/master/pythonforandroid/bootstraps/sdl2/build>`__
you can find ``build.tmpl.gradle``, ``AndroidManifest.tmpl.xml``
etc. in the `templates subdirectory
<https://github.com/kivy/python-for-android/tree/master/pythonforandroid/bootstraps/sdl2/build/templates>`__.

If you edit the code in these bootstrap directories, the changes will
*always* take effect if you rebuild your whole project, but *might
not* affect anything if you repeat a previous build. This is due to
caching of previous build components. You can always guarantee that
everything is cleared to be rebuilt using ``p4a clean dists builds``
(or there are other tricks if you look into it).

Build directories
=================

Most of the individual python-for-android recipes are built in
individual build directories. The location of these depents on the OS:
on Linux the default is ``~/.local/share/python-for-android``,
especially ``~/.local/share/python-for-android/other_builds``. When
you build a recipe, it is copied here for the build to be run.  These
folders also cache builds, so if you e.g. build two different projects
using ``python3`` then the same build directory is used both times,
reducing time spent compiling.

You can edit code in
``~/.local/share/python-for-android/other_builds``, but it isn't
recommended unless you have a good idea what python-for-android will
overwrite or cache on each run. It is, however, sometimes useful
during development.

Dists
=====

Dists are p4a's fully compiled Android projects, including the bundled
output of all the different requirements specified by the user. On
Linux, their default location is
``~/.local/share/python-for-android/dists``.

Every time you build an APK using ``p4a apk ...``, this essentially
runs gradle from appropriate dist directory (i.e. the one with the
recipes you wanted). At this point, nothing new is built or copied
from the build directories, so changes you make to p4a's recipes or
build directories have no effect on the output. However, templated
files such as ``AndroidManifest.tmpl.xml`` are rebuilt *every
time*. That means that you must edit the templates themselves if you
want your changes to make it to the APK.

You can always run ``p4a clean dists`` to delete the existing Android
projects. Next time you run ``p4a apk ...``, a new dist will be
created.

Buildozer
=========

When using buildozer, everything works basically the same except that
the build and dist directories can be found in
``$PROJECT_DIR/.buildozer/android/platform/build`` instead of
``~/.local/share/python-for-android``. The python-for-android source
code is stored in
``$PROJECT_DIR/.buildozer/android/platform/python-for-android``.
