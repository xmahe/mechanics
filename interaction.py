import pygame
from vector import *
from node import *

class Interaction():
    # Any physical interaction between two objects
    def __init(self):
        pass
    def apply(self):
        pass
    def draw(self):
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
    def increase_length(self, Δx):
        self.l0 += Δx
    def set_length(self, l0):
        self.l0 = l0

class Gravity(Interaction):
    def __init__(self, node):
        self.node = node
    def apply(self):
        g = 9.82
        gravity = Vector(0, -self.node.mass*g)
        self.node.apply_force(gravity)

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
