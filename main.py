import pygame
import time
import math
import random

from pygame.constants import K_s, K_w, K_a, K_d, K_SPACE

#define constants
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

S_HEIGHT = 1000
S_WIDTH = 1000

pygame.init() #start pygame

screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))

pygame.display.set_caption('Pygame Template')

clock = pygame.time.Clock()


class Tank:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.vel = 0
        self.turretAngle = 0
        self.lastShotTime = time.time()
        self.hullColor = BLUE
        self.turretColor = RED
        self.width = 20
        self.height = 20

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
        # print("")
        # print(self.x, self.y)
        # print(deltaX, deltaY)
        # print("")
        
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

        # if deltaX != 0 or deltaY != 0:
        #     self.x += deltaX

        #     self.y += deltaY
        #     self.update_rect()

        #     for wall in walls:
        #         while wall.colliderect(self.get_rect()):
            
        #             if deltaX < 0:
        #                 self.x += 1
        #             elif deltaX > 0:
        #                 self.x -= 1
        #             if deltaY < 0:
        #                 self.y += 1
        #             elif deltaY > 0:
        #                 self.y -= 1
        #             self.update_rect()

            # for wall in walls:
            #     while wall.colliderect(self.get_rect()):
            #         if deltaY < 0:
            #             self.y += 1
            #         elif deltaY > 0:
            #             self.y -= 1
            #         self.update_rect()
            
        for wall in walls:
            if wall.colliderect(self.get_rect()):
                print("Still colliding")

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
            angle = rToD(angle)
        elif self.x < x and self.y > y:
            angle = math.atan(deltaY/deltaX)
            angle = rToD(angle)
            angle += 90
        elif self.x > x and self.y > y:
            angle = math.atan(deltaX/deltaY)
            angle = rToD(angle)
            angle += 180
        else:
            angle = math.atan(deltaY/deltaX)
            angle = rToD(angle)
            angle += 270
        
        return angle

    def get_turret_angle(self):
        self.turretAngle = self.turretAngle % 360
        return self.turretAngle

    def render(self):
        self.hull = pygame.draw.rect(screen, self.hullColor, [self.x, self.y, self.width, self.height])
        rectRotated(screen, self.turretColor, (self.x + 7.5, self.y - 10, 5, 20), 0, 0, self.turretAngle, (0, 10), 8)

    def fire(self):
        if time.time() - self.lastShotTime > 1:
            shellVel = 4
            self.turretAngle = self.turretAngle % 360
            quadrant = self.turretAngle // 90
            angle = self.turretAngle
            if quadrant == 0:
                xVel = -1 * math.sin(dToR(angle)) * shellVel
                yVel = -1 * math.cos(dToR(angle)) * shellVel
                
            elif quadrant == 1:
                angle -= 90
                yVel = math.sin(dToR(angle)) * shellVel
                xVel = -1 * math.cos(dToR(angle)) * shellVel
            
            elif quadrant == 2:
                angle -= 180
                xVel = math.sin(dToR(angle)) * shellVel
                yVel = math.cos(dToR(angle)) * shellVel

            else:
                angle -= 270
                yVel = -1 * math.sin(dToR(angle)) * shellVel
                xVel = math.cos(dToR(angle)) * shellVel
            
            self.lastShotTime = time.time()
            return Shell(self.x + self.width / 2, self.y + self.height / 2, xVel, yVel, self)
        return None

class Shell:

    def __init__(self, x, y, xVel, yVel, friendly):
        self.friendly = friendly
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel

        self.rect = pygame.Rect(self.x, self.y, 2, 2)

    def move(self):
        self.x += self.xVel
        self.y += self.yVel

    def render(self):
        self.rect = pygame.draw.rect(screen, WHITE, [self.x, self.y, 2, 2])

    def check_hit(self, tanks):
        for tank in tanks:
            if not tank is self.friendly:
                if tank.get_rect().colliderect(self.rect):
                    return tank
        return None

    def get_rect(self):
        return self.rect

    def get_line(self):
        return Line(self.x, self.y, self.xVel, self.yVel)

class Line:

    def __init__(self, x, y, rise, run):
        self.x1 = x
        self.y1 = y
        self.x2 = x + run
        self.y2 = y + rise
    
    def dist(self, x, y):
        num = abs((self.x2 - self.x1)*(self.y1 - y) - (self.x1 - x)*(self.y2 - self.y1))
        denom = math.sqrt( ((self.x2 - self.x1) ** 2) + ((self.y2 - self.y1) ** 2) )
        return num / denom

def dToR(degrees):
    return (degrees / 180) * math.pi

def rToD(radians):
    return (radians / math.pi) * 180

def rectRotated( surface, color, pos, fill, border_radius, rotation_angle, rotation_offset_center = (0,0), nAntialiasingRatio = 1 ):
    """
    - rotation_angle: in degree
    - rotation_offset_center: moving the center of the rotation: (-100,0) will turn the rectangle around a point 100 above center of the rectangle,
                                            if (0,0) the rotation is at the center of the rectangle
    - nAntialiasingRatio: set 1 for no antialising, 2/4/8 for better aliasing
    """
    nRenderRatio = nAntialiasingRatio
    
    sw = pos[2]+abs(rotation_offset_center[0])*2
    sh = pos[3]+abs(rotation_offset_center[1])*2

    surfcenterx = sw//2
    surfcentery = sh//2
    s = pygame.Surface( (sw*nRenderRatio,sh*nRenderRatio) )
    s = s.convert_alpha()
    s.fill((0,0,0,0))
    
    rw2=pos[2]//2 # halfwidth of rectangle
    rh2=pos[3]//2

    pygame.draw.rect( s, color, ((surfcenterx-rw2-rotation_offset_center[0])*nRenderRatio,(surfcentery-rh2-rotation_offset_center[1])*nRenderRatio,pos[2]*nRenderRatio,pos[3]*nRenderRatio), fill*nRenderRatio, border_radius=border_radius*nRenderRatio )
    s = pygame.transform.rotate( s, rotation_angle )        
    if nRenderRatio != 1: s = pygame.transform.smoothscale(s,(s.get_width()//nRenderRatio,s.get_height()//nRenderRatio))
    incfromrotw = (s.get_width()-sw)//2
    incfromroth = (s.get_height()-sh)//2
    surface.blit( s, (pos[0]-surfcenterx+rotation_offset_center[0]+rw2-incfromrotw,pos[1]-surfcentery+rotation_offset_center[1]+rh2-incfromroth) )
        
class Wall:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WHITE

    def get_rect(self):
        return self.rect

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

    def render(self):
        pygame.draw.rect(screen, self.color, self.rect)

def get_angle_to_hit(tX, tY, sX, sY):
    deltaX = abs(tX - sX)
    deltaY = abs(tY - sY)
    
    if deltaX == 0 or deltaY == 0:
        return 0

    if tX < sX and tY < sY:
        angle = math.atan(deltaX/deltaY)
        angle = rToD(angle)
    elif tX < sX and tY > sY:
        angle = math.atan(deltaY/deltaX)
        angle = rToD(angle)
        angle += 90
    elif tX > sX and tY > sY:
        angle = math.atan(deltaX/deltaY)
        angle = rToD(angle)
        angle += 180
    else:
        angle = math.atan(deltaY/deltaX)
        angle = rToD(angle)
        angle += 270
    
    return angle

def get_vel_components(velocity, angle):
    angle = angle % 360
    quadrant = angle // 90
    if quadrant == 0:
        xVel = -1 * math.sin(dToR(angle)) * velocity
        yVel = -1 * math.cos(dToR(angle)) * velocity
        
    elif quadrant == 1:
        angle -= 90
        yVel = math.sin(dToR(angle)) * velocity
        xVel = -1 * math.cos(dToR(angle)) * velocity
    
    elif quadrant == 2:
        angle -= 180
        xVel = math.sin(dToR(angle)) * velocity
        yVel = math.cos(dToR(angle)) * velocity

    else:
        angle -= 270
        yVel = -1 * math.sin(dToR(angle)) * velocity
        xVel = math.cos(dToR(angle)) * velocity

    return (xVel, yVel)

done = False #we're not done displaying

xVel = 0
yVel = 0
turretAngleVel = 0

tank = Tank()
tank.x = 100
tank.y = 100
tank.update_rect()

tank2 = Tank()
tank2.hullColor = GREEN
tank2.x = S_WIDTH - 100
tank2.y = S_HEIGHT - 100
tank.update_rect()

tankSpeed = 3
turretSpeed = 2

blueShells = []
greenShells = []

wall_width = 20
walls = []
walls.append(Wall(0, 0, wall_width, S_HEIGHT - wall_width))
walls.append(Wall(0, S_HEIGHT - wall_width, S_WIDTH - wall_width, wall_width))
walls.append(Wall(S_WIDTH - wall_width, wall_width, wall_width, S_HEIGHT - wall_width))
walls.append(Wall(wall_width, 0, S_WIDTH - wall_width, wall_width))

screenRect = pygame.Rect(0, 0, S_WIDTH, S_HEIGHT)

class AIMove:

    def __init__(self):
        self.deltaX = 0
        self.deltaY = 0
        self.deltaTurretAngle = 0
        self.turret_angle = None
        self.attemptToFire = False
    
    def change_x_by(self, amt):
        self.deltaX = amt
    
    def change_y_by(self, amt):
        self.deltaY = amt

    def change_turret_angle(self, amt):
        self.deltaTurretAngle = amt
    
    def set_turret_angle(self, val):
        self.turret_angle = val
    
    def attempt_to_fire(self, val):
        self.attemptToFire = val

'''
Create an instance of AIMove and make the desired changes
EX:

aiMove = AIMove()
aiMove.change_x_by(10)
aiMove.change_y_by(-5)
aiMove.change_turret_angle(34)
aiMove.attempt_to_fire(true)
return aiMove

#USEFUL FUNCTIONS
AIMove:
aiMove.change_x_by(amt)
aiMove.change_y_by(amt)
aiMove.change_turret_angle(amt)
aiMove.attempt_to_fire(True/False)
aiMove.set_turret_angle(val)
#Note set_turret_angle will override change_turret_angle

Tank
tank.get_x()
tank.get_y()
# This gives the angle that a tank at x, y needs to fire at to hit tank
tank.get_angle_to_hit(x, y)

Shell
# Gives a line which represents where the shell will travel
shell.get_line()

Line
#Tells you how close x, y is to the line
line.dist(x, y)

Variables
#How fast the tanks move
tankSpeed
#How fast the turrets turn
turretSpeed
#A list of shells fired by the green tank
blueShells
#A list of shells fired by the blue tank
greenShells

'''

class Marker:
    def __init__(self, x, y):
        self.color = RED
        self.x = x
        self.y = y
        self.width = 5
        self.height = 5
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def render(self):
        pygame.draw.rect(screen, self.color, self.rect)

markers = []

class AIInfo:
    def __init__(self):
        self.aiDest = (random.randint(50, S_WIDTH - 50), random.randint(50, S_HEIGHT - 50))
        self.travelTime = time.time()
        self.aiVels = get_vel_components(tankSpeed, get_angle_to_hit(self.aiDest[0], self.aiDest[1], S_WIDTH - 100, S_HEIGHT - 100))

aiInfo = AIInfo()

def get_ai_actions(tank, enemy_tank, enemy_shells):
    ai = AIMove()

    lines = [shell.get_line() for shell in enemy_shells]
    
    changed = False

    for line in lines:
        cur_dist = line.dist(tank.get_x(), tank.get_y())
        newDest = [tank.get_x(), tank.get_y()]
        maxDist = cur_dist
        if cur_dist < 30:
            for deltaX in range(-4, 5, 4):
                for deltaY in range(-4, 5, 4):
                    if deltaX != 0 or deltaY != 0:
                        newDist = line.dist(tank.get_x() + deltaX, tank.get_y() + deltaY)
                        if newDist > maxDist:
                            newDest = [tank.get_x() + deltaX, tank.get_y() + deltaY]
                            maxDist = newDist
        if maxDist != cur_dist:
            changed = True
            markers.append(Marker(newDest[0], newDest[1]))
            aiInfo.aiDest = tuple(newDest)
            aiInfo.travelTime = time.time()
            aiInfo.aiVels = get_vel_components(tankSpeed, get_angle_to_hit(aiInfo.aiDest[0], aiInfo.aiDest[1], tank.get_x(), tank.get_y()))


    if not changed and tank.get_rect().collidepoint(aiInfo.aiDest) or time.time() - aiInfo.travelTime > 3:
        aiInfo.aiDest = (random.randint(50, S_WIDTH - 50), random.randint(50, S_HEIGHT - 50))
        aiInfo.travelTime = time.time()
        aiInfo.aiVels = get_vel_components(tankSpeed, get_angle_to_hit(aiInfo.aiDest[0], aiInfo.aiDest[1], tank.get_x(), tank.get_y()))
    else:
        ai.change_x_by(aiInfo.aiVels[0])
        ai.change_y_by(aiInfo.aiVels[1])

    angle = get_angle_to_hit(enemy_tank.get_x(), enemy_tank.get_y(), tank.get_x(), tank.get_y())
    ai.set_turret_angle(angle)
    ai.attempt_to_fire(True)

    return ai

while not done:
    for event in pygame.event.get(): #check the events list
        if event.type == pygame.QUIT: #if the user clicks the X
            done = True #now we're done displaying
        if event.type == pygame.KEYDOWN:

            if event.key == K_w:
                yVel -= tankSpeed
            if event.key == K_s:
                yVel += tankSpeed
            if event.key == K_a:
                xVel -= tankSpeed
            if event.key == K_d:
                xVel += tankSpeed
            if event.key == K_SPACE:
                shell = tank.fire()
                if not shell is None:
                    blueShells.append(shell)
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                yVel += tankSpeed
            if event.key == K_s:
                yVel -= tankSpeed
            if event.key == K_a:
                xVel += tankSpeed
            if event.key == K_d:
                xVel -= tankSpeed

        if event.type == pygame.MOUSEMOTION:
            tank.set_turret_angle(get_angle_to_hit(event.pos[0], event.pos[1], tank.get_x(), tank.get_y()))
    
    screen.fill(BLACK)

    for marker in markers:
        marker.render()

    idx = 0
    while idx < len(blueShells):
        shell = blueShells[idx]
        shell.move()
        tankHit = shell.check_hit([tank, tank2])
        if not tankHit is None:
            print( "Green was hit! Game over!")
            done = True
        if not screenRect.contains(shell):
            blueShells.pop(idx)
        else:
            idx += 1
        shell.render()

    idx = 0
    while idx < len(greenShells):
        shell = greenShells[idx]
        shell.move()
        tankHit = shell.check_hit([tank, tank2])
        if not tankHit is None:
            print( "Blue was hit! Game over!")
            done = True
        if not screenRect.contains(shell):
            greenShells.pop(idx)
        else:
            idx += 1
        shell.render()

    for wall in walls:
        idx = 0
        while idx < len(blueShells):
            shell = blueShells[idx]
            if wall.colliderect(shell.get_rect()):
                blueShells.pop(idx)
            else:
                idx += 1

        idx = 0
        while idx < len(greenShells):
            shell = greenShells[idx]
            if wall.colliderect(shell.get_rect()):
                greenShells.pop(idx)
            else:
                idx += 1

        wall.render()

    tank.move(xVel, yVel, walls)
    tank.turn_turret(turretAngleVel)
    tank.render()

    aiMove = get_ai_actions(tank2, tank, blueShells)
    tank2.move(aiMove.deltaX, aiMove.deltaY, walls)
    if not aiMove.turret_angle is None:
        tank2.set_turret_angle(aiMove.turret_angle)
    else:
        tank2.turn_turret(aiMove.deltaTurretAngle)
    if aiMove.attemptToFire:
        shell = tank2.fire()
        if not shell is None:
            greenShells.append(shell)

    tank2.render()

    pygame.display.update()


    clock.tick(60)

pygame.quit()