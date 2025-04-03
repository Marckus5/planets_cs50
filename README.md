# Planetary Orbit Simulator
#### Video Demo: https://youtu.be/qKSBHrbQHEY
#### Requirements
Requires pygame-ce for source code. Install using pip:
```
pip install pygame-ce
```

#### Controls:
* Left-click to select planet
* Right-click drag or Arrow Keys to pan camera
* Scroll to Zoom
* period (.) and comma (,) for timescaling

#### Description:
This is a physics simulation of n-body orbital motion written in Python. There is a basic solar system consisting of the Sun, Venus, Earth (and Moon), and Mars when starting the program. You can create your own solar system or try to recreate one from your favorite series, or just mess with the solar system by throwing a black hole into it. The program uses Euler method to simulate gravity with the equation $a = \frac{GM}{r^2}$, though for simplicity I let $G=1$; the program uses arbritary units for all its quantities, so all constants have value equal to $1$. This program was inspired by games like Universe Sandbox.

Pygame is used as the graphics API for this program. It is a useful Python package for making graphical program, in particular for games. I used this one because I learned it before taking this course. This package is a wrapper for SDL2, restructure to be more oriented towards game development. I also extensively used object oriented programming for this one. The Planet class, for example, is a Sprite subclass, a pygame class that are useful for organizing the required parameters for a sprite, such as its image and how it behaves. The Planet class contains all the methods required for simulating the physics, and a method used for spawning it in an orbit. The object uses vectors for most of its physical quantities, such as its position, velocity, and acceleration. It is not required; I can use tuples for it, but the math is much simpler to implement for vectors as I can modify the two values of the vector with only one line. An example is `velocity = 2*velocity` would mean multiply each component of `velocity` by 2. The simulation itself uses delta-time, a technique to ensure consistent physics even when the framerate varies.

There are two main screens in the program, the scene where the planets are rendered and the menu where the you can do some things to the simulation. I made the camera to be a SpriteGroup object so I can make a large _surface_ (a variable that holds images in pygame) that is then blitted onto the scene. The surface of the scene is rendered larger than what is shown on the screen to give us the ability to zoom in or out. I also track the camera's position so I can easily render the planets accordingly. The planets are blitted onto the camera's surface, as well as a line that represents the previous position of the planet.

For the menu, we have two tabs, the _view_ and _add_ tabs. On the bottom of the menu, you can see which planet is selected and the zoom level and timescaling of the simulation.
The _view_ tab is used to view the list of planets (and their mass and position) currently in the program; you can select them by clicking on this tab. Use the _go to selected_ button make the camera follow a selected planet and _remove selected_ to delete the selected planet. You can use this to select planets that you can't find with your camera. For spawning planets, use the _add_ tab. First input the name, mass and color of the planet. Then, input some parameters depending if planet is stationary or not. For stationary planets, you only need to input the x and y-coordinates relative to the selected planet (you need to select an existing planet to spawn one). For non-stationary planets, however, you need to input orbital elements from 2-body Keplerian orbital physics where the parent body will be the selected planet. These are: initial anomaly, apoapsis, periapsis, and angle of periapsis. The initial anomaly refers to the true anomaly angular parameter that defines the position of a body moving along a Keplerian orbit, where the planet will initially be. The apoapsis and periapsis refer to the furthest and nearest points, respectively, of the orbit from the parent body. The angle of periapsis refers to the angle between the periapsis and the horizontal axis. Not inputting a value in one of the textboxes (except for the name) will make the program choose a random number from 0-255.

The method for generating a planet's orbit is one that I am most proud as I implemented it mostly by reading through the math of orbital mechanics. This is where vector math is useful as I can use in-built methods for it such as rotation.

There are still have some issues like the mouse detection for selecting planets in the scene is not accurate when zoomed. It is likely due to how I implemented the camera's surface so I may be missing a factor, but I have no idea what it is. But, most of the features I wanted to have is implemented.

If I have more time, I would have liked to:
* Fix bugs like the aforementioned mouse detection issue
* Inlcude collisions - Planets colliding would spawn smaller chunks that will go into different directions. These chunks would follow conservation of momentum.
* A more intinuitive system for spawning planets - Spawn planets using the screen.
* A better way to implement the zooming mechanic. My implementation is limited due to how much it consumes memory.
