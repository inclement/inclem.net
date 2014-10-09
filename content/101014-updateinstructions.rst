Updating canvas instructions declared in Python
###############################################

:date: 2014-10-10 23:46
:tags: kivy, python, canvas instructions
:category: kivy
:slug: kivy_update_instructions
:author: Alexander Taylor

         
Continuing the theme of my last few posts, a common problem for new
kivy users is creating canvas instructions that follow their parent
widgets. For instance, here's some code for a custom widget that tries
to draw a red rectangle in its upper-right corner - this is fairly
standard kivy code to draw directly on the widget canvas, and is
documented `here <http://kivy.org/docs/api-kivy.graphics.html>`_.

.. code-block:: python
                
   from kivy.uix.widget import Widget
   from kivy.graphics import Rectangle, Color

   class CornerRectangleWidget(Widget)
       def __init__(self, **kwargs):
           super(CornerRectangleWidget, self).__init__(**kwargs)
           
           with self.canvas:
               Color(1, 0, 0, 1)  # set the colour to red
               self.rect = Rectangle(pos=self.center, 
                                     size=(self.width/2., 
                                           self.height/2.))
               
This looks like it will create a red rectangle, whose length is half the
parent size in both directions, and whose position is the parent
centre.

The surprise is that this is actually not what happens. Instead, the
rectangle is always positioned at (50, 50) with size (50, 50),
regardless of where the widget appears.

The reason for this is that these values really are based on the pos
and size of the widget at the point where the canvas code was run; all
widgets have a default position of (0, 0) and size of (100, 100), and
this will not necessarily be updated (for instance by a parent layout
class) until after their ``__init__`` is run. However, the Rectangle
properties receive only these initial values, and don't know about the
new position of the widget.

The solution is to simply hook into kivy's event system to update the
rectangle pos and size ourselves whenever the widget changes:

.. code-block:: python
                
   from kivy.uix.widget import Widget
   from kivy.graphics import Rectangle, Color

   class CornerRectangleWidget(Widget)
       def __init__(self, **kwargs):
           super(CornerRectangleWidget, self).__init__(**kwargs)
           
           with self.canvas:
               Color(1, 0, 0, 1)  # set the colour to red
               self.rect = Rectangle(pos=self.center, 
                                     size=(self.width/2., 
                                           self.height/2.))
               
           self.bind(pos=self.update_rect,
                     size=self.update_rect)
     
       def update_rect(self, *args):
           self.rect.pos = self.pos
           self.rect.size = self.size

Now whenever the widget ``pos`` or ``size`` changes, our new method is
called and the rectangle resized or repositioned as necessary. It will
always track the widget's upper right corner, so we get the visual
effect we were originally looking for.

Of course, an even better solution (where possible) is to use kv
language:

.. code-block:: python
                
   <CornerRectangleWidget@Widget>  
       canvas:
           Color:
              rgba: 1, 0, 0, 1                        
           Rectangle:
              pos: self.center
              size: self.width / 2., self.height / 2.
              
This is shorter, simpler and clearer. We don't need to manually set up the
binding because kv automatically detects that we referred to
properties of the parent widget and creates it automatically -
something that isn't really possible in python. This is
one reason that we recommend using kv language wherever possible.
                                
