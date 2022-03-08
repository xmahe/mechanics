import pygame

from world import *
from vector import *
from node import *
from interaction import *
from drone import *

world = World()

#drone = Drone(world, RAW_MODE)
#drone = Drone(world, ACRO_MODE)
#drone = Drone(world, ACRO_ALTITUDE_MODE)
#drone = Drone(world, STABILISED_MODE)
drone = Drone(world, SPEED_MODE)
tool = Tool(world, drone)

nodea = world.add_node(Node(position = Vector(2.5,3), velocity = Vector(0,0), mass = 2, J = 1))
nodeb = world.add_node(Node(position = Vector(2.6,2), velocity = Vector(0,0), mass = 2, J = 1))
nodec = world.add_node(Node(position = Vector(3.6,2), velocity = Vector(0,0), mass = 2, J = 1))
world.add_interaction(Floor(nodea))
world.add_interaction(Floor(nodeb))
world.add_interaction(Floor(nodec))
world.add_interaction(Gravity(nodea))
world.add_interaction(Gravity(nodeb))
world.add_interaction(Gravity(nodec))
world.add_interaction(FixedDistance(nodea,nodeb))
world.add_interaction(FixedDistance(nodeb,nodec))
nodeafixer = world.add_node(FixedNode(position = nodea.p))
world.add_interaction(RotarySpring(nodeafixer, nodea))
world.add_interaction(FixedDistance(nodea, nodeafixer))

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
