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
        self.background = self.screen.copy()
        self.background.fill((255,255,255))  # Set background to white TODO image?
        self.screen.blit(self.background, (0,0))
        self.interleaving = 20

    def add_node(self, node):
        if isinstance(node, list):
            for node_ in node:
                self.add_node(node_)
            return node
        else:
            node.world = self
            self.nodes.append(node)
        return node

    def add_interaction(self, interaction):
        if isinstance(interaction, list):
            for interaction_ in interaction:
                self.add_interaction(interaction_)
            return interaction
        interaction.world = self
        self.interactions.append(interaction)
        return interaction

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
        fps_target = 30
        dt = self.clock.tick(self.interleaving*fps_target)*1e-3
        if dt == 0:
            return (self.t, 1/fps_target)
        fps_actual = 1/self.interleaving/dt
        if fps_actual < 0.75*fps_target:
            print(f"warning fps actual low ({1/dt/self.interleaving})")
        self.t += dt
        return (self.t, dt)
