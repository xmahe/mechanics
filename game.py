import pygame
from math import sin, pi

from vector import *
from node import *
from interaction import *
from world import *

world = World()

## Add a pendulum
drone = world.add_node(Node(position = Vector(0, 2)))
# tool = world.add_node(Node(position = Vector(1, 2.0), velocity = Vector(0.1, 0), mass = 1, J = 1))

world.add_interaction(Gravity(drone))

running = 1

# Warmpup
for i in range(0,100):
    (t, dt) = world.tick()
    for node in world.nodes:
        node.reset()  # Reset forces
    for interaction in world.interactions:
        interaction.apply()  # Compute forces
    for node in world.nodes:
        node.simulate(dt,t)  # Step all nodes forward in time

i = 0
while running:
    (t, dt) = world.tick()

    # Physics computations
    for node in world.nodes:
        node.reset()  # Reset forces
    for interaction in world.interactions:
        interaction.apply()  # Compute forces
    for node in world.nodes:
        node.simulate(dt,t)  # Step all nodes forward in time

    if i == world.interleaving:
        i = 0
    else:
        i += 1
        continue

    # Draw graphics
    world.screen.fill((255,255,255))
    for node in world.nodes:
        node.draw()
    for interaction in world.interactions:
        interaction.draw()
    pygame.display.flip()
