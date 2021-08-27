import pygame
from math import sin, pi

screen = pygame.display.set_mode((400,400))
running = 1
clock = pygame.time.Clock()
t = 0

while running:
    # Increase time
    dt = clock.tick(30)
    t += dt*1e-3
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pass
        #elif event.type == pygame.MOUSEMOTION:
        #print(f"mouse at {event.pos}")
        #LEFT = 1
        #if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        #    print(f"You pressed the left mouse button at {event.pos}")
        else:
            #print(event.type)
            pass

    # Compute physics
    x = 50*sin(2*pi*t)
    screen.set_at((220,230), (255,0,0))

    # Draw graphics

    pygame.draw.line(screen, (0,0,255), (100,100), (200,150 + x), 5)

    pygame.display.flip()
