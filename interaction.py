import pygame
from vector import *
from node import *
from math import pi as π

class Interaction():
    # Any physical interaction between two objects
    def __init(self):
        pass
    def apply(self):
        pass
    def draw(self):
        pass
    def undraw(self):
        pass
    def handle_event(self, events):
        pass

class Spring(Interaction):
    def __init__(self, node_a, node_b, stiffness_N_per_m = 1000, damping_Ns_per_m = 30, l0 = 1, rotational_damping_Nm_per_rads = 2.3):
        self.a = node_a
        self.b = node_b
        self.k = stiffness_N_per_m
        self.l0 = l0
        self.damping_Ns_per_m = damping_Ns_per_m
        self.rotational_damping_Nm_per_rads = rotational_damping_Nm_per_rads
    def apply(self):
        # Find the normal of the spring
        try:
            n_hat = (self.a.p - self.b.p).normalise()
            j_hat = n_hat.rotate90CCW()
            distance = (self.a.p - self.b.p).length()
            speed = (self.a.v - self.b.v).dot(n_hat)
            rotational_speed = (self.a.v - self.b.v).dot(j_hat)/distance
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
    def __init__(self, node):
        self.node = node
    def apply(self):
        g = 9.82
        gravity = Vector(0, -self.node.mass*g)
        self.node.apply_force(gravity)

class Sprite(Interaction):
    def __init__(self, node, filename):
        self.node = node
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.pluscenter = (+self.rect[2]/2, +self.rect[3]/2)
        self.minuscenter = (-self.rect[2]/2, -self.rect[3]/2)
    def apply(self):
        pass
    def draw(self):
        x = self.world.world_to_screen_transform(self.node.p)
        rotated_sprite = pygame.transform.rotate(self.image,self.node.θ*360/2/π)
        self.rect = rotated_sprite.get_rect(center = self.pluscenter)
        self.world.screen.blit(rotated_sprite, self.rect.move(x).move(self.minuscenter))
    def undraw(self):
        x = self.world.world_to_screen_transform(self.node.p)
        y = self.rect.move(x)
        self.world.screen.blit(self.world.background, y.move(self.minuscenter), y)
    def handle_event(self, events):
        pass


class Floor(Interaction):
    def __init__(self, node):
        self.node = node
    def apply(self):
        if self.node.p.y < 0:
            self.node.p.y = 0
            if self.node.f.y < 0:
                self.node.f.y = 0
            if self.node.v.y < 0:
                self.node.v.y *= -0.4
            self.node.v.x *= 0.95

class Drag(Interaction):
    def __init__(self, node, drag_coefficient = 0.1):
        self.node = node
        self.drag_coefficient = drag_coefficient
        self.transition_speed = 1
        self.linear_drag = drag_coefficient*self.transition_speed
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
    def __init__(self, cm, a, b, c, d, stiffness = 5000): # a,b,c,d must be given in CW order, or normal computations will be wrong
        self.cm = cm
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.k = stiffness
        self.υ = 0.3
    def apply(self):
        # Loop through all nodes and see if any node has passed through bounding box
        # Simple neighbourhood check first
        x_min = min([self.a.p.x, self.b.p.x, self.c.p.x, self.d.p.x])
        y_min = min([self.a.p.y, self.b.p.y, self.c.p.y, self.d.p.y])
        x_max = max([self.a.p.x, self.b.p.x, self.c.p.x, self.d.p.x])
        y_max = max([self.a.p.y, self.b.p.y, self.c.p.y, self.d.p.y])
        close_nodes = [node for node in self.world.nodes if node.p.x < x_max and node.p.x > x_min and node.p.y < y_max and node.p.y > y_min]
        close_nodes = [node for node in close_nodes if not id(node) == id(self.cm)]
        #import pdb; pdb.set_trace()
        for node in close_nodes:
            def is_inside(p):
                at = (self.b.p - self.a.p).cross(p - self.a.p) > 0
                bt = (self.c.p - self.b.p).cross(p - self.b.p) > 0
                ct = (self.d.p - self.c.p).cross(p - self.c.p) > 0
                dt = (self.a.p - self.d.p).cross(p - self.d.p) > 0
                return at == bt and at == ct and at == dt
            if not is_inside(node.p):
                continue
            # At this point, we know we have a node which have entered a bounding box!
            # There should be force in the normal direction of the box.
            # 1. Compute normal of every line
            normals = [
                    (self.b.p - self.a.p).rotate90CCW().normalise(),
                    (self.c.p - self.b.p).rotate90CCW().normalise(),
                    (self.d.p - self.c.p).rotate90CCW().normalise(),
                    (self.a.p - self.d.p).rotate90CCW().normalise()]
            # 2. Compute middle point of every line
            midpoints = [
                    (self.a.p+self.b.p).scale(0.5),
                    (self.b.p+self.c.p).scale(0.5),
                    (self.c.p+self.d.p).scale(0.5),
                    (self.d.p+self.a.p).scale(0.5)]
            # 3. Compute normal dot (p - middle point of line) for every line
            distances = [normals[i].dot(midpoints[i] - node.p) for i in range(4)]
            # 4. The lowest value from step 3 is the line with the closest distance
            index = distances.index(min(distances))  # Search for minimum value item and return index O(n)
            distance = distances[index]
            midpoint = midpoints[index]
            n_hat    = normals[index]
            # Two options - if collision is high relative velocity, use momentum theory, otherwise, use normal forces
            spring_model = True
            if spring_model:
                abs_spring_force = self.k*distance
                spring_force = n_hat.scale(abs_spring_force)  # TODO add damping
                friction_force = n_hat.rotate90CCW().scale(self.υ*abs_spring_force)
                self.cm.apply_force_at(spring_force.scale(-1) - friction_force, node.p)
                node.apply_force(friction_force + spring_force.scale(1))
                continue
            else:
                continue

            # TODO check speed and implement both methods, compare with virtual nodes in corners
            # 5. Mirror the particle position and velocity around the closest line, if the n_hat*velocity is negative
            normal_velocity = normals[index].dot(node.v)
            if normal_velocity > 0:
                # don't do anything
                return
            damping = 0.30 # 0.10 equals 90% energy lost when bumping
            node.p = node.p + normals[index].scale(2*(midpoints[index] - node.p).dot(normals[index]))
            node.v = node.v - normals[index].scale(normal_velocity*(1+damping))
            # 6. Apply force to all nodes in bounding box? the center of mass of the box is used to also compute torque which are converted to forces as well
            self.cm
            #import pdb;pdb.set_trace()


        # TODO check if a line passes through a bounding box, or a bounding box with a bounding box

    def draw(self):
        pygame.draw.lines(self.world.screen, (100,100,100), closed = True,
            points = [self.world.world_to_screen_transform(self.a.p),
                      self.world.world_to_screen_transform(self.b.p),
                      self.world.world_to_screen_transform(self.c.p),
                      self.world.world_to_screen_transform(self.d.p)],
            width = 2)


def RopeBuilder(world, start, stop, N = 6):
    from numpy import linspace
    X = linspace(start.x, stop.x, N)
    Y = linspace(start.y, stop.y, N)
    L = (start-stop).length()
    dL = L / (N - 1)
    nodes = [Node(position = Vector(X[i], Y[i]), mass = 0.1, J = 0.1) for i in range(N)]
    world.add_node(nodes)
    rope = Rope(nodes)
    world.add_interaction(rope)
    for node in rope.nodes:
        world.add_interaction(Gravity(node))
    for i in range(N-1):
        world.add_interaction(Spring(nodes[i], nodes[i+1], l0 = dL, stiffness_N_per_m = (N-1)*1e3, damping_Ns_per_m = 0, rotational_damping_Nm_per_rads= 0))
    return rope

class Rope(Interaction):
    def __init__(self, nodes):
        self.nodes = nodes
    def apply(self):
        pass
    def draw(self):
        pygame.draw.lines(self.world.screen, (200,200,200), closed = False,
            points = [self.world.world_to_screen_transform(node.p) for node in self.nodes],
            width = 2)
