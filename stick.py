import pygame
from math import sin, pi

running = 1
clock = pygame.time.Clock()
t = 0

screen_x_px = 600
screen_y_px = 600
screen = pygame.display.set_mode((screen_x_px, screen_y_px))
origo = (screen_x_px/2, screen_y_px/2)
screen_height_m = 5
screen_width_m = screen_height_m
pixel_per_m = screen_y_px / screen_height_m
lookat = (0,1)
def world_to_screen_transform(position_m):
    x_m = position_m.x
    y_m = position_m.y
    return (          0 + (x_m - lookat[0])*pixel_per_m + origo[0],
            screen_y_px - (y_m - lookat[1])*pixel_per_m - origo[1])  # y grows in "wrong" direction


class Vector:
    class TooShort(Exception):
        pass

    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def scale(self, factor):
        return Vector(self.x*factor, self.y*factor)
    def length(self):
        return (self.x**2 + self.y**2)**0.5
    def normal(self):
        l = self.length()
        if l < 1e-5:
            raise Vector.TooShort()
        return self.scale(1/l)
    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f})"
    def dot(self, other):
        return self.x*other.x + self.y*other.y
    def cross(self, other):
        return Vector(self.x*other.y, self.y*other.x)
    def rotate90CCW(self):
        return Vector(-self.y, self.x)
    def rotate90CW(self):
        return Vector(self.y, -self.x)

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
        node.v.x = RK45(dt, lambda t, f: node.f.x/node.mass, t, node.v.x)
        node.v.y = RK45(dt, lambda t, f: node.f.y/node.mass, t, node.v.y)
        # dposition/dt = velocity = f(t,position) (a constant as well)
        node.p.x = RK45(dt, lambda t, f: node.v.x       , t, node.p.x)
        node.p.y = RK45(dt, lambda t, f: node.v.y       , t, node.p.y)
    def draw(self):
        pygame.draw.circle(screen, (10,10, 10), world_to_screen_transform(self.p), 5)

class FixedNode(Node):
    def __init__(self, p, m):
        super().__init__(p, Vector(0, 0), m)
    def reset(self):
        pass
    def apply_force(self, f):
        pass
    def simulate(self, dt, t):
        pass


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
            n_hat = (self.a.p - self.b.p).normal()
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
        pygame.draw.line(screen, (100,100,100),
                world_to_screen_transform(self.a.p),
                world_to_screen_transform(self.b.p),
                2)

class Gravity(Interaction):
    def __init__(self, node):
        self.node = node
    def apply(self):
        g = 9.82
        gravity = Vector(0, -node.mass*g)
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

nodes = []
interactions = []

nodes.append(FixedNode(Vector(0, 2), 1))
nodes.append(Node(Vector(1, 2), Vector(0.1, 0), 1))
nodes.append(Node(Vector(2, 3), Vector(-3, 3), 1))

interactions.append(Gravity(nodes[1]))
interactions.append(Gravity(nodes[2]))
interactions.append(Floor(nodes[1]))
interactions.append(Floor(nodes[2]))
interactions.append(Spring(nodes[0], nodes[1]))


while running:
    # Increase time and monitor framerate
    fps_target = 60
    dt = clock.tick(fps_target)*1e-3
    fps_actual = 1/dt
    if fps_actual < 0.75*fps_target:
        print(f"warning fps actual low ({1/dt})")
    t += dt

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        #elif event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_UP:
        #        pass
        #elif event.type == pygame.MOUSEMOTION:
        #print(f"mouse at {event.pos}")
        #LEFT = 1
        #if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        #    print(f"You pressed the left mouse button at {event.pos}")
        #else:
        #    #print(event.type)
        #    pass

    # Physics computations
    for node in nodes:
        node.reset()  # Reset forces
    for interaction in interactions:
        interaction.apply()  # Compute forces
    for node in nodes:
        node.simulate(dt,t)  # Step all nodes forward in time

    # Draw graphics
    screen.fill((255,255,255))
    for node in nodes:
        node.draw()
    for interaction in interactions:
        interaction.draw()
    pygame.display.flip()
