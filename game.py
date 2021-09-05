import pygame
from math import sin, pi

from Vector import *
from Node import *
from Interaction import *
from World import *

running = 1

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

def screen_to_world_transform(position_px):
    x_px = position_px[0]
    y_px = position_px[1]
    x_m = (              x_px - origo[0])/pixel_per_m + lookat[0]
    y_m = (screen_y_px - y_px - origo[1])/pixel_per_m + lookat[1]
    return Vector(x_m, y_m)

world = world()

world.add_node(FixedNode(Vector(0, 2),                 1, transform = world_to_screen_transform))
world.add_node(     Node(Vector(1, 2), Vector(0.1, 0), 1, transform = world_to_screen_transform))
world.add_node(     Node(Vector(2, 3), Vector(-3, 3) , 1, transform = world_to_screen_transform))

world.add_interaction(Gravity(nodes[1]))
world.add_interaction(Gravity(nodes[2]))
#world.add_interaction(Floor(nodes[1]))
#world.add_interaction(Floor(nodes[2]))
world.add_interaction(Spring(world.nodes[0], world.nodes[1]))
world.add_interaction(BoundingBox(Vector(1.2,0.6), Vector(1.1,-1.3), Vector(-1.4, -0.9), Vector(-0.8,1.6)))
world.add_interaction(Drag(nodes[1]))
world.add_interaction(Drag(nodes[2]))

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

        #    p = screen_to_world_transform(event.pos)


        #    def is_inside(box, p):
        #        r = interactions[-1]
        #        at = (r.b-r.a).cross(p-r.a) > 0
        #        bt = (r.c-r.b).cross(p-r.b) > 0
        #        ct = (r.d-r.c).cross(p-r.c) > 0
        #        dt = (r.a-r.d).cross(p-r.d) > 0
        #        return at == bt and at == ct and at == dt

        #    if is_inside(interactions[-1], p):
        #        print("You clicked inside!")

        ##    #print(f"Clicked at {p}, Bounding: {at}{bt}{ct}{dt}")

        #    nodes.append(Node(p, Vector(0,0), 1))
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
        node.draw(screen)
    for interaction in interactions:
        interaction.draw()
    #pygame.draw.line(screen, (100,100,100), world_to_screen_transform(Vector(-1000,0)), world_to_screen_transform(Vector(+1000,0)), 2)
    pygame.display.flip()
