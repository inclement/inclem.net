
python-for-android 0.4 released, now available on PyPI
######################################################

:date: 2016-06-18 23:06
:tags: python, android, kivy
:category: kivy
:slug: python_for_android_0_4_released
:author: Alexander Taylor
         
We've just officially released python-for-android 0.4, and pushed it
to PyPI for the first time!

`python-for-android
<http://python-for-android.readthedocs.io/en/latest/>`__ is a
packaging tool for turning Python scripts and apps into Android
APKs. It was originally created for use with the `Kivy graphical
framework <https://kivy.org/#home>`__, but now supports multiple kinds
of Python app including Kivy, PySDL2, a webview interface with Flask
or other webserver backend, plain Python scripts without a GUI, or other
possibilities such as Python builds for use in other applications.

This release is the culmination of all the work over the last year to
replace Kivy's old Android toolchain with something more flexible and
useful for other projects. Major features added in this time include
the fully Python toolchain itself, support for SDL2 and other
bootstraps, (experimental) python3 support via the `CrystaX NDK
<https://www.crystax.net/>`__, multiple architecture support, and many
general improvements to the backend. Many thanks to all the
contributors who have made this possible!

From now on we intend to move to regular versioned releases rather
than the previous rolling master branch. Short term targets for the
next release include bringing the python3 build up to full
functionality and stability, and some argument restructuring to make
command line usage simpler and clearer.

As of this release, you can now install python-for-android with simply::

    pip install pythonforandroid
    
For full instructions and further information, see the
`python-for-android documentation
<https://python-for-android.readthedocs.io/en/latest/>`__.
