import pygame

from world import *
from vector import *
from node import *
from interaction import *
from drone import *

world = World()

drone = Drone(world, SPEED_MODE)

while True:
    (t, dt) = world.tick()

    # Undraw graphics
    for node in world.nodes:
        node.undraw()
    for interaction in world.interactions:
        interaction.undraw()

    # Physics computations
    for node in world.nodes:
        node.reset()  # Reset forces

    # Handle user inputs and node interactions
    events = pygame.event.get()
    for interaction in world.interactions:
        interaction.handle_event(events)
        interaction.apply()  # Compute forces

    # Compute time step
    for node in world.nodes:
        node.simulate(dt,t)  # Step all nodes forward in time

    # Draw graphics
    for node in world.nodes:
        node.draw()
    for interaction in world.interactions:
        interaction.draw()

    pygame.display.flip()
