# Planetary Orbit Simulator
#### Video Demo: https://youtu.be/qKSBHrbQHEY
#### Description:
This is a physics simulation of n-body orbital motion written in Python. There is a basic solar system consisting of the Sun, Venus, Earth (and Moon), and Mars when starting the program. You can create your own solar system or try to recreate one from your favorite series, or just mess with the solar system by throwing a black hole into it. The program uses Euler method to simulate gravity.

The _view_ tab is used to view the list of planets (and their mass and position) currently in the program; you can select them by clicking on this tab. Use the _go to selected_ button make the camera follow a selected planet and _remove selected_ to delete the selected planet. You can use this to select planets that you can't find with your camera.

For spawning planets, use the _add_ tab. First input the name, mass and color of the planet. Then, input some parameters
You can spawn two kinds of planet, stationary or non-stationary. For stationary planets, you only need to input the x and y-coordinates relative to the selected planet (you need to select an existing planet to spawn one). For non-stationary planets, however, you need to input orbital elements from 2-body Keplerian orbital physics. These are: initial anomaly, apoapsis, periapsis, and angle of periapsis. The initial anomaly refers to the true anomaly angular parameter that defines the position of a body moving along a Keplerian orbit, where the planet will initially be. The apoapsis and periapsis refer to the furthest and nearest points, respectively, of the orbit from the parent body. The angle of periapsis refers to the angle between the periapsis and the horizontal axis. Not inputting a value in one of the textboxes (except for the name) will make the program choose a random number from 0-255.

##### Requirements
Requires pygame-ce for source code. Install using pip:
```
pip install pygame-ce
```

##### Controls:
* Left-click to select planet
* Right-click drag or Arrow Keys to pan camera
* Scroll to Zoom
* period (.) and comma (,) for timescaling

##### Notes
There are still have some issues like the mouse detection for selecting planets is not accurate when zoomed. But, most of the features I wanted to have is implemented.

If I have more time, I would have liked to:
* Fix bugs
* Inlcude collisions - Planets colliding would spawn smaller chunks that will go into different directions. These chunks would follow conservation of momentum.
* A more intinuitive system for spawning planets - Spawn planets using the screen.
