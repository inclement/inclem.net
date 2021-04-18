Thoughts on writing a wayland window manager with wlroots
#########################################################

:date: 2021-04-17 21:00
:tags: vivarium, wayland
:category: wayland
:slug: writing_a_wayland_compositor_with_wlroots
:author: Alexander Taylor

I recently released `Vivarium <{filename}/20210226-vivarium.rst>`__, a dynamic tiling
wayland compositor built using the `wlroots library
<https://github.com/swaywm/wlroots>`__.  Going from zero to compositing was interesting,
there are good libraries available but everything has moved very fast in the last couple
of years so it can be hard to know where to start. I especially wanted to write the
equivalent of an X window manager that only really cares about window layout and wants
everything else to Just Work.

Wlroots is a library created to support this use case. To quote its own README, it
provides "pluggable, composable, unopinionated modules for building a Wayland compositor;
or about 50,000 line of code you were going to write anyway". For me it's fulfilled that
goal very well, and Vivarium probably wouldn't exist without it. Still, while there are
many good development resources around it wasn't always straightforward to get up to speed
so I thought I should write the blog post I would have loved to read at the start, setting
out the broad ideas and good resources for each development step. This is that post.

Background
==========

(If you've got this far you probably have some idea what Wayland is about already, but
here's an unnecessarily long summary for general background purposes.)

Any modern desktop utilises some kind of *display server*, a program that brings together
the disparate components of desktop input and output to allow a consistent desktop
experience. In broad terms the display server keeps track of system outputs (an
abstraction that for the most part means physical monitors), and the applications that
want to draw to them, and via some set of rules draws the window images to them. This
means the display server also has to care about all sorts of other details: it must track
system inputs (keyboard, mouse) and pass their events through to applications; it must
deal with hardware details like monitor framerates, dpi scaling and rotation including
potentially passing these details to applications; and it may need to do drawing of its
own such as window decorations if the clients have not drawn their own. These are just
examples, the definition of the display manager is not rigid and these tasks can be
divided up in more than one different way, but you can't think about implementing display
server functionality without worrying about them.

For a very long time the display server on almost all linux systems has been `X.Org
<https://www.x.org/wiki/>`__, implementing the X11 protocol. X has the problem that its
design is old and crufty, there are many details of its architecture that do not map well
to how modern software wants to work. For this reason there has been growing development
effort behind an alternative, the `Wayland protocol
<https://wayland.freedesktop.org/>`__. It's been a long time coming, Wayland first became
a named thing somewhere around 2008, but nowadays the big desktop environments (Gnome,
KDE) are providing Wayland servers, many applications toolkits support it, and some big
distros are supporting Wayland by default.

Much has been written about this, some people think it's incredibly terrible for various
reasons and others don't. For what it's worth I'm in the latter camp, I think Wayland will
improve the Linux desktop experience. Still, changing such a big desktop component is a
complicated process and personally I have one particular problem: what about my window
manager?

The problem here is that under X it's been normal that the X server exists and handles all
the core display server functionality, but other applications can control a lot of its
behaviour. A special example is the *window manager*, the program that looks at the open
windows and actually decides where to draw them. In a big desktop environment like
Gnome/KDE the window manager is a small part of a larger desktop architecture, but it's
also totally practical and quite common to run a standalone window manager and there are
many popular ones for X11. As a quick reference, the Arch Linux wiki lists about `60
different options <https://wiki.archlinux.org/index.php/window_manager>`__, and these are
just the ones that people have bothered to list there. Personally I've used `xmonad
<https://xmonad.org/>`__ for many years, not because I think its particular brand of
tiling window management is the one true way, but I like it and it's been super stable.

With Wayland the situation is different. It isn't an irreconcilable change, you could
certainly write a Wayland server that lets you hotplug all the functionality a window
manager needs (and probably e.g. Gnome/KDE plugins already can do a lot of that, I'm not
sure), but in practice different projects have implemented their own Wayland display
servers. A window manager in this environment really has its work cut out, instead of
focusing on implementing window positioning logic it would need to implement the entire
wayland protocol, all those hardware interfaces, and all the additional protocols you
want to use such as the xdg-shell protocol applications use to actually tell the
Wayland server they want to display stuff.

Thankfully there has been much developer effort to rally around libraries and tooling to
make Wayland window manager equivalents easy. The most popular example is almost certainly
`wlroots <https://github.com/swaywm/wlroots>`__, a library for creating Wayland
compositors. Effectively wlroots can be used to write a window manager under Wayland
without worrying directly about the core Wayland functionality, although the final result is a
standalone binary that implements a full Wayland compositor as opposed to the X model of
window managers plugging into a separate server. Wlroots is still under development but is
nowadays quite stable and complete for every core task I've worked through. There are many
technical details of interest, I want to cover here how I got started learning about the
key ideas and writing a useful compositor that I now use full time.


How to get started with wlroots
===============================

The following is entirely my opinion and perspective. There is no single correct path to
take and I'm sure there are other great resources I didn't even notice or pay attention
to.

Before anything else you may want to ask whether you really need to write a Wayland
compositor. Window management functionality can potentially be achieved just as well
(maybe more easily!) as a plugin to another compositor, if it supports such an
interface. Some possibilities include:

* Write a `Wayfire plugin
  <https://github.com/WayfireWM/wayfire/wiki/Plugin-architecture>`__. Wayfire is an
  existing Wayland compositor using wlroots and its plugin system seems extensive enough
  to cover a lot of window manager functionality. There are also other similar options
  like writing a KWin or Gnome Shell script, but I don't know much about what these
  currently support.
* Use an existing tiling window manager. `Sway <https://swaywm.org/>`__ is mostly a
  drop-in replacement for the i3 window manager and is popular and well supported, with
  some scripting functionality. `River <https://github.com/ifreund/river>`__ supports a
  system of user-provided executables that makes its layouts quite flexible. Indeed
  `Vivarium <https://github.com/inclement/vivarium>`__ itself supports customisable
  layouts, but those other projects are much more established and perhaps more flexible.

  * Obviously I wrote Vivarium despite these alternative possibilities. I did that because
    I wanted to learn from the project and see how practical it was. Without that
    motivation, I'd probably be a happy Sway/River/other user.

* Hang around and see if wlroots grows a `higher level API
  <https://github.com/swaywm/wlroots/issues/1826>`__, or if another project/library starts
  to provide one. As it stands I think wlroots is a step more technically involved than it
  needs to be for most window management purposes - it isn't hard, but I feel like
  different wlroots compositors tend to implement some things in similar ways, which
  supports the idea that a better abstraction layer isn't quite there yet. Examples
  include damage tracking and the abstraction of views to provide a consistent
  api for views managed via different protocols, especially xdg-shell/xwayland. This isn't a
  criticism, just a feature that I think will eventually exist but doesn't yet.

I think ultimately there will naturally end up being multiple active compositor projects,
some of which support easily creating distinct window managers via extensive plugin
APIs, although it's of course impossible to know which projects will ultimately be
successful. See `Should you write a Wayland compositor
<https://tudorr.ro/blog/technical/2021/01/26/the-wayland-experience/>`__ by tudor for
another overview discussing these questions. Of course, there's never anything wrong with
starting another project.

So, if you do want to write a wlroots compositor...how to get started? Here's what I found
useful, in rough order. I started Vivarium without any specific knowledge about wlroots or
wayland, so that's the direction I'm coming from below.

* Drew DeVault's `Writing a Wayland compositor
  <https://drewdevault.com/2018/02/17/Writing-a-Wayland-compositor-1.html>`__ blog posts
  are an excellent introduction to how to think about Wayland. Don't worry too much about
  the code itself, I think it's outdated for current wlroots and the repository is
  archived, but the overview of key ideas will take you a long way.
* Fork `tinywl <https://github.com/swaywm/wlroots/blob/master/tinywl/tinywl.c>`__. This
  tiny example is shipped with wlroots and is an excellent base for a serious
  compositor. Although short it implements in a basic way almost every core
  functionality you'll need, and implicitly teaches a lot about Wayland API interaction
  (especially if using the C interface to events, listeners etc.) which scales very well
  when branching out into other protocols. Since tinywl is within the wlroots tree it is
  also guaranteed to be up to date.
* Watch (and join in on) the #sway and #sway-dev irc channels on irc.freenode.net. Seeing
  how other people think about things is always invaluable.
* Don't be afraid to actually read the wayland protocol definitions - the other linked
  resources also say this but it bears repeating. They are often surprisingly
  straightforward.
* Read `the Wayland Book <https://wayland-book.com/>`__. This is a much more thorough (but
  not complete) overview of the Wayland protocols and way of working. I've found this more
  useful as a reference to revisit than a direct learning tool, mostly because much of the
  detail isn't actually necessary to sit down and write code, but it's very nice for
  formalising knowledge to really do things right.
* Read `the Sway source code <https://github.com/swaywm/sway>`__. Sway doubles as a
  thorough reference for how to do just about anything with wlroots, since it's an active
  and fairly complete project that has tackled most issues you're likely to run into.
* Make use of the `wlroots examples
  <https://github.com/swaywm/wlroots/tree/master/examples>`__. When testing individual
  protocols/features these save a lot of time writing your own test code!

One issue I've sometimes hit is that wlroots doesn't always have much in-code
documentation. However, it mostly makes up for this in general design consistency, and
this is a big part of the value of tinywl: the methodology it demonstrates is widely
applicable throughout wlroots. For instance, supporting a new protocol is likely to come
down to a ``_create`` function call returning a manager object with an obvious-looking
API, whose events you can probably read the protocol documentation to understand, and
tinywl demonstrates this process.

It's also worth looking through the list of `projects which use wlroots
<https://github.com/swaywm/wlroots/wiki/Projects-which-use-wlroots>`__. Between them these
demonstrate many different things, especially where they focus on functionality that is
not so core to Sway.

There are many other useful resources scattered around, such as some posts on the blogs of
`Drew DeVault <https://drewdevault.com/>`__ (sway and wlroots creator) and `Simon Ser
<https://emersion.fr/blog/>`__ (sway and wlroots current maintainer), but I've generally
found these by googling keywords when stuck rather than from any specific catalogue.

And with all that...this is pretty much where I am. I'm no expert, but Vivarium works and
it was fun to write. Thanks to the Wayland developer community for creating all these
useful resources.
