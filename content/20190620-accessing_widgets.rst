Widget interactions between Python and Kv
#########################################

:date: 2019-06-20 22:00
:tags: kivy, python
:category: kivy
:slug: widget_interactions_between_python_and_kv
:author: Alexander Taylor

One of the biggest Kivy confusions I see is how different widgets can
access one another when they're in different parts of the
application. Fortunately, it's generally straightforward to do so. This
post gives examples of methods you might use in different situations.

The emphasis here is on what you *can* do, not what you *should*. If
you aren't sure which way is best in a given situation, go ahead and
choose what seems best at the time, but don't be afraid to revisit it
later.

How can a widget access its parent?
===================================

Use the ``parent`` property of the widget:

.. code-block:: python
   child = Widget()
   parent = Widget()

   assert child.parent is None  # child widget isn't added to any parent

   parent.add_widget(child)

   assert child.parent == parent


How can a widget access its children?
=====================================

Use the ``children`` property. This is a list containing all the children you added.

.. code-block:: python
   child = Widget()
   parent = Widget()

   assert len(parent.children) == 0  # no children added to parent

   parent.add_widget(child)

   print(parent.children)  # [<kivy.uix.widget.Widget object at 0x???>]
   assert child in parent.children

.. note:: The ``children`` list is actually backwards, i.e. the last
          widget you add will by default be the first in the
          list. This is a bit surprising, and only really happens for
          backwards compatibility.

How can a widget in Python access children from its kv rule?
============================================================

Option 1: ids
-------------

You can give the widgets in your kv rule ids to access them from Python.

.. code-block:: python
   # main.py

   from kivy.uix.boxlayout import BoxLayout
   from kivy.uix.label import Label
   from kivy.app import App

   class KvRuleWidget(BoxLayout):
       def on_touch_down(self, touch):
           print('We can get references to all the children using the ids dict.')

           # syntax is `self.ids.<id_text>`

           assert self.ids.middle in self.children
           assert self.ids.bottom in self.children

           # widgets can be accessed from deep in the kv rule
           assert self.ids.top_left not in self.children
           assert self.ids.top_right not in self.children

   class ExampleApp(App):
       def build(self):
           return KvRuleWidget()

.. code-block:: python
   # example.kv

   <KvRuleWidget>:
       orientation: 'vertical'
       BoxLayout:
           orientation: 'horizontal'
           Label:
               id: top_left
               text: 'top left'
           Label:
               id: top_right
               text: 'top right'
       Label:
           id: middle
           text: 'middle'
       Label:
           id: bottom
           text: 'bottom'

.. note:: You *cannot* set up widget ids from Python code, if
          you write e.g. ``w = Widget(id='some_name')`` this will not
          crash but the id will not be available in any ids
          dictionary.

.. note:: Remember that you can also use ids to

Option 2: properties
--------------------

You can use Kivy properties to pass around references to widgets.

.. code-block:: python
   # main.py

   from kivy.uix.boxlayout import BoxLayout
   from kivy.uix.label import Label
   from kivy.app import App
   from kivy.properties import ObjectProperty

   class KvRuleWidget(BoxLayout):
       top_right_label = ObjectProperty()

       def on_touch_down(self, touch):
           print('The top right label is {}'.format(self.top_right_label))

   class ExampleApp(App):
       def build(self):
           return KvRuleWidget()

.. code-block:: python
   # example.kv

   <KvRuleWidget>:
       orientation: 'vertical'
       top_right_label: top_right  # note that we used an id to set the property
       BoxLayout:
           orientation: 'horizontal'
           Label:
               id: top_right
               text: 'top left'
           Label:
               text: 'top right'
       Label:
           text: 'middle'
       Label:
           text: 'bottom'

Option 3: The ``parent`` and ``children`` properties
----------------------------------------------------

It is possible to walk through the widget tree using the ``parent`` and ``children`` properties.

This is usually a bad idea and is prone to breakage if the structure
of the widget tree changes. However, it's still possible.

.. code-block:: python
   # main.py

   from kivy.uix.boxlayout import BoxLayout
   from kivy.uix.label import Label
   from kivy.app import App
   from kivy.properties import ObjectProperty

   class KvRuleWidget(BoxLayout):
       def on_touch_down(self, touch):

           # get a reference to the top right label only by walking through the widget tree
           top_right_label = self.children[-1].children[0]

           print('The top right label is {}'.format(self.top_right_label))

   class ExampleApp(App):
       def build(self):
           return KvRuleWidget()

.. code-block:: python
   # example.kv

   # note: this time there are no ids at all
   <KvRuleWidget>:
       orientation: 'vertical'
       BoxLayout:
           orientation: 'horizontal'
           Label:
               text: 'top left'
           Label:
               text: 'top right'
       Label:
           text: 'middle'
       Label:
           text: 'bottom'

How can a widget in Kv access children defined in Python?
=========================================================

Sometimes you might have some children defined via a Kv rule, and
others created dynamically in Python. You can access the Python
widgets in kv by saving references to them in Kivy properties:

.. code-block:: python
   # main.py

   from kivy.uix.boxlayout import BoxLayout
   from kivy.uix.label import Label
   from kivy.app import App
   from kivy.properties import ObjectProperty

   class KvRuleWidget(BoxLayout):
       label_created_in_python = ObjectProperty()

       def __init__(self, **kwargs):
           super().__init__(**kwargs)

           # add a widget from python code
           label = Label(text='label created in Python')
           self.add_widget(label)
           self.label_created_in_python = label  # save a reference

   class ExampleApp(App):
       def build(self):
           return KvRuleWidget()

.. code-block:: python
   # example.kv

   <KvRuleWidget>:
       orientation: 'vertical'
       Label:
           text: 'label created in Kv'
       Label:
           text: 'the label created in Python has text "{}"'.format(root.label_created_in_python.text)

How can a widget defined in a kv rule access a widget defined in another kv rule?
=================================================================================

Sometimes you might have two widgets in very different places that
need to talk to one another somehow. Usually the best way to achieve
this is to consider how they are related to one another, and pass
information between them via their common relations.

Also see the next Section for how to access any widget from anywhere,
without worrying about how the widgets are related. However, that
usually isn't such a good choice in the long run.

The following example is deliberately very simple, but the same
principles can be used to link together widgets across your whole
program using references passed around where the kv rules meet.

.. code-block:: python
   # main.py

   from kivy.uix.boxlayout import BoxLayout
   from kivy.uix.button import Button
   from kivy.uix.label import Label
   from kivy.app import App
   from kivy.properties import ObjectProperty

   class IncrementCounterButton(Button):
       counter = NumericProperty(0)
       def on_press(self):
           self.counter += 1

   class CounterLabel(Label):
       counter = NumericProperty(0)

   class RootWidget(BoxLayout):
       pass

   class ExampleApp(App):
       def build(self):
           return RootWidget()

.. code-block:: python
   # example.kv

   <IncrementCounterButton>:
       text: 'press me'

   <CounterLabel>:
       text: 'the counter value is {}'.format(app.counter)  # `app` in kv is equivalent to `App.get_running_app()` in Python

   <RootWidget>:
       orientation: 'vertical'
       CounterLabel:
           counter: button.counter  # this means the CounterLabel's counter will always match the button's counter
       IncrementCounterButton:
           id: button

How can any widget access any other widget from anywhere?
=========================================================

Sometimes you really do want widgets to interact with one another
without any good relationship between them. You can do this in a
convenient way by using a Kivy property in the App class.

.. note:: This is notionally similar to using a global variable, and
          is often bad practice for all the same reasons.

The following example is quite contrived to keep it simple. In this
case you could probably think of a better way to do the same thing,
perhaps using the methods from the previous Sections.

.. code-block:: python
   # main.py

   from kivy.uix.boxlayout import BoxLayout
   from kivy.uix.button import Button
   from kivy.uix.label import Label
   from kivy.app import App
   from kivy.properties import ObjectProperty

   class IncrementCounterButton(Button):
       def on_press(self):
           # You can always access your App class from Python as follows:
           App.get_running_app().counter += 1

   class CounterLabel(Label):
       counter = NumericProperty(0)

   class ExampleApp(App):
       def build(self):
           boxlayout = BoxLayout(orientation='vertical')
           label = CounterLabel()
           button = IncrementCounterButton()

           boxlayout.add_widget(label)
           boxlayout.add_widget(button)

           return boxlayout

.. code-block:: python
   # example.kv

   <IncrementCounterButton>:
       text: 'press me'

   <CounterLabel>:
       text: 'the counter value is {}'.format(app.counter)  # `app` in kv is equivalent to `App.get_running_app()` in Python
