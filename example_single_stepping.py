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
# Simulate the system a single step
################################################################

class System():
    # Helper class for single-stepping the simulation
    def __init__(self, nodes, interactions):
        self.nodes = nodes
        self.interactions = interactions
        self.t = 0

    def step(self, dt):
        self.t += dt
        for node in self.nodes:
            node.reset()  # Reset forces
        for interaction in self.interactions:
            interaction.apply()  # Compute forces
        for node in self.nodes:
            node.simulate(dt, self.t)  # Step all nodes forward in time

    def __str__(self):
        s = f"t = {self.t}\t"
        for node in self.nodes:
            s += str(node) + "\n"
        return s

# Create a System object for single-stepping the simulation
system = System([drone1, drone2, drone3, tool1, tool2, tool3], \
                [drone_strut12, drone_strut13, drone_strut23, tool_strut12, tool_strut13, tool_strut23, line1, line2])

# Time parameters
dt = 0.1

# Perform
print(f"System Step 0\n", system)

system.step(dt)
print(f"System step 1\n", system)

line1.increase_length(0.1)

system.step(dt)
print(f"System step 2\n", system)



# Maybe we want to inspect some system state at this point, e.g.
print(f"Tool node 2 has a lateral velocity of {tool2.v.x} m/s")

# Maybe we want to have a copy of our system state at this point and try what happens if we do a certain crazy thing
from copy import deepcopy
system_copy = deepcopy(system)
system_copy.nodes[0].v.x = 5
system_copy.interactions[0].increase_length(0.2)
system_copy.step(dt)
system_copy.step(dt)
system_copy.step(dt)
system_copy.step(dt)
print(system_copy)
del system_copy # remove copy entirely

# That was fun, but now we simulate our normal system again, which was not ruined by the above little test thing
system.step(dt)
print(f"System step 3\n", system)

