import pygame
from math import sin, pi

screen = pygame.display.set_mode((400,400))
running = 1
clock = pygame.time.Clock()
t = 0

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def scale(self, factor):
        return Vector(self.x*factor, self.y*factor)

class Node:
    FIXED = 0
    def __init__(self, p, v, m):
        self.p = p
        self.v = v
        self.m = m
        self.f = Vector(0, 0)
        self.condition = None

class Link:
    def __init__(self, node_a, node_b):
        self.a = node_a
        self.b = node_b
    def apply_link_forces(self):
        # This is a rigid link
        # That means that forces in the link direction must be propagated through the link
        # pa = (1,1), ma = 1
        # pb = (2,2), mb = 2
        # external forces on nodes are fa = (0,1)
        # maybe b is rigid. what forces should b exert via the link to not move?
        # the direction of forces on b from a is (pa-pb)/|pa-pb| = (-1, -1)/2 = (-0.5, -0.5)

        pass


nodes = []


nodes.append(Node(Vector(100,100), Vector(0, 0), 1))
nodes.append(Node(Vector(100,100), Vector(0.1, 0), 1))
nodes.append(Node(Vector(230,100), Vector(33, 100), 1))


nodes[0].condition = Node.FIXED


while running:
    # Increase time
    dt = clock.tick(50)*1e-3
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

    # Compute physics
    ## Compute forces
    for node in nodes:
        # Gravity
        node.f += Vector(0, 10/dt).scale(node.m)
        # Floor
        if node.p.y > 280:
            node.p.y = 280
            if node.f.y > 0:
                node.f.y = 0
            if node.v.y > 0:
                node.v.y *= -0.4
            node.v.x *= 0.95

    for node in nodes:
        if node.condition == Node.FIXED:
            # Make sure this stays still by zeroing out all forces acting upon it from neighbours
            node.f = Vector(0, 0)

    ## Compute step
    for node in nodes:
        def RK45(dt, f, t, x):  # Runge-Kutta 45, solves f(t,x) = dx/dt
            k1 = dt*f(t, x)
            k2 = dt*f(t+dt/2, x+k1/2)
            k3 = dt*f(t+dt/2, x+k2/2)
            k4 = dt*f(t+dt  , x+k3  )
            return x + k1/6 + k2/3 + k3/3 + k4/6

        # acc = force / mass = dvelocity/dt, f(t,velocity) = force/mass (a constant)
        node.v.x = RK45(dt, lambda t, f: node.f.x/node.m, t, node.v.x)
        node.v.y = RK45(dt, lambda t, f: node.f.y/node.m, t, node.v.y)
        # dposition/dt = velocity = f(t,position) (a constant as well)
        node.p.x = RK45(dt, lambda t, f: node.v.x       , t, node.p.x)
        node.p.y = RK45(dt, lambda t, f: node.v.y       , t, node.p.y)

    ## Reset forces
    for node in nodes:
        node.f = Vector(0, 0)

    # Draw graphics
    screen.fill((0,0,0))
    ## Nodes
    for node in nodes:
        pygame.draw.circle(screen, (200,200,255), (node.p.x, node.p.y), 5)

    #pygame.draw.line(screen, (0,0,255), (100,100), (200,150 + x), 5)
    #screen.set_at((220,230), (255,0,0))

    pygame.display.flip()
