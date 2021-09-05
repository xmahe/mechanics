import pygame
from vector import *

class Node:
    def __init__(self, p, v, mass):
        self.p = p
        self.v = v
        self.mass = mass
        self.f = Vector(0, 0)
        self.condition = None
    def reset(self):
        self.f = Vector(0, 0)
    def apply_force(self, f):
        self.f += f
    def simulate(self, dt, t):
        def RK45(dt, f, t, x):  # Runge-Kutta 45, solves f(t,x) = dx/dt
            k1 = dt*f(t, x)
            k2 = dt*f(t+dt/2, x+k1/2)
            k3 = dt*f(t+dt/2, x+k2/2)
            k4 = dt*f(t+dt  , x+k3  )
            return x + k1/6 + k2/3 + k3/3 + k4/6
        # acc = force / mass = dvelocity/dt, f(t,velocity) = force/mass (a constant)
        self.v.x = RK45(dt, lambda t, f: self.f.x/self.mass, t, self.v.x)
        self.v.y = RK45(dt, lambda t, f: self.f.y/self.mass, t, self.v.y)
        # dposition/dt = velocity = f(t,position) (a constant as well)
        self.p.x = RK45(dt, lambda t, f: self.v.x       , t, self.p.x)
        self.p.y = RK45(dt, lambda t, f: self.v.y       , t, self.p.y)
    def draw(self):
        pygame.draw.circle(self.world.screen, (10,10, 10), self.world.world_to_screen_transform(self.p), 5)

class FixedNode(Node):
    def __init__(self, p, m):
        super().__init__(p, Vector(0, 0), m)
    def reset(self):
        pass
    def apply_force(self, f):
        pass
    def simulate(self, dt, t):
        pass

