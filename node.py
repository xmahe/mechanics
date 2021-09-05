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
        #def RK45(dt, f, t, x):  # Runge-Kutta 45, solves f(t,x) = dx/dt
        #    k1 = dt*f(t, x)
        #    k2 = dt*f(t+dt/2, x+k1/2)
        #    k3 = dt*f(t+dt/2, x+k2/2)
        #    k4 = dt*f(t+dt  , x+k3  )
        #    return x + k1/6 + k2/3 + k3/3 + k4/6
        ## acc = force / mass = dvelocity/dt, f(t,velocity) = force/mass (a constant)
        #self.v.x = RK45(dt, lambda t, f: self.f.x/self.mass, t, self.v.x)
        #self.v.y = RK45(dt, lambda t, f: self.f.y/self.mass, t, self.v.y)
        ##if self.startup:
        ##    if self.v.x > +0.5: self.v.x = +0.5
        ##    if self.v.x < -0.5: self.v.x = -0.5
        ##    if self.v.y > +0.5: self.v.y = +0.5
        ##    if self.v.y < -0.5: self.v.y = -0.5
        ## dposition/dt = velocity = f(t,position) (a constant as well)
        #self.p.x = RK45(dt, lambda t, f: self.v.x       , t, self.p.x)
        #self.p.y = RK45(dt, lambda t, f: self.v.y       , t, self.p.y)
        ## dω/dt  = τ/J, f(t, ω) = τ/J (τ constant)
        #self.ω   = RK45(dt, lambda t, f: self.τ/self.J  , t, self.ω)
        ## dΘ/dt = ω, f(t, Θ) = ω (ω constant)
        #self.θ   = RK45(dt, lambda t, f: self.ω         , t, self.θ)


        def implicit_Euler_constant_f(dt, f, x0):
            #f(t,x) = dx/dt
            x1 = x0 + dt*f
            return x1

        # acc = force / mass = dvelocity/dt, f(t,velocity) = force/mass (a constant)
        a_lim = 100
        #if self.f.x/self.mass > +a_lim: self.f.x = +a_lim*self.mass
        #if self.f.x/self.mass < -a_lim: self.f.x = -a_lim*self.mass
        self.v.x = implicit_Euler_constant_f(dt, self.f.x/self.mass, self.v.x)
        if self.f.x/self.mass > +a_lim: self.v.x *= 0.85
        if self.f.x/self.mass < -a_lim: self.v.x *= 0.85
        #if self.f.y/self.mass > +a_lim: self.f.y = +a_lim*self.mass
        #if self.f.y/self.mass < -a_lim: self.f.y = -a_lim*self.mass
        self.v.y = implicit_Euler_constant_f(dt, self.f.y/self.mass, self.v.y)
        if self.f.y/self.mass > +a_lim: self.v.y *= 0.85
        if self.f.y/self.mass < -a_lim: self.v.y *= 0.85
        # dposition/dt = velocity = f(t,position) (a constant as well)
        self.p.x = implicit_Euler_constant_f(dt, self.v.x, self.p.x)
        self.p.y = implicit_Euler_constant_f(dt, self.v.y, self.p.y)
        # dω/dt  = τ/J, f(t, ω) = τ/J (τ constant)
        self.ω   = implicit_Euler_constant_f(dt, self.τ/self.J, self.ω)
        # dΘ/dt = ω, f(t, Θ) = ω (ω constant)
        self.θ   = implicit_Euler_constant_f(dt, self.ω, self.θ)

    def draw(self):
        pygame.draw.circle(self.world.screen, (10,10, 10), self.world.world_to_screen_transform(self.p), self.radius)
        #pygame.draw.line(self.world.screen, (100,100,255), self.world.world_to_screen_transform(self.p), self.world.world_to_screen_transform(self.p + self.v), 2)
        if self.mass > 0:
            #pygame.draw.line(self.world.screen, (255,100,100), self.world.world_to_screen_transform(self.p), self.world.world_to_screen_transform(self.p + self.f.scale(1e-3/self.mass)), 2)
            pass

class FixedNode(Node):
    def __init__(self, position):
        super().__init__(position, Vector(0, 0), 1, 1)
    def reset(self):
        pass
    def apply_force(self, f):
        pass
    def apply_torque(self, τ):
        pass
    def simulate(self, dt, t):
        pass

class VirtualNode(Node):
    # Used for nodes belonging to bounded boxes, with no own mass
    def __init__(self, cm, position_relative_to_cm):
        super().__init__(cm.p + position_relative_to_cm, Vector(0, 0), 0, 0)
        self.cm = cm
        self.position_relative_to_cm = position_relative_to_cm
    def reset(self):
        pass
    def apply_force(self, f):
        # A force applied to a virtual node gets propagated to it's cm-node instead
        self.cm.apply_force_at(f, self.position_relative_to_cm)
    def apply_torque(self, f):
        raise Exception("Not implemented!") # TODO implement
    def simulate(self, dt, t):
        rotated = self.position_relative_to_cm.rotate(self.cm.θ)
        self.p = self.cm.p + rotated
        self.v = self.cm.v + rotated.scale(self.cm.ω).rotate90CCW()
