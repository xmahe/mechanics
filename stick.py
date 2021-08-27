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
    def __init__(self, p, v, m):
        self.p = p
        self.v = v
        self.m = m
        self.f = Vector(0, 0)

nodes = []


nodes.append(Node(Vector(100,100), Vector(0.1,0), 1))

while running:
    # Increase time
    dt = clock.tick(50)
    t += dt*1e-3
    screen.fill((0,0,0))

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
    #x = 50*sin(2*pi*t)

    ## Compute forces
    for node in nodes:
        # Gravity
        node.f += Vector(0, 0.001).scale(node.m)

        # Floor
        if node.p.y > 280:
            node.p.y = 280
            if node.f.y > 0:
                node.f.y = 0
            if node.v.y > 0:
                node.v.y *= -0.4
            node.v.x *= 0.95

    ## Compute positions
    for node in nodes:
        node.v += node.f.scale(1/node.m*dt)
        node.p += node.v.scale(dt)

    ## Reset forces
    for node in nodes:
        node.f = Vector(0, 0)

    # Draw graphics
    ## Nodes
    for node in nodes:
        pygame.draw.circle(screen, (200,200,255), (node.p.x, node.p.y), 5)

    #pygame.draw.line(screen, (0,0,255), (100,100), (200,150 + x), 5)
    #screen.set_at((220,230), (255,0,0))

    pygame.display.flip()
