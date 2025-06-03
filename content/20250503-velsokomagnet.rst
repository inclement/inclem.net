History of the Velsokomagnet
############################

:date: 2025-06-03 21:00
:tags: puzzlescript
:category: games
:slug: history_of_the_velsokomagnet
:author: Alexander Taylor

I like playing puzzle games and I always wondered what it would take to make one...so I had a go.

`Click here to play History of the Velsokomagnet! <https://www.puzzlescript.net/play.html?p=458ac36579dda092d8760585f08da80c>`__

.. figure:: {filename}/media/velsokomagnet.png
   :alt: Image of "History of the Velsokomagnet" gameplay
   :align: center

My goal was to try to find something interesting in some fairly arbitrary simple
rules. The core of the game is "normal" crate-pushing `sokoban
<https://en.wikipedia.org/wiki/Sokoban>`__ but with two twists: the player repels crates
at any distance when moving in their row or column...unless they're adjacent in which case
they stick to the player forever.

This actually turned out fairly annoying to work with, but I figured that's the whole
point of designing puzzles and tried to persevere. I'm pretty happy with the result, the
game as published has 12 levels that hopefully each achieve something interesting
arising from these mechanics without resorting to just being complex. I have no idea if
this is really successful though, or if it's fun. Let me know if you feel inspired either
way.

I wrote the game using `PuzzleScript <https://www.puzzlescript.net/>`__, which is a
delightful little html5 game engine for making grid-based puzzles. Its smart design makes
it easy to throw together many kinds of puzzle rules and just get on with designing
levels. The `gallery <https://www.puzzlescript.net/Gallery/index.html>`__ is very
inspiring, there are some absolutely genius puzzles in there teasting out amazing
complexity from incredibly simple rules.

The source is available `on github <https://github.com/inclement/velsokomagnet>`__, or
from the `play
<https://www.puzzlescript.net/play.html?p=458ac36579dda092d8760585f08da80c>`__ link above
you can click "hack" to directly start editing in the PuzzleScript editor.
