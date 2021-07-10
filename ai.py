import time

import helperFunctions as hf
from aiMove import AIMove

def check_aim(tank, enemy_tank, start_angle, angle_mod):
    enemy_pos = [enemy_tank.get_x(), enemy_tank.get_y()]

    angle = start_angle
    angle += angle_mod
    tank.set_turret_angle(angle)

    shell = tank.dummy_fire()
    shell_pos = [shell.x, shell.y]

    prev_dist = hf.get_dist(shell_pos, enemy_pos)
    
    shell_pos[0] += shell.xVel
    shell_pos[1] += shell.yVel
    enemy_pos[0] += enemy_tank.xVel
    enemy_pos[1] += enemy_tank.yVel
    cur_dist = hf.get_dist(shell_pos, enemy_pos)

    while cur_dist < prev_dist:
        prev_dist = cur_dist
        shell_pos[0] += shell.xVel
        shell_pos[1] += shell.yVel
        enemy_pos[0] += enemy_tank.xVel
        enemy_pos[1] += enemy_tank.yVel
        cur_dist = hf.get_dist(shell_pos, enemy_pos)

    return prev_dist

def aim(tank, enemy_tank):

    start_angle = hf.get_angle_to_hit(enemy_tank.get_x(), enemy_tank.get_y(), tank.get_x(), tank.get_y())

    min_dist = check_aim(tank, enemy_tank, start_angle, 0)


    if check_aim(tank, enemy_tank, start_angle, 1) < min_dist:
        # Do increasing
        angle_mod = 2
        prev_dist = check_aim(tank, enemy_tank, start_angle, 1)
        new_dist = check_aim(tank, enemy_tank, start_angle, angle_mod)
        while prev_dist > new_dist:
            prev_dist = new_dist
            angle_mod += 0.5
            new_dist = check_aim(tank, enemy_tank, start_angle, angle_mod)
        return start_angle + angle_mod - 1
    elif check_aim(tank, enemy_tank, start_angle, -1) < min_dist:
        # Do decreasing
        angle_mod = -2
        prev_dist = check_aim(tank, enemy_tank, start_angle, -1)
        new_dist = check_aim(tank, enemy_tank, start_angle, angle_mod)
        while prev_dist > new_dist:
            prev_dist = new_dist
            angle_mod -= 0.5
            new_dist = check_aim(tank, enemy_tank, start_angle, angle_mod)
        return start_angle + angle_mod + 1
    else:
        return start_angle

def get_ai_actions(tank, enemy_tank, enemy_shells, aiInfo):
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
            # markers.append(Marker(newDest[0], newDest[1]))
            aiInfo.aiDest = tuple(newDest)
            aiInfo.travelTime = time.time()
            aiInfo.aiVels = hf.get_vel_components(tank.tankSpeed, hf.get_angle_to_hit(aiInfo.aiDest[0], aiInfo.aiDest[1], tank.get_x(), tank.get_y()))


    if not changed and tank.get_rect().collidepoint(aiInfo.aiDest) or time.time() - aiInfo.travelTime > 3:
        aiInfo.new_dest()
        aiInfo.reset_travel_time()
    else:
        ai.change_x_by(aiInfo.aiVels[0])
        ai.change_y_by(aiInfo.aiVels[1])

    ai.set_turret_angle(aim(tank, enemy_tank))
    ai.attempt_to_fire(True)

    return ai