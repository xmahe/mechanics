from world import *
from vector import *
from node import *
from interaction import *
import pygame


class Drone:
    def __init__(self, world):
        cm = world.add_node(
                Node(
                    position = Vector(0, 3),
                    velocity = Vector(-0.1, 2),
                    mass = 5,
                    J = 1))
        world.add_interaction(Gravity(cm))
        world.add_interaction(Drag(cm))
        world.add_interaction(Floor(cm))
        #world.add_interaction(RawControl(cm))
        #world.add_interaction(AcroModeControl(cm))
        #world.add_interaction(AcroModeAltitudeControl(cm))
        world.add_interaction(StabilisedControl(cm))
        world.add_interaction(Sprite(cm, 'drone.png'))
        world.add_interaction(
                BoundingBox(
                    world.add_node(cm),
                    world.add_node(VirtualNode(cm, position_relative_to_cm = Vector(+1.2, +0.6))),
                    world.add_node(VirtualNode(cm, position_relative_to_cm = Vector(+1.1, -1.3))),
                    world.add_node(VirtualNode(cm, position_relative_to_cm = Vector(-1.4, -0.9))),
                    world.add_node(VirtualNode(cm, position_relative_to_cm = Vector(-0.8, +1.6)))))


class RawControl(Interaction):
    def __init__(self, node):
        self.node = node
        self.keys = []
        self.accelerating_up = False
        self.accelerating_down = False
        self.turning_right = False
        self.turning_left = False
    def apply(self):
        #self.node.apply_force(Vector(0,35).rotate(self.node.θ))
        if self.accelerating_up:
            self.node.apply_force(Vector(0,75).rotate(self.node.θ))
        if self.accelerating_down:
            self.node.apply_force(Vector(0,0*-35).rotate(self.node.θ))
        if self.turning_left:
            self.node.apply_torque(10)
        if self.turning_right:
            self.node.apply_torque(-10)

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.accelerating_up = True
                if event.key == pygame.K_RIGHT:
                    self.turning_right = True
                if event.key == pygame.K_LEFT:
                    self.turning_left = True
                if event.key == pygame.K_DOWN:
                    self.accelerating_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.accelerating_up = False
                if event.key == pygame.K_RIGHT:
                    self.turning_right = False
                if event.key == pygame.K_LEFT:
                    self.turning_left = False
                if event.key == pygame.K_DOWN:
                    self.accelerating_down = False

class AcroModeAltitudeControl(Interaction):
    def __init__(self, node):
        self.node = node
        self.keys = []
        self.accelerating_up = False
        self.accelerating_down = False
        self.turning_right = False
        self.turning_left = False

        self.MAX_ROTATIONAL_SPEED = 5
        self.z = 0
        self.ω_ref_last = 0

        self.MAX_CLIMB_SPEED = 2
        self.vy_error_integrated = 0
        self.vy_last = 0
        self.diff_last = 0

    def _angular_rate_feedback(self, ω_ref):
        k = 0.11
        p = 10

        # Filter
        ω_ref = ω_ref * k + self.ω_ref_last * (1 - k)
        self.ω_ref_last = ω_ref

        # Error feedback ctrl
        error = ω_ref - self.node.ω

        return p*error

    def _altitude_rate_feedback(self, vy_ref):
        error = vy_ref - self.node.v.y

        p = 10
        i = 0.05
        d = 1000

        self.vy_error_integrated += error

        diff = self.node.v.y - self.vy_last

        k = 0.2
        diff = diff*k + self.diff_last * (1-k)
        self.diff_last = diff
        self.vy_last = self.node.v.y
        #print(f"P = {error*p}, I = {self.vy_error_integrated*i}, D = {diff*d}")

        PID_out = error*p + self.vy_error_integrated*i + diff*d

        return Vector(0, PID_out)

    def apply(self):
        if self.accelerating_up:
            vy_ref = +self.MAX_CLIMB_SPEED
        elif self.accelerating_down:
            vy_ref = -self.MAX_CLIMB_SPEED
        else:
            vy_ref = 0
        self.node.apply_force(self._altitude_rate_feedback(vy_ref).rotate(self.node.θ))

        if self.turning_left:
            ω_ref = +self.MAX_ROTATIONAL_SPEED
        elif self.turning_right:
            ω_ref = -self.MAX_ROTATIONAL_SPEED
        else:
            ω_ref = 0
        self.node.apply_torque(self._angular_rate_feedback(ω_ref))


    def handle_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.accelerating_up = True
                if event.key == pygame.K_RIGHT:
                    self.turning_right = True
                if event.key == pygame.K_LEFT:
                    self.turning_left = True
                if event.key == pygame.K_DOWN:
                    self.accelerating_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.accelerating_up = False
                if event.key == pygame.K_RIGHT:
                    self.turning_right = False
                if event.key == pygame.K_LEFT:
                    self.turning_left = False
                if event.key == pygame.K_DOWN:
                    self.accelerating_down = False

class AcroModeControl(Interaction):
    def __init__(self, node):
        self.node = node
        self.keys = []
        self.accelerating_up = False
        self.accelerating_down = False
        self.turning_right = False
        self.turning_left = False

        self.MAX_ROTATIONAL_SPEED = 5
        self.z = 0
        self.ω_ref_last = 0

    def _angular_rate_feedback(self, ω_ref):
        k = 0.11
        p = 10

        # Filter
        ω_ref = ω_ref * k + self.ω_ref_last * (1 - k)
        self.ω_ref_last = ω_ref

        # Error feedback ctrl
        error = ω_ref - self.node.ω

        return p*error

    def _altitude_rate_feedback(self):
        pass

    def apply(self):
        self.node.apply_force(Vector(0,35).rotate(self.node.θ))
        if self.accelerating_up:
            self.node.apply_force(Vector(0,50).rotate(self.node.θ))
        if self.accelerating_down:
            self.node.apply_force(Vector(0,-35).rotate(self.node.θ))

        if self.turning_left:
            ω_ref = +self.MAX_ROTATIONAL_SPEED
        elif self.turning_right:
            ω_ref = -self.MAX_ROTATIONAL_SPEED
        else:
            ω_ref = 0
        self.node.apply_torque(self._angular_rate_feedback(ω_ref))


    def handle_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.accelerating_up = True
                if event.key == pygame.K_RIGHT:
                    self.turning_right = True
                if event.key == pygame.K_LEFT:
                    self.turning_left = True
                if event.key == pygame.K_DOWN:
                    self.accelerating_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.accelerating_up = False
                if event.key == pygame.K_RIGHT:
                    self.turning_right = False
                if event.key == pygame.K_LEFT:
                    self.turning_left = False
                if event.key == pygame.K_DOWN:
                    self.accelerating_down = False

class StabilisedControl(Interaction):
    def __init__(self, node):
        self.node = node
        self.keys = []
        self.accelerating_up = False
        self.accelerating_down = False
        self.turning_right = False
        self.turning_left = False

        self.MAX_TILT = 0.3
        self.z = 0
        self.ω_ref_last = 0

        self.MAX_CLIMB_SPEED = 2
        self.vy_error_integrated = 0
        self.vy_last = 0
        self.diff_last = 0

    def _angular_rate_feedback(self, ω_ref):
        k = 0.11
        p = 10

        # Filter
        ω_ref = ω_ref * k + self.ω_ref_last * (1 - k)
        self.ω_ref_last = ω_ref

        # Error feedback ctrl
        error = ω_ref - self.node.ω

        return p*error

    def _altitude_rate_feedback(self, vy_ref):
        error = vy_ref - self.node.v.y

        p = 10
        i = 0.05
        d = 1000

        self.vy_error_integrated += error

        diff = self.node.v.y - self.vy_last

        k = 0.2
        diff = diff*k + self.diff_last * (1-k)
        self.diff_last = diff
        self.vy_last = self.node.v.y
        #print(f"P = {error*p}, I = {self.vy_error_integrated*i}, D = {diff*d}")

        PID_out = error*p + self.vy_error_integrated*i + diff*d

        return Vector(0, PID_out)

    def _stabilisation_feedback(self, θ_ref):
        p = 10
        error = θ_ref - self.node.θ
        PID_out = error*p

        return PID_out  # ω_ref


    def apply(self):
        if self.accelerating_up:
            vy_ref = +self.MAX_CLIMB_SPEED
        elif self.accelerating_down:
            vy_ref = -self.MAX_CLIMB_SPEED
        else:
            vy_ref = 0

        self.node.apply_force(self._altitude_rate_feedback(vy_ref).rotate(self.node.θ))

        if self.turning_left:
            θ_ref = +self.MAX_TILT
        elif self.turning_right:
            θ_ref = -self.MAX_TILT
        else:
            θ_ref = 0

        ω_ref = self._stabilisation_feedback(θ_ref)
        self.node.apply_torque(self._angular_rate_feedback(ω_ref))


    def handle_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.accelerating_up = True
                if event.key == pygame.K_RIGHT:
                    self.turning_right = True
                if event.key == pygame.K_LEFT:
                    self.turning_left = True
                if event.key == pygame.K_DOWN:
                    self.accelerating_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.accelerating_up = False
                if event.key == pygame.K_RIGHT:
                    self.turning_right = False
                if event.key == pygame.K_LEFT:
                    self.turning_left = False
                if event.key == pygame.K_DOWN:
                    self.accelerating_down = False
