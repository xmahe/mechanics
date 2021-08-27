import pygame
from math import sin, pi

screen = pygame.display.set_mode((400,400))
running = 1
clock = pygame.time.Clock()
t = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pass
        else:
            #print(event.type)
            pass
    dt = clock.tick(30)
    t += dt*1e-3
    screen.set_at((220,230), (255,0,0))

    pygame.display.flip()
#while running:
#    # Increase time
#
#    # Check if there are any events to process
#    event = pygame.event.poll()
#    if event.type == pygame.QUIT:
#        print("Shutting down!")
#        running = 0
#    #if event.type == pygame.MOUSEMOTION:
#    #    pass
#    #    #print(f"mouse at {event.pos}")
#    #LEFT = 1
#    #if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
#    #    print(f"You pressed the left mouse button at {event.pos}")
#
#    # Compute physics
#    x = 50*sin(2*pi*t)
#
#    # Draw graphics
#    #pygame.draw.aaline
#    screen.fill((0,0,0))
#    pygame.draw.line(screen, (0,0,255), (100,100), (200,150 + x))
#
#    # Push graphics to screen
#    pygame.display.flip()
