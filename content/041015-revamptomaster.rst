
python-for-android revamp replaces master
#########################################

:date: 2015-10-04 21:00
:tags: kivy, python, android
:category: kivy
:slug: python_for_android_revamp_replaces_master
:author: Alexander Taylor
         
This post is to announce that the revamped python-for-android
toolchain, introduced `in this previous post
<{filename}/180715-p4arevamp.rst>`__, has now been merged into
`python-for-android's master branch
<https://github.com/kivy/python-for-android>`__. This is now the
master branch going forward.

The revamp project is largely (but not quite) feature complete with
the old toolchain, supporting almost all the same options when
building pygame-based APKs. It also supports a new and much better
SDL2 backend, which Kivy will move to in the future, but which also
supports other kinds of python projects such as Vispy as described in
the previous post.

We've done our best to minimise problems arising from this change. The
old toolchain (with distribute.sh and build.py) is still available in
the `old_toolchain branch
<https://github.com/kivy/python-for-android/tree/old_toolchain>`__. Issues
and PRs relating to this branch are still accepted, though existing
PRs will need to be retargeted or merged manually (we'll try to do
what's easiest case by case, if necessary).

If you use buildozer, this now pulls from the old_toolchain branch and
so will work exactly as before. However, you will need to install the
latest version from pypi or github (at least version 0.30) for this to
work. Older versions of buildozer will continue to build APKs fine
with existing projects, but if you create a new one they will download
the new and incompatible python-for-android master. The revamp includes
a fake distribute.sh executable giving these same instructions, so if
this happens the problem and solution should be clearly displayed.

The new toolchain is currently documented (temporarily) `here
<http://inclem.net/files/p4a_revamp_doc/>`__. We'll push the new
documentation to the normal readthedocs site
(`http://python-for-android.rtfd.org`_) as soon as possible, which
will also include the legacy doc for the old toolchain so nothing is
lost.

In the slightly longer term, the new toolchain will receive an
official release and hopefully be released itself on pypi; unlike the
old toolchain, it behaves as a fully installable python module with an
improved command line interface.
