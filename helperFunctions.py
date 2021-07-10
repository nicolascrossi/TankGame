import pygame
import math

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

def get_dist(pos0, pos1):
    return get_dist_indiv(pos0[0], pos0[1], pos1[0], pos1[1])

def get_dist_indiv(x0, y0, x1, y1):
    return math.sqrt( (x0 - x1)**2 + (y0 - y1)**2 )