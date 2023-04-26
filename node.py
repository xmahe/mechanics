import pygame
from vector import *

class Node:
    def __init__(self, position, velocity = Vector(0, 0), mass = 1, J = 1, ω = 0):
        self.mass = mass
        self.p = position
        self.v = velocity
        self.f = Vector(0, 0)
        self.J = J
        self.θ = 0
        self.ω = ω
        self.τ = 0
        self.condition = None
        self.radius = 4
        self.startup = True

    def reset(self):
        self.f = Vector(0, 0)
        self.τ = 0

    def apply_force(self, f):
        self.f += f

    def apply_torque(self, τ):
        self.τ += τ

    def apply_force_at(self, f, r_world):
        self.apply_force(f)
        r = r_world - self.p
        self.apply_torque(r.cross(f))

    def simulate(self, dt, t):
        def integrate(dt, f, x0):
            # Based on Implicit Euler Method (?)
            #f(t,x) = dx/dt
            x1 = x0 + dt*f
            return x1

        # Magically make simulation a bit more stable by decreasing speed
        # if acceleration is very high (high acceleration == stiff problem)
        a_lim = 100
        if self.f.x/self.mass > +a_lim: self.v.x *= 0.85
        if self.f.x/self.mass < -a_lim: self.v.x *= 0.85
        if self.f.y/self.mass > +a_lim: self.v.y *= 0.85
        if self.f.y/self.mass < -a_lim: self.v.y *= 0.85

        # Update states by integrating them
        # acc = force / mass = dvelocity/dt, f(t,velocity) = force/mass (a constant)
        self.v = integrate(dt, self.f / self.mass, self.v)
        # dposition/dt = velocity = f(t,position) (a constant as well)
        self.p = integrate(dt, self.v, self.p)
        # dω/dt  = τ/J, f(t, ω) = τ/J (τ constant)
        self.ω   = integrate(dt, self.τ/self.J, self.ω)
        # dΘ/dt = ω, f(t, Θ) = ω (ω constant)
        self.θ   = integrate(dt, self.ω, self.θ)

    def draw(self):
        pygame.draw.circle(
                self.world.screen,
                (10, 10, 10),
                self.world.world_to_screen_transform(self.p),
                self.radius)

    def __str__(self):
        return f"m = {self.mass}\t" + \
               f"p = {self.p}\t" + \
               f"v = {self.v}\t" + \
               f"F = {self.f}\t" + \
               f"J = {self.J}\t" + \
               f"θ = {self.θ}\t" + \
               f"ω = {self.ω}\t" + \
               f"τ = {self.τ}"
