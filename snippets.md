
### Add a pendulum
#fixed    = world.add_node(FixedNode(position = Vector(0, 2)))
#pendulum = world.add_node(     Node(position = Vector(1, 2.0), velocity = Vector(0.1, 0), mass = 1, J = 1))
#world.add_interaction(Gravity(pendulum))
#world.add_interaction(Drag(pendulum))
#world.add_interaction(Spring(fixed, pendulum, l0 = 1.0))

## Add a box
#box_cm = Node(position = Vector(0.2, -0.3), velocity = Vector(0.0, 0.0).scale(0), mass = 10, J = 5000, ω = 1.0)
#world.add_interaction(
#        BoundingBox(
#            world.add_node(box_cm),
#            world.add_node(VirtualNode(box_cm, position_relative_to_cm = Vector(+1.2, +0.6))),
#            world.add_node(VirtualNode(box_cm, position_relative_to_cm = Vector(+1.1, -1.3))),
#            world.add_node(VirtualNode(box_cm, position_relative_to_cm = Vector(-1.4, -0.9))),
#            world.add_node(VirtualNode(box_cm, position_relative_to_cm = Vector(-0.8, +1.6)))))
#
#world.add_interaction(Spring(FixedNode(position = Vector(0.2, -0.3)), box_cm, stiffness_N_per_m= 10000, rotational_damping_Nm_per_rads = 20, damping_Ns_per_m = 60, l0 = 0))
#world.add_interaction(Gravity(box_cm))

## Another, smaller, box
#small_cm = Node(position = Vector(-0.2, 2), velocity = Vector(0, -0.8), mass = 15, J = 2, ω=0)
#world.add_interaction(
#        BoundingBox(
#            world.add_node(small_cm),
#            world.add_node(VirtualNode(small_cm, position_relative_to_cm = Vector(+0.2, +0.2))),
#            world.add_node(VirtualNode(small_cm, position_relative_to_cm = Vector(+0.2, -0.2))),
#            world.add_node(VirtualNode(small_cm, position_relative_to_cm = Vector(-0.2, -0.2))),
#            world.add_node(VirtualNode(small_cm, position_relative_to_cm = Vector(-0.2, +0.2))),
#            ))
#
#world.add_interaction(Gravity(small_cm))

# # Rope
# rope = RopeBuilder(world, start = Vector(0, 2), stop = Vector(2, 2), N = 15)
# world.add_interaction(Spring(FixedNode(position = Vector(0, 2)), rope.nodes[0], l0 = 0))
#
# stone = world.add_node(Node(position = Vector(2, 2), mass = 5))
# stone.radius = 15
# world.add_interaction(Spring(rope.nodes[-1], stone, stiffness_N_per_m = 1e3, l0 = 0))
# world.add_interaction(Gravity(stone))

