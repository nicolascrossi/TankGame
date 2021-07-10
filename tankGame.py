import pygame

from tank import Tank
from wall import Wall

import helperFunctions as hf
from ai import AI

from pygame.constants import K_s, K_w, K_a, K_d, K_SPACE

# Define constants
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

S_HEIGHT = 900
S_WIDTH = 1000

pygame.init() # Start pygame

screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT)) # Create the screen

screenRect = pygame.Rect(0, 0, S_WIDTH, S_HEIGHT) # Create the rect used to check if a shell is on screen

pygame.display.set_caption('Tank Game') 

clock = pygame.time.Clock()

# Create the player tank
tank = Tank(screen)
tank.hull_color = BLUE
tank.turret_color = RED
tank.set_x(100)
tank.set_y(100)
tank.update_rect()

# Create the AI tank
tank2 = Tank(screen)
tank2.hull_color = GREEN
tank2.turret_color = RED
tank2.set_x(S_WIDTH - 100)
tank2.set_y(S_HEIGHT - 100)
tank.update_rect()

#aiInfo = AIInfo(tank2, S_WIDTH, S_HEIGHT) # Stores values for the AI

blueShells = [] # Player shells
greenShells = [] # AI shells

walls = [] # All the walls

ai = AI(tank2, tank, blueShells, S_WIDTH, S_HEIGHT) # Represents the AI

# Create the border walls
wall_width = 20
walls.append(Wall(0, 0, wall_width, S_HEIGHT - wall_width, screen))
walls.append(Wall(0, S_HEIGHT - wall_width, S_WIDTH - wall_width, wall_width, screen))
walls.append(Wall(S_WIDTH - wall_width, wall_width, wall_width, S_HEIGHT - wall_width, screen))
walls.append(Wall(wall_width, 0, S_WIDTH - wall_width, wall_width, screen))

done = False #we're not done displaying
paused = False # Whether the rendering is paused

while not done:
    for event in pygame.event.get(): #check the events list
        if event.type == pygame.QUIT: #if the user clicks the X
            done = True #now we're done displaying
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                tank.change_vels(0, -tank.get_speed())

            if event.key == K_s:
                tank.change_vels(0, tank.get_speed())

            if event.key == K_a:
                tank.change_vels(-tank.get_speed(), 0)

            if event.key == K_d:
                tank.change_vels(tank.get_speed(), 0)
            
            if event.key == K_SPACE:
                shell = tank.fire()
                if shell:
                    blueShells.append(shell)
        
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                tank.change_vels(0, tank.get_speed())
            
            if event.key == K_s:
                tank.change_vels(0, -tank.get_speed())
            
            if event.key == K_a:
                tank.change_vels(tank.get_speed(), 0)
            
            if event.key == K_d:
                tank.change_vels(-tank.get_speed(), 0)

        if event.type == pygame.MOUSEMOTION:
            tank.set_turret_angle(hf.get_angle_to_hit(event.pos[0], event.pos[1], tank.get_x(), tank.get_y()))
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                shell = tank.fire()
                if shell:
                    blueShells.append(shell)
            if event.button == 3:
                tank.autofire = not tank.autofire
    
    if not paused:

        screen.fill(BLACK)

        # Check if autofire is on, try to shoot if so
        if tank.autofire:
            shell = tank.fire()
            if shell:
                blueShells.append(shell)

        # Check if blue's bullets have hit anything
        idx = 0
        while idx < len(blueShells):
            shell = blueShells[idx]
            shell.move()
            tankHit = shell.check_hit([tank, tank2])
            if tankHit:
                blueShells.pop(idx)
                print( "Green was hit! Game over!")
                paused = True
            elif not screenRect.contains(shell):
                blueShells.pop(idx)
            else:
                idx += 1
            shell.render()

        # Check if green's bullets have hit anything
        idx = 0
        while idx < len(greenShells):
            shell = greenShells[idx]
            shell.move()
            tankHit = shell.check_hit([tank, tank2])
            if tankHit:
                greenShells.pop(idx)
                print( "Blue was hit! Game over!")
                paused = True
            elif not screenRect.contains(shell):
                greenShells.pop(idx)
            else:
                idx += 1
            shell.render()

        # Check if any shells are colliding with walls and render the wall
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

        # Move and render the tank
        tank.move(walls)
        tank.render()

        # Get the AIMove object representing the AI's actions
        ai_move = ai.get_ai_actions()
        deltas = ai_move.get_deltas()
        tank2.set_vels(deltas[0], deltas[1])
        tank2.move(walls)
        if not ai_move.get_turret_angle() is None:
            tank2.set_turret_angle(ai_move.get_turret_angle())
        else:
            tank2.turn_turret(deltas[2])
        if ai_move.get_attempt_to_fire():
            shell = tank2.fire()
            if shell:
                greenShells.append(shell)

        tank2.render()

        pygame.display.update()

    clock.tick(60)

pygame.quit()