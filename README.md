Katana
======
[In het Nederlands](README.nl.md)

Katana is a Scratch 2.0 extension to interface with gamepads

The Scratch 2.0 extension API has always remained experimental so getting
extensions loaded requires a trick.

To use this extension, connect your gamepad, run the server in `katana.py` and
then, in Scratch 2.0, Shift-click on the `File` menu, this will make a hidden
option appear to `Import experimental scratch extension`, click that and select
`katana.s2e`.

That should be all that's required, you can find the Katana blocks under "More
Blocks", usually a black or grey color in the blocks menu. There's red/green
indicator dot next to the katana subsection, green denotes a connection to the
server but does not indicate whether a controller is connected.

The katana server doesn't currently have a graphical UI, rather it is to be run
in a text terminal and emits copious messages that reflect the current state of
inputs on the controller. To check whether your controller is connected you can
look at this log output, if values change when you interact with the controller
it's connected.

Katana currently only supports connecting a single controller to scratch.

There's an older similar project with more polish available at the [Coolest
Projects](http://coolestprojects.be/controller/) website (in dutch). Be sure to
check it out because they have some great advice.

Is there any point to this project existing if there's an alternative?
I can come up with three reasons:

1. One of the express goals of this project is to "keep it simple" the
   extension is composed of only two files. The server is written in Python and
   aims to be understandable, with some effort, by beginner programmers.
2. We've been using `gamepad2scratch` in our dojos and it generally works
   really well, the GUI is definitely easier to understand. However, we've run
   into a controller simply not working with `gamepad2scratch` but working fine
   with Katana.
3. Katana uses a better algorithm to deal with an inherent property of
   Joysticks known as "deadzones." Based on an excellent article on the
   subject, [Doing Thumbstick Dead Zones
   Right](http://www.third-helix.com/2013/04/12/doing-thumbstick-dead-zones-right.html).
