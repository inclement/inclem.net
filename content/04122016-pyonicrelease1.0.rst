Pyonic interpreter 1.0 released
###############################

:date: 2016-12-04 22:30
:tags: python, android, kivy, pyonic
:category: kivy
:slug: pyonic_interpreter_1_0_released
:author: Alexander Taylor

I've just released Pyonic interpreter 1.0. You can get it from Google
Play for `Python 2.7
<https://play.google.com/store/apps/details?id=net.inclem.pyonicinterpreter>`__
or `Python 3.5
<https://play.google.com/store/apps/details?id=net.inclem.pyonicinterpreter3>`__,
or download the APKs directly `from Github
<https://github.com/inclement/Pyonic-interpreter/releases/tag/v1.0>`__.

The primary change in this release is that both APKs are about 25%
smaller than before, thanks to optimisations in the Python
distributions that I've added to python-for-android - in particular,
making sure Python files are shipped as .pyo files (which may also
speed things up a bit) and stripping unneeded symbols from object
files with Python 3. Both of these were things python-for-android has
been missing for a while, so it's nice to get them working and
immediately see the benefits.

I've also been working on some backend improvements in Pyonic and
python-for-android in order to support multiple interpreter processes.
This will be convenient for using pip and running Python code from
files, but isn't ready yet and so hasn't made it into this release.
