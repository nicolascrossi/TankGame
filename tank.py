import pygame
import time
import math

import helperFunctions as hf
from shell import Shell

class Tank:

    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.xVel = 0
        self.yVel = 0
        self.turretAngle = 0
        self.lastShotTime = time.time()
        self.hullColor = (255, 255, 255)
        self.turretColor = (0, 0, 0)
        self.width = 20
        self.height = 20
        self.autofire = False
        self.tankSpeed = 4
        self.screen = screen

        self.hull = pygame.Rect(self.x, self.y, 20, 20)

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def turn_turret(self, degrees):
        self.turretAngle += degrees

    def set_turret_angle(self, degrees):
        self.turretAngle = degrees

    def move(self, deltaX, deltaY, walls):
        self.x += deltaX
        self.update_rect()

        for wall in walls:
            while wall.colliderect(self.get_rect()):
                if deltaX < 0:
                    self.x += 1
                elif deltaX > 0:
                    self.x -= 1
                self.update_rect()
        
        self.y += deltaY
        self.update_rect()

        for wall in walls:
            while wall.colliderect(self.get_rect()):
                if deltaY < 0:
                    self.y += 1
                elif deltaY > 0:
                    self.y -= 1
                self.update_rect()

    def update_rect(self):
        self.get_rect().update(self.x, self.y, self.width, self.height)

    def get_rect(self):
        return self.hull

    #Returns the angle you have to be aiming at to hit this 
    def get_angle_to_hit(self, x, y):
        
        deltaX = abs(self.x - x)
        deltaY = abs(self.y - y)
        
        # Top left
        if self.x < x and self.y < y:
            angle = math.atan(deltaX/deltaY)
            angle = hf.rToD(angle)
        elif self.x < x and self.y > y:
            angle = math.atan(deltaY/deltaX)
            angle = hf.rToD(angle)
            angle += 90
        elif self.x > x and self.y > y:
            angle = math.atan(deltaX/deltaY)
            angle = hf.rToD(angle)
            angle += 180
        else:
            angle = math.atan(deltaY/deltaX)
            angle = hf.rToD(angle)
            angle += 270
        
        return angle

    def get_turret_angle(self):
        self.turretAngle = self.turretAngle % 360
        return self.turretAngle

    def render(self):
        self.hull = pygame.draw.rect(self.screen, self.hullColor, [self.x, self.y, self.width, self.height])
        hf.rectRotated(self.screen, self.turretColor, (self.x + 7.5, self.y - 10, 5, 20), 0, 0, self.turretAngle, (0, 10), 8)

    def dummy_fire(self):
        temp = self.lastShotTime
        shell = self.fire(-1)
        self.lastShotTime = temp
        return shell

    def fire(self, delay = 1):
        if time.time() - self.lastShotTime > delay:
            shellVel = 4
            self.turretAngle = self.turretAngle % 360
            quadrant = self.turretAngle // 90
            angle = self.turretAngle
            if quadrant == 0:
                xVel = -1 * math.sin(hf.dToR(angle)) * shellVel
                yVel = -1 * math.cos(hf.dToR(angle)) * shellVel
                
            elif quadrant == 1:
                angle -= 90
                yVel = math.sin(hf.dToR(angle)) * shellVel
                xVel = -1 * math.cos(hf.dToR(angle)) * shellVel
            
            elif quadrant == 2:
                angle -= 180
                xVel = math.sin(hf.dToR(angle)) * shellVel
                yVel = math.cos(hf.dToR(angle)) * shellVel

            else:
                angle -= 270
                yVel = -1 * math.sin(hf.dToR(angle)) * shellVel
                xVel = math.cos(hf.dToR(angle)) * shellVel
            
            self.lastShotTime = time.time()
            return Shell(self.x + self.width / 2, self.y + self.height / 2, xVel, yVel, self, self.screen)
        
        return None