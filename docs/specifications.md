## General specifications

### Objectives :

Designing a system that efficiently routes a fleet of drones from a central base (start) to a target location (end), while navigating this dynamic network under a set of strict constraints and optimization goals.

### Lore and ideas :

Travelling in space in Star Wars universe, episode 42, to establish communications through the galaxy

### Composition :

- **Multithreading** : To handle multiple drone movements simultaneously
- **Semaphores** : To lock zones for Nmax of drones
- **Arcade** : Uses OpenGL and way faster than PyGame
- **Pydantic** : To parse documents and validate easily the arguments

### Work organization :

#### 1 / Map Parsing

Data parsing will be done by reading each line of a file, encapsulating argue in a dict after pydantic validation.

#### 2 / Algorithm

Creation of the drone fleet algorithm with threading and semaphores.

#### 3 / GUI

GUI making with Arcade library

