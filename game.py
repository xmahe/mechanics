import pygame
from math import sin, pi

from vector import *
from node import *
from interaction import *
from world import *

world = World()

# Add a pendulum
fixed    = world.add_node(FixedNode(position = Vector(0, 2), mass = 1))
pendulum = world.add_node(     Node(position = Vector(1, 2), velocity = Vector(0.1, 0), mass = 1))
world.add_interaction(Gravity(pendulum))
world.add_interaction(Drag(pendulum))
world.add_interaction(Spring(fixed, pendulum))

# Add a free ball
freeball = world.add_node(Node(position = Vector(2, 3), velocity = Vector(-3, 3) , mass = 1))
world.add_interaction(Gravity(freeball))
world.add_interaction(Drag(freeball))

# TODO make boundingbox consist of nodes instead

# Add a box
box_a = world.add_node(Node(position = Vector(+1.2, +0.6), velocity = Vector(0, 0), mass = 1))
box_b = world.add_node(Node(position = Vector(+1.1, -1.3), velocity = Vector(0, 0), mass = 1))
box_c = world.add_node(Node(position = Vector(-1.4, -0.9), velocity = Vector(0, 0), mass = 1))
box_d = world.add_node(Node(position = Vector(-0.8, +1.6), velocity = Vector(0, 0), mass = 1))
world.add_interaction(BoundingBox(box_a, box_b, box_c, box_d))

running = 1
while running:
    (t, dt) = world.tick()

    # Physics computations
    for node in world.nodes:
        node.reset()  # Reset forces
    for interaction in world.interactions:
        interaction.apply()  # Compute forces
    for node in world.nodes:
        node.simulate(dt,t)  # Step all nodes forward in time

    # Draw graphics
    world.screen.fill((255,255,255))
    for node in world.nodes:
        node.draw()
    for interaction in world.interactions:
        interaction.draw()
    pygame.display.flip()
