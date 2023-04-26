from vector import *
from node import *
from interaction import *

################################################################
# Create a drone
################################################################

# Create three nodes to represent the drone
drone_positions = [Vector(0, 3), Vector(-1, 2.5), Vector(1, 2.5)]
drone1 = Node(position = drone_positions[0], velocity = Vector(0, 0), mass = 1, J = 1, ω = 0)
drone2 = Node(position = drone_positions[1], velocity = Vector(0, 0), mass = 1, J = 1, ω = 0)
drone3 = Node(position = drone_positions[2], velocity = Vector(0, 0), mass = 1, J = 1, ω = 0)

# Add a few boundary conditions so that the drone is held together
drone_strut12 = Spring(
            drone1,
            drone2,
            stiffness_N_per_m = 1000,
            damping_Ns_per_m = 30,
            l0 = (drone_positions[0] - drone_positions[1]).length(),
            rotational_damping_Nm_per_rads = 2.3)
drone_strut13 = Spring(
            drone1,
            drone3,
            stiffness_N_per_m = 1000,
            damping_Ns_per_m = 30,
            l0 = (drone_positions[0] - drone_positions[2]).length(),
            rotational_damping_Nm_per_rads = 2.3)
drone_strut23 = Spring(
            drone2,
            drone3,
            stiffness_N_per_m = 1000,
            damping_Ns_per_m = 30,
            l0 = (drone_positions[1] - drone_positions[2]).length(),
            rotational_damping_Nm_per_rads = 2.3)


################################################################
# Create the tool
################################################################

# Create three nodes to represent the tool
tool_positions = [Vector(0, 0), Vector(-0.5, 0.5), Vector(0.5, 0.5)]
tool1 = Node(position = tool_positions[0], velocity = Vector(0, 0), mass = 1, J = 1, ω = 0)
tool2 = Node(position = tool_positions[1], velocity = Vector(0, 0), mass = 1, J = 1, ω = 0)
tool3 = Node(position = tool_positions[2], velocity = Vector(0, 0), mass = 1, J = 1, ω = 0)

# Add a few boundary conditions so that the tool is held together
tool_strut12 = Spring(
            tool1,
            tool2,
            stiffness_N_per_m = 1000,
            damping_Ns_per_m = 30,
            l0 = (tool_positions[0] - tool_positions[1]).length(),
            rotational_damping_Nm_per_rads = 2.3)
tool_strut13 = Spring(
            tool1,
            tool3,
            stiffness_N_per_m = 1000,
            damping_Ns_per_m = 30,
            l0 = (tool_positions[0] - tool_positions[2]).length(),
            rotational_damping_Nm_per_rads = 2.3)
tool_strut23 = Spring(
            tool2,
            tool3,
            stiffness_N_per_m = 1000,
            damping_Ns_per_m = 30,
            l0 = (tool_positions[1] - tool_positions[2]).length(),
            rotational_damping_Nm_per_rads = 2.3)

################################################################
# Create lines between tool and drone
################################################################


line1 = Spring(
            drone2,
            tool2,
            stiffness_N_per_m = 100,
            damping_Ns_per_m = 30,
            l0 = (drone_positions[1] - tool_positions[1]).length(),
            rotational_damping_Nm_per_rads = 2.3)
line2 = Spring(
            drone3,
            tool3,
            stiffness_N_per_m = 100,
            damping_Ns_per_m = 30,
            l0 = (drone_positions[2] - tool_positions[2]).length(),
            rotational_damping_Nm_per_rads = 2.3)


################################################################
# The world class helps us draw and run the simulation like a game
################################################################

from world import *

world = World()

world.add_node(drone1)
world.add_node(drone2)
world.add_node(drone3)

world.add_interaction(drone_strut12)
world.add_interaction(drone_strut13)
world.add_interaction(drone_strut23)

world.add_node(tool1)
world.add_node(tool2)
world.add_node(tool3)

world.add_interaction(tool_strut12)
world.add_interaction(tool_strut13)
world.add_interaction(tool_strut23)

world.add_interaction(line1)
world.add_interaction(line2)

world.run()
