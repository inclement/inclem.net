Wrapping text in Kivy's Label
#############################

:date: 2014-07-05 23:14
:tags: kivy, python, label
:category: kivy
:slug: kivy_label_text
:author: Alexander Taylor
         

Another Kivy question that I often see (particularly recently for some
reason) is about using the Label widget - how to have text wrap
automatically, or the opposite, how to have the label automatically
grow to accommodate its text. I've covered this before in the 12th
`Kivy crash course video
<https://www.youtube.com/watch?v=WdcUg_rX2fM>`_, but here's a quick
write up of the basics.


The first thing to realise is how the Label works by default. It takes
the text, and *draws* it to a texture, in practical terms that's an
image of the characters. Everything you might want to do with the
Label revolves around what this texture is really doing. By default,
it does *not* wrap the text (unless you put in linebreak characters
manually) - it just makes one long image on a single row.  This image
is is placed right in the middle of the label, centered in both
directions. The behaviour is fine for short text snippets, but will
overhang the Label on both sides if the text is too long.

This also leads to some other annoying behaviour - as well as the
text not wrapping, you might have observed that the halign and valign
properties seem to do nothing by default. This is because they orient
things not inside the widget, but inside the texture...which 
is the exact size it needs to contain the text so alignments change
nothing.

To solve all these problems, you can manually set the size of the
texture with :code:`text_size`, a tuple of width and height, e.g.::

    Label:
        text_size: self.size

This reverses the default behaviour - instead of the texture growing
to fit the text, the text will be wrapped to fit the texture! If there
is space to spare, it is aligned within the texture according to the
:code:`halign` and :code:`valign` properties.

The Label also has another useful property, the :code:`texture_size`,
which holds the *actual* size of the texture. You can use that do bind
behaviour to the size of the text. For instance, a common requirement
is to create a Label that grows as long as it needs to contain its
text, but which wraps it to a certain width. We can combine both of
the above ideas to accomplish this::

    Label:
        size_hint_y: None
        text_size: self.width, None
        height: self.texture_size[1]

If you (for instance) place this label in a ScrollView, it will be
Scrollable over exactly the right distance to fit in all the text.
