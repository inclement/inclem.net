Kivy Crash Course 3 - More interesting widget interactions
##########################################################

:date: 2014-01-15 21:24
:tags: kivy, crash course, python, android
:category: Kivy Crash Course
:slug: 3_more_interesting_widget_interactions
:author: Alexander Taylor


Introduction
============

(`Original video <https://www.youtube.com/watch?v=-NvpKDReKyg>`_)

This is the standalone write-up of my third Kivy Crash Course video,
linked above. In this entry, I head back to Python to add some more
complex and interesting behaviour to our simple program from the
`first article <{filename}/kivycrashcourse/1-making_a_simple_app.rst>`_.

If you want to follow along, you can copy down the state of the code
from the end of the first tutorial, as below. You can also find it
`on github
<https://github.com/inclement/kivycrashcourse/blob/master/video3-more_interesting_widget_interactions/before.py>`_.

.. code-block:: python

   from kivy.app import App

   from kivy.uix.scatter import Scatter
   from kivy.uix.label import Label
   from kivy.uix.floatlayout import FloatLayout

   class TutorialApp(App):
       def build(self):
           f = FloatLayout()
           s = Scatter()
           l = Label(text="Hello!",
                     font_size=150)

           f.add_widget(s)
           s.add_widget(l)
           return f

   if __name__ == "__main__":
       TutorialApp().run()

As explained in my original article, this codes for a simple app with
a label saying 'Hello!' that you can click and drag around. You can
also scale and rotate it by using multiple touches if you have a
multitouch interface, or on a desktop/laptop by right clicking to use
Kivy's touch emulation.

Adding some more behaviour
==========================

So how are we going to change the app? I want to add some more complex
behaviour - at the moment, it's nice that we can move the text around,
but this is all handled by the Scatter widget and it isn't yet clear
how we could create our own widget interactions in a useful way.

I'm going to demonstrate a simple widget interaction by adding a
`TextInput`, a textbox widget that the user can type into. I'll then
create a binding so that the Label automatically updates to match this
text, so as soon as the user types anything the text is automatically
propagated to the Label, which we'll still be able to drag around via
the Scatter widget.

Let's start by importing the widgets we need:

.. code-block:: python

   from kivy.uix.textinput import TextInput
   from kivy.uix.boxlayout import BoxLayout
