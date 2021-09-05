import pygame
from vector import *

class World:
    def __init__(self):
        self.nodes = list()
        self.interactions = list()
        self.clock = pygame.time.Clock()
        self.t = 0
        self.screen_x_px = 600
        self.screen_y_px = 600
        self.screen = pygame.display.set_mode((self.screen_x_px, self.screen_y_px))
        self.origo = (self.screen_x_px/2, self.screen_y_px/2)
        self.screen_height_m = 5
        self.screen_width_m = self.screen_height_m
        self.pixel_per_m = self.screen_y_px / self.screen_height_m
        self.lookat = (0,1)
        self.screen = pygame.display.set_mode((self.screen_x_px, self.screen_y_px))

    def add_node(self, node):
        self.nodes.append(node)

    def add_interaction(self, interaction):
        self.interactions.append(interaction)

    def world_to_screen_transform(self, position_m):
        x_m = position_m.x
        y_m = position_m.y
        return (               0 + (x_m - self.lookat[0])*self.pixel_per_m + self.origo[0],
                self.screen_y_px - (y_m - self.lookat[1])*self.pixel_per_m - self.origo[1])  # y grows in "wrong" direction

    def screen_to_world_transform(self, position_px):
        x_px = position_px[0]
        y_px = position_px[1]
        x_m = (                   x_px - self.origo[0])/self.pixel_per_m + self.lookat[0]
        y_m = (self.screen_y_px - y_px - self.origo[1])/self.pixel_per_m + self.lookat[1]
        return Vector(x_m, y_m)

    def tick(self):
        # Increase time and monitor framerate
        fps_target = 60
        dt = self.clock.tick(fps_target)*1e-3
        fps_actual = 1/dt
        if fps_actual < 0.75*fps_target:
            print(f"warning fps actual low ({1/dt})")
        self.t += dt
        return (self.t, dt)
