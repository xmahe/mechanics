import pygame
from math import sin, pi

from vector import *
from node import *
from interaction import *
from world import *

world = World()

## Add a pendulum
fixed    = world.add_node(FixedNode(position = Vector(0, 2)))
pendulum = world.add_node(     Node(position = Vector(1, 2.0), velocity = Vector(0.1, 0), mass = 1, J = 1))
world.add_interaction(Gravity(pendulum))
world.add_interaction(Drag(pendulum))
world.add_interaction(Spring(fixed, pendulum, l0 = 1.0))

# Add a free ball
freeball = world.add_node(Node(position = Vector(0, 3), velocity = Vector(-0.1, 2) , mass = 5, J = 1))
world.add_interaction(Gravity(freeball))
world.add_interaction(Drag(freeball))

# Add a box
box_cm = Node(position = Vector(0.2, -0.3), velocity = Vector(0.0, 0.0).scale(0), mass = 10, J = 50, ω = -0.0)
world.add_interaction(
        BoundingBox(
            world.add_node(box_cm),
            world.add_node(VirtualNode(box_cm, position_relative_to_cm = Vector(+1.2, +0.6))),
            world.add_node(VirtualNode(box_cm, position_relative_to_cm = Vector(+1.1, -1.3))),
            world.add_node(VirtualNode(box_cm, position_relative_to_cm = Vector(-1.4, -0.9))),
            world.add_node(VirtualNode(box_cm, position_relative_to_cm = Vector(-0.8, +1.6)))))

world.add_interaction(Spring(FixedNode(position = Vector(0.2, -0.3)), box_cm, stiffness_N_per_m= 1000, rotational_damping_Nm_per_rads = 20, damping_Ns_per_m = 60, l0 = 0))
world.add_interaction(Gravity(box_cm))

# Another, smaller, box
small_cm = Node(position = Vector(-0.2, 2), velocity = Vector(0, -0.8), mass = 15, J = 2, ω=0)
world.add_interaction(
        BoundingBox(
            world.add_node(small_cm),
            world.add_node(VirtualNode(small_cm, position_relative_to_cm = Vector(+0.2, +0.2))),
            world.add_node(VirtualNode(small_cm, position_relative_to_cm = Vector(+0.2, -0.2))),
            world.add_node(VirtualNode(small_cm, position_relative_to_cm = Vector(-0.2, -0.2))),
            world.add_node(VirtualNode(small_cm, position_relative_to_cm = Vector(-0.2, +0.2))),
            ))

#world.add_interaction(Gravity(small_cm))

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
