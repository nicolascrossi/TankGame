import pygame
import time
import math

from pygame.constants import K_s, K_w, K_a, K_d, K_r, K_t, K_SPACE

#define constants
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

S_HEIGHT = 400
S_WIDTH = 400

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

    def move(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY

    def get_rect(self):
        return self.rect

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
        self.rect = pygame.draw.rect(screen, self.hullColor, [self.x, self.y, self.width, self.height])
        rectRotated(screen, self.turretColor, (self.x + 7.5, self.y - 10, 5, 20), 0, 0, self.turretAngle, (0, 10), 1)

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

    def get_line(self):
        return Line(self.x, self.y, self.xVel, self.yVel)

class Line:

    def __init__(self, x, y, rise, run):
        self.x = x
        self.y = y
        self.x2 = x + run
        self.y2 = y + rise
    
    def dist(self, x, y):
        num = (abs((self.x2 - self.x)(self.y - y) - (self.x - x)(self.y2 - self.y)))
        denom = (math.sqrt(((self.x2 - self.x) ** 2) + ((self.y2 - self.y) ** 2)))
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
        

done = False #we're not done displaying

xVel = 0
yVel = 0
turretAngleVel = 0

tank = Tank()
tank.x = 100
tank.y = 100

tank2 = Tank()
tank2.hullColor = GREEN
tank2.x = 300
tank2.y = 300

tankSpeed = 3
turretSpeed = 2

blueShells = []
greenShells = []

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
def get_ai_actions(tank, enemy_tank, enemy_shells):
    ai = AIMove()
    #PUT EVERYTHING IN HERE THAT YOU WANT TO HAPPEN
    # if tank.get_x() < 380:
    #     ai.change_x_by(10)
    # if tank.get_y() > 10:
    #     ai.change_y_by(-5)
    # ai.change_turret_angle(3)
    # ai.attempt_to_fire(True)


    return ai

while not done:
    for event in pygame.event.get(): #check the events list
        if event.type == pygame.QUIT: #if the user clicks the X
            done = True #now we're done displaying
        if event.type == pygame.KEYDOWN:
            if event.key == K_t:
                turretAngleVel -= turretSpeed
            elif event.key == K_r:
                turretAngleVel += turretSpeed
            elif event.key == K_w:
                yVel -= tankSpeed
            elif event.key == K_s:
                yVel += tankSpeed
            elif event.key == K_a:
                xVel -= tankSpeed
            elif event.key == K_d:
                xVel += tankSpeed
            elif event.key == K_SPACE:
                shell = tank.fire()
                if not shell is None:
                    blueShells.append(shell)
        if event.type == pygame.KEYUP:
            if event.key == K_w or event.key == K_s:
                yVel = 0
            elif event.key == K_a or event.key == K_d:
                xVel = 0
            elif event.key == K_r or event.key == K_t:
                turretAngleVel = 0
    
    screen.fill(BLACK)

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


    tank.move(xVel, yVel)
    tank.turn_turret(turretAngleVel)
    tank.render()

    aiMove = get_ai_actions(tank2, tank, blueShells)
    tank2.move(aiMove.deltaX, aiMove.deltaY)
    if not aiMove.turret_angle is None:
        tank2.set_turret_angle(aiMove.turret_angle)
    else:
        tank2.turn_turret(aiMove.deltaTurretAngle)
    if aiMove.attemptToFire:
        shell = tank2.fire()
        if not shell is None:
            greenShells.append(shell)

    tank2.render()
    # pygame.draw.rect(screen, BLUE, [100, 100, 20, 35])
    # rectRotated(screen, RED, (107.5, 95, 5, 30), 0, 0, rotation, (0, 15), 1)

    pygame.display.update()


    clock.tick(60)

pygame.quit()