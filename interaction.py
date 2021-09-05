import pygame
from vector import *

class Interaction():
    # Any physical interaction between two objects
    def __init(self):
        pass
    def apply(self):
        pass
    def draw(self):
        pass

class Spring(Interaction):
    def __init__(self, world, node_a, node_b, stiffness_N_per_m = 1000, damping_Ns_per_m = 30, l0 = 1, rotational_damping_Nm_per_rads = 2.3):
        self.a = node_a
        self.b = node_b
        self.k = stiffness_N_per_m
        self.l0 = l0
        self.damping_Ns_per_m = damping_Ns_per_m
        self.rotational_damping_Nm_per_rads = rotational_damping_Nm_per_rads
        self.world = world
        world.add_interaction(self)
    def apply(self):
        # Find the normal of the spring
        try:
            n_hat = (self.a.p - self.b.p).normalise()
            j_hat = n_hat.rotate90CCW()
            distance = (self.a.p - self.b.p).length()
            speed = (self.a.v.dot(n_hat) - self.b.v.dot(n_hat))
            rotational_speed = (self.a.v.dot(j_hat) - self.b.v.dot(j_hat))/distance
        except Vector.TooShort:
            return

        force = self.k * (distance - self.l0) + self.damping_Ns_per_m*speed
        rotational_damping = rotational_speed * self.rotational_damping_Nm_per_rads * distance
        # apply equal and opposite forces on both nodes
        self.a.apply_force(n_hat.scale(-force) + j_hat.scale(-rotational_damping))
        self.b.apply_force(n_hat.scale(+force) + j_hat.scale(+rotational_damping))
    def draw(self):
        pygame.draw.line(self.world.screen, (100,100,100),
                self.world.world_to_screen_transform(self.a.p),
                self.world.world_to_screen_transform(self.b.p),
                2)

class Gravity(Interaction):
    def __init__(self, world, node):
        self.node = node
        world.add_interaction(self)
    def apply(self):
        g = 9.82
        gravity = Vector(0, -self.node.mass*g)
        self.node.apply_force(gravity)

class Floor(Interaction):
    def __init__(self, world, node):
        self.node = node
        world.add_interaction(self)
    def apply(self):
        if self.node.p.y < 0:
            self.node.p.y = 0
            if self.node.f.y < 0:
                self.node.f.y = 0
            if self.node.v.y < 0:
                self.node.v.y *= -0.4
            self.node.v.x *= 0.95

class Drag(Interaction):
    def __init__(self, world, node, drag_coefficient = 0.1):
        self.node = node
        self.drag_coefficient = drag_coefficient
        self.transition_speed = 1
        self.linear_drag = drag_coefficient*self.transition_speed
        world.add_interaction(self)
    def apply(self):
        v = self.node.v.length()
        if v < 0.01:
            return
        elif v < self.transition_speed:
            self.node.apply_force(self.node.v.scale(-self.linear_drag))  # make sure this is smooth transition to other case
        else:
            v_hat = self.node.v.normalise()
            drag = -self.drag_coefficient*v**2
            self.node.apply_force(v_hat.scale(drag))

class BoundingBox(Interaction):
    def __init__(self, world, a, b, c, d, stiffness = 5000): # a,b,c,d must be given in CW order, or normal computations will be wrong
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.k = stiffness
        self.world = world
        world.add_interaction(self)
    def apply(self):
        # Loop through all nodes and see if any node has passed through bounding box
        # Simple neighbourhood check first
        x_min = min([self.a.x, self.b.x, self.c.x, self.d.x])
        y_min = min([self.a.y, self.b.y, self.c.y, self.d.y])
        x_max = max([self.a.x, self.b.x, self.c.x, self.d.x])
        y_max = max([self.a.y, self.b.y, self.c.y, self.d.y])
        close_nodes = [node for node in self.world.nodes if node.p.x < x_max and node.p.x > x_min and node.p.y < y_max and node.p.y > y_min]
        for node in close_nodes:
            def is_inside(p):
                at = (self.b - self.a).cross(p - self.a) > 0
                bt = (self.c - self.b).cross(p - self.b) > 0
                ct = (self.d - self.c).cross(p - self.c) > 0
                dt = (self.a - self.d).cross(p - self.d) > 0
                return at == bt and at == ct and at == dt
            if not is_inside(node.p):
                continue
            # At this point, we know we have a node which have entered a bounding box!
            # There should be force in the normal direction of the box.
            # 1. Compute normal of every line
            normals = [
                    (self.b - self.a).rotate90CCW().normalise(),
                    (self.c - self.b).rotate90CCW().normalise(),
                    (self.d - self.c).rotate90CCW().normalise(),
                    (self.a - self.d).rotate90CCW().normalise()]
            # 2. Compute middle point of every line
            midpoints = [
                    (self.a+self.b).scale(0.5),
                    (self.b+self.c).scale(0.5),
                    (self.c+self.d).scale(0.5),
                    (self.d+self.a).scale(0.5)]
            # 3. Compute normal dot (p - middle point of line) for every line
            distances = [normals[i].dot(midpoints[i] - node.p) for i in range(4)]
            # 4. The lowest value from step 3 is the line with the closest distance
            index = distances.index(min(distances))  # Search for minimum value item and return index O(n)
            # 5. Mirror the particle position and velocity around the closest line, if the n_hat*velocity is negative
            normal_velocity = normals[index].dot(node.v)
            if normal_velocity > 0:
                # don't do anything
                return
            damping = 0.10
            node.p = node.p + normals[index].scale(2*(midpoints[index] - node.p).dot(normals[index]))
            node.v = node.v - normals[index].scale(normal_velocity*(1+damping))
            # 6. Apply force to all nodes in bounding box? the center of mass of the box is used to also compute torque which are converted to forces as well

        # TODO check if a line passes through a bounding box, or a bounding box with a bounding box

    def draw(self):
        pygame.draw.lines(self.world.screen, (100,100,100), closed = True,
            points = [self.world.world_to_screen_transform(self.a),
                      self.world.world_to_screen_transform(self.b),
                      self.world.world_to_screen_transform(self.c),
                      self.world.world_to_screen_transform(self.d)],
            width = 2)

