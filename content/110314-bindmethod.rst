Kivy's bind method
##################

:date: 2014-03-11 10:47
:tags: kivy, python, 
:category: kivy
:slug: kivy_bind_method
:author: Alexander Taylor
         
One of the big mistakes I see from new Kivy users is misunderstanding
how the bind method works, especially amongst newer Python users who
haven't fully formed their intuition about function calls. For
instance, a user will write code like:

.. code-block:: python

   some_screenmanager.bind(current=a_function(arg1, arg2))

Here, the idea is that when the :code:`current` property changes, it
will call :code:`a_function` with the arguments :code:`arg1` and
:code:`arg2`.

The problem is that Python itself fundamentally doesn't work like
this. The bind method doesn't know about the existence of
:code:`a_function` or its arguments, it only receives the *result* of
this function call. This often leads to confusion when a user doesn't
understand why the binding is only called once, during the declaration
of the binding.

Stepping back, our real goal is to call :code:`a_function` with the
given arguments, but :code:`bind` needs to be passed a function if it
is to work correctly. That means we can solve our problem by creating
a new function with these arguments already passed (and discarding the
extra arguments automatically passed by bind).

It's usually convenient to do this with the :code:`partial` function
from the functools module:

.. code-block:: python

   from functools import partial
   some_screenmanager.bind(current=partial(a_function,arg1, arg2))
   
:code:`partial` returns a new function that will automatically be
passed arg1 and arg2, exactly as we want. You can also pass kwargs
this way.

This isn't the only way to solve the problem, we could have created a
lambda function (though the syntax is longer and can have scope
problems) or an entire new function with :code:`def` syntax, but both
of these are more complicated than the simple use of
:code:`partial`. So if you need to do a binding in Python, look at
this way first! 
