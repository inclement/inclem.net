Creating a Kivy layout: the SparseGridLayout
############################################

:date: 2014-01-27 22:37
:tags: kivy, python, layout, widget
:category: kivy
:slug: sparsegridlayout
:author: Alexander Taylor
         

I thought for a change I'd try for a shorter post on a single quick
subject, so I'm going to quickly explain a simple Kivy layout I
created, the :code:`SparseGridLayout`. The post is standalone, but would go
well with ideas from my `Kivy Crash Course
<{filename}/pages/kivycrashcourse.rst>`_, especially the recent videos
trying to draw ideas together to make widgets or specifically focusing
on layouts.
         
The point here is that Kivy has a built in GridLayout, but it doesn't
cover all use cases for widgets in a grid, which is sometimes
confusing to users who've seen grid widgets in other places and
expected a slightly different behaviour. The problem is that the
GridLayout fills widgets in from the top. That means for instance if there are 3
columns, you can't place a widget in the third row without first
adding *6* widgets to fill the first two rows. That's just inefficient
and wasteful if all you wanted was a small number of widgets in a grid.

So, my SparseGridLayout is a very simple layout that has a number of
rows or columns, and checks its children for a `row` and `column`
property. It then resizes them automatically to be placed in the right
grid cell. That means we don't need any extra widgets, which is much
more efficient if we want a grid with not many entries, hence *sparse*
grid layout.

We can start with a :code:`FloatLayout` base, then all we need to do is set
our grid children's :code:`size_hint` and :code:`pos_hint` properties
appropriately for the grid and call the `FloatLayout`'s normal layout
method to actually place them in the grid positions/shapes for us.

We can start by making our layout class:

.. code-block:: python

   from kivy.uix.floatlayout import FloatLayout
   from kivy.properties import NumericProperty, ReferenceListProperty

   class SparseGridLayout(FloatLayout):
       rows = NumericProperty(1)
       columns = NumericProperty(1)
       shape = ReferenceListProperty(rows, columns)

That creates a basic class that doesn't have any more actual behavior
than the :code:`FloatLayout` alone, but has a few new properties. It'll
hopefully all make sense if you've used Kivy a little or followed my
crash course, though the :code:`ReferenceListProperty` may be new - this
takes multiple other properties and lets us access them as a list, so
for instance referencing or setting :code:`shape[0]` really updates the
:code:`rows` property, including calling all its associated events etc.. At
the same time, the :code:`shape` is also a real property, with its own
events. Do experiment with this if the explanation is not clear.

Now, to make our layout actually rearrange its children to the grid,
we need to override its :code:`do_layout` method, which is what's called
whenever it or its children are updated.

.. code-block:: python

   def do_layout(self, *args):
       shape_hint = (1. / self.columns, 1. / self.rows)
       for child in self.children:
           child.size_hint = shape_hint
           if not hasattr(child, 'row'):
               child.row = 0
           if not hasattr(child, 'column'):
               child.column = 0

           child.pos_hint = {'x': shape_hint[0] * child.row,
                             'y': shape_hint[1] * child.column}
       super(SparseGridLayout, self).do_layout(*args)

This iterates over all the `SparseGridLayout`'s children, setting their
size_hint so that they'll fit exactly in a grid cell (as per the
:code:`rows` and :code:`columns` properties we set above). It then checks if
they have a :code:`row` or :code:`column` property, setting it to :code:`0` if not - I've
chosen that my rows and columns should be zero-indexed, you could
modify that if you like. After that, it sets their :code:`pos_hint` such
that they're placed in the right place. I've deliberately let this
work with floats, so for instance they could be in column 2.5 to be
halfway between the integer columns, so the layout is extra flexible.

The final step is calling the original :code:`do_layout` method of the
:code:`FloatLayout`. The magic is that all we did is set the child widgets
:code:`size_hint` and :code:`pos_hint` so that the widgets align to a grid - the
:code:`FloatLayout` itself already knows how to actually set their positions
and sizes based on this information. By making use of Kivy's existing
layout abilities, we've saved ourself a lot of work.

Finally, I also added a class to represent entries in the grid:

.. code-block:: python

   class GridEntry(EventDispatcher):
       row = NumericProperty(0)
       column = NumericProperty(0)

This is very simple, but it means you can do for example:

.. code-block:: python

   class GridLabel(Label, GridEntry):
       pass

The GridLabel is thereby a :code:`Label` that already has row and column
properties, so it will behave properly in our :code:`SparseGridLayout`. We
don't strictly need to do this, we could add the :code:`row` and :code:`column`
any other way, but this is neat and makes it totally clear what we're
using our widgets for.

That's everything! With just a few simple modifications we've made a
whole new Layout widget that can place its children in rows and
columns of a grid. Maybe you'll find that useful, but more generally I
hope this demonstrates the general principles of thinking about
Layouts and using Kivy's existing mechanisms to do most of the work.

You can find all this code at my `sparsegridlayout github repository
<https://github.com/inclement/sparsegridlayout/blob/master/__init__.py>`_,
which also includes a simple demonstration App so you can test the new
layout if you like.
