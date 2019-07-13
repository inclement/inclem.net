
A delayed resize layout in Kivy
###############################

:date: 2019-07-13 13:30
:tags: python, kivy
:category: kivy
:slug: delayed_resize_layout
:author: Alexander Taylor

A user on the `Kivy Discord <https://discordapp.com/invite/eT3cuQp>`__
just raised the question of how to delay widget updates during resize
events. The problem was that the widgets did some heavy processing
(generating matplotlib graphs) that would be very slow if called for
every tiny update during a larger resize event.

This is a good opportunity to return to the flexibility of Kivy
layouts. It's very easy to add some simple behaviour that delays
updates until a short period has passed without the size
changing. Here's a quick implementation I threw together:

.. code-block:: python

   from kivy.uix.anchorlayout import AnchorLayout
   from kivy.clock import Clock
   from kivy.properties import ObjectProperty, NumericProperty

   from functools import partial

   class DelayedResizeLayout(AnchorLayout):

       do_layout_event = ObjectProperty(None, allownone=True)

       layout_delay_s = NumericProperty(0.2)

       def do_layout(self, *args, **kwargs):
           if self.do_layout_event is not None:
               self.do_layout_event.cancel()
           real_do_layout = super().do_layout
           self.do_layout_event = Clock.schedule_once(
               lambda dt: real_do_layout(*args, **kwargs),
               self.layout_delay_s)

This layout could be used as the root widget of a whole application,
to delay the resizing of all the content, or somewhere within the app
to delay only a small part of it.

And a simple example:

.. code-block:: python

   from kivy.uix.button import Button
   from kivy.base import runTouchApp

   button = Button(text='example button')
   layout = DelayedResizeLayout()
   layout.add_widget(button)
   runTouchApp(layout)
