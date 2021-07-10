import pygame
import time
import math

import helperFunctions as hf
from shell import Shell


class Tank:

    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.x_vel = 0
        self.y_vel = 0
        self.turret_angle = 0
        self.last_shot_time = time.time()
        self.hull_color = (255, 255, 255)
        self.turret_color = (0, 0, 0)
        self.width = 20
        self.height = 20
        self.autofire = False
        self.tank_speed = 4
        self.screen = screen
        self.shell_vel = 4

        self.hull = pygame.Rect(self.x, self.y, 20, 20)

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    def set_x_vel(self, x_vel):
        self.x_vel = x_vel

    def set_y_vel(self, y_vel):
        self.y_vel = y_vel

    def change_vels(self, delta_x, delta_y):
        self.x_vel += delta_x
        self.y_vel += delta_y

    def set_vels(self, delta_x, delta_y):
        self.x_vel = delta_x
        self.y_vel = delta_y

    def get_vels(self):
        return (self.x_vel, self.y_vel)

    def get_speed(self):
        return self.tank_speed

    def turn_turret(self, degrees):
        self.turret_angle += degrees

    def set_turret_angle(self, degrees):
        self.turret_angle = degrees

    def get_turret_angle(self):
        self.turret_angle = self.turret_angle % 360
        return self.turret_angle

    def update_rect(self):
        self.get_rect().update(self.x, self.y, self.width, self.height)

    def get_rect(self):
        return self.hull

    def render(self):
        self.hull = pygame.draw.rect(self.screen, self.hull_color, [
                                     self.x, self.y, self.width, self.height])
        hf.rectRotated(self.screen, self.turret_color, (self.x + 7.5,
                       self.y - 10, 5, 20), 0, 0, self.turret_angle, (0, 10), 8)

    def move(self, walls):

        self.x += self.x_vel
        self.update_rect()

        for wall in walls:
            while wall.colliderect(self.get_rect()):
                if self.x_vel < 0:
                    self.x += 1
                elif self.x_vel > 0:
                    self.x -= 1
                self.update_rect()

        self.y += self.y_vel
        self.update_rect()

        for wall in walls:
            while wall.colliderect(self.get_rect()):
                if self.y_vel < 0:
                    self.y += 1
                elif self.y_vel > 0:
                    self.y -= 1
                self.update_rect()

    def dummy_fire(self):
        temp = self.last_shot_time
        shell = self.fire(-1)
        self.last_shot_time = temp
        return shell

    def fire(self, delay=1):
        if time.time() - self.last_shot_time > delay:

            self.turret_angle = self.turret_angle % 360
            quadrant = self.turret_angle // 90
            angle = self.turret_angle
            if quadrant == 0:
                x_vel = -1 * math.sin(hf.dToR(angle)) * self.shell_vel
                y_vel = -1 * math.cos(hf.dToR(angle)) * self.shell_vel

            elif quadrant == 1:
                angle -= 90
                y_vel = math.sin(hf.dToR(angle)) * self.shell_vel
                x_vel = -1 * math.cos(hf.dToR(angle)) * self.shell_vel

            elif quadrant == 2:
                angle -= 180
                x_vel = math.sin(hf.dToR(angle)) * self.shell_vel
                y_vel = math.cos(hf.dToR(angle)) * self.shell_vel

            else:
                angle -= 270
                y_vel = -1 * math.sin(hf.dToR(angle)) * self.shell_vel
                x_vel = math.cos(hf.dToR(angle)) * self.shell_vel

            self.last_shot_time = time.time()
            return Shell(self.x + self.width / 2, self.y + self.height / 2, x_vel, y_vel, self, self.screen)

        return None
