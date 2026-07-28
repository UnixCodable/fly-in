*This project has been created as part of the 42 curriculum by lbordana*

## Description

Fly_in is an algorythmic project demonstrating how to lead a fleet of drone from a starting zone to an ending zone, passing through multiple restricted / valuated ones, and reaching those through connections. It must be showed has a graph.

Drones are facing some other restrictions as they must move simultaneously and cannot reach a zone if other ones had crossed the connection and the connection's max_link is full. 

This fleet of drone must reach the ending zone within a minimum of turns.

## Instructions

First the project will be much more appreciated with **[SOUND ON]**

Then, you'll need to install all the dependencies :

```bash
make install
```

After that you can launch the program with :

```bash
make run
```

In case of corrupted settings, please delete the file **settings.json**, it will regenerate a default one.

To check for mypy and flake8 norms, please run :

```bash
make lint
```

or

```bash
make lint-strict
```

## Resources

**AI Usage :** I do not use AI for coding or as a tutor. It is only used for assets generation.

**Links**:

- Pygame documentation : https://www.pygame.org/docs/
- Button manipulation in pygame : https://www.youtube.com/watch?v=jyrP0dDGqgY
- How to play videos in pygame : https://www.youtube.com/watch?v=K8PoK3533es
- Dijkstra logic : https://www.youtube.com/watch?v=bZkzH5x0SKU

## 