
Android apps with Python, Flask and a WebView
#############################################

:date: 2016-05-01 22:00
:tags: kivy, python, android
:category: kivy
:slug: python_for_android_webview_support
:author: Alexander Taylor
         

python-for-android has just gained support for a new webview app
interface, an alternative to the existing SDL2 or Pygame
backends. Under this mode of operation the app gui consists entirely
of a browser window directed to open a webpage on localhost, and the
Python backend can then run any web framework (I tested with Flask,
but others like Bottle or even Django should work), serving this
website and managing the app backend.

.. figure:: {filename}/media/flask_on_android.png
   :alt: Example Flask app running on Android
   :align: center
   :width: 200px
           
This idea is not itself new; I think SL4A has supported a kind of
webview interface for some time and certainly `does so now
<https://github.com/ainsophical/DROID_PYTHON>`__, and we've previously
seen users running web servers alongside Kivy. The difference to other
projects is that apps can take advantage of python-for-android's
relatively extensive toolchain including python3.5 support, the
ability to build popular libraries like numpy, support for multiple
architectures, and access to the Android API via `PyJNIus
<https://pyjnius.readthedocs.io/en/latest/>`__ or `Plyer
<https://github.com/kivy/plyer>`__ rather than SL4A.

In the image of my testing app above, each of the vibration and orientation
buttons sends a request to a Flask url that calls the Android
API with PyJNIus to achieve the desired result.

Building a webview app
----------------------

You can use the webview backend by adding :code:`--bootstrap=webview`
to your python-for-android command line (see `the documentation
<http://python-for-android.readthedocs.io/en/latest/quickstart/>`__
for more details), or including :code:`webviewjni` in your
:code:`--requirements` argument list. Note that this is incompatible
with using SDL or Kivy because the webview bootstrap does not start or
manage an OpenGL context. If for any reason you want to run a web
server alongside a Kivy app, this is possible but you'll need to use a
different bootstrap and manage the webview yourself via PyJNIus from
your Kivy code.

You should also add your chosen web framework to the
:code:`--requirements` argument, or include it your app directory so
that it will be imported locally. If there isn't a recipe for it and
it's a pure Python module, make sure you also add its Python
dependencies as these aren't automatically included right now (letting
pip resolve dependencies causes issues when they include compiled
modules that must be built separately). python-for-android now
includes a recipe for Flask that automatically installs its
dependencies (jinja2, werkzeug, markupsafe, itsdangerous and click),
so you only need to add :code:`flask` to the requirements in that case.


Technical details
-----------------

It turns out that very little hackery is necessary to make a webview
type app work. The APK seems to need the INTERNET permission to use a
WebView, but Android is very happy for the Python code to run a web
server with no further problems.

Making PyJNIus work required a little extra work, as it previously
relied on the now-absent SDL to access a pointer to the current
JNIEnv. This was fairly simple to fix by using only the relevant code
from SDL2 - the important parts are only a small fraction
of what SDL provides, as SDL has to worry about all the app input and
output going via JNI. For now, python-for-android just patches PyJNIus
before building it, but now that there are three different ways to get
the JNIEnv on Android this will need addressing somehow in PyJNIus
itself.

         
         
