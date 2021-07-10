import time
import random

import helperFunctions as hf
from aiMove import AIMove


class AI:

    def __init__(self, ai_tank, enemy_tank, enemy_shells, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.ai_tank = ai_tank
        self.enemy_tank = enemy_tank
        self.enemy_shells = enemy_shells

        self.ai_dest = [0, 0]
        self.ai_vels = [0.0, 0.0]
        self.travel_time = 0.0
        self.new_dest()
        self.reset_travel_time()

    def new_dest(self):
        self.ai_dest = (random.randint(50, self.screen_width - 50),
                        random.randint(50, self.screen_height - 50))
        self.ai_vels = hf.get_vel_components(self.ai_tank.get_speed(), hf.get_angle_to_hit(
            self.ai_dest[0], self.ai_dest[1], self.screen_width - 100, self.screen_height - 100))

    def reset_travel_time(self):
        self.travel_time = time.time()

    def get_screen_dim(self):
        return (self.screen_width, self.screen_width)

    def within_bounds(self, pos):
        x, y = pos
        return not (x < 0 or x > self.screen_width or y < 0 or y > self.screen_height)

    def check_aim(self, start_angle, angle_mod):
        enemy_pos = [self.enemy_tank.get_x(), self.enemy_tank.get_y()]

        angle = start_angle
        angle += angle_mod
        self.ai_tank.set_turret_angle(angle)

        shell = self.ai_tank.dummy_fire()
        shell_pos = list(shell.get_pos())

        prev_dist = hf.get_dist(shell_pos, enemy_pos)

        shell_pos[0] += shell.get_vels()[0]
        shell_pos[1] += shell.get_vels()[1]
        enemy_pos[0] += self.enemy_tank.get_vels()[0]
        enemy_pos[1] += self.enemy_tank.get_vels()[1]
        cur_dist = hf.get_dist(shell_pos, enemy_pos)

        while cur_dist < prev_dist and self.within_bounds(enemy_pos) and self.within_bounds(shell_pos):
            prev_dist = cur_dist
            shell_pos[0] += shell.get_vels()[0]
            shell_pos[1] += shell.get_vels()[1]
            enemy_pos[0] += self.enemy_tank.get_vels()[0]
            enemy_pos[1] += self.enemy_tank.get_vels()[1]
            cur_dist = hf.get_dist(shell_pos, enemy_pos)

        return prev_dist

    def aim(self, increment, fine_increment):

        start_angle = hf.get_angle_to_hit(self.enemy_tank.get_x(
        ), self.enemy_tank.get_y(), self.ai_tank.get_x(), self.ai_tank.get_y())

        min_dist = self.check_aim(start_angle, 0)

        if self.check_aim(start_angle, increment) < min_dist:
            # Do increasing

            # Gross adjustment
            angle_mod = increment * 2
            prev_dist = self.check_aim(start_angle, increment)
            new_dist = self.check_aim(start_angle, angle_mod)
            while prev_dist > new_dist:
                prev_dist = new_dist
                angle_mod += increment
                new_dist = self.check_aim(start_angle, angle_mod)

            # Fine adjustment
            prev_dist = new_dist
            angle_mod -= fine_increment
            new_dist = self.check_aim(start_angle, angle_mod)
            while prev_dist > new_dist:
                prev_dist = new_dist
                angle_mod -= fine_increment
                new_dist = self.check_aim(start_angle, angle_mod)

            return start_angle + angle_mod + fine_increment
        elif self.check_aim(start_angle, -increment) < min_dist:
            # Do decreasing

            # Gross adjustment
            angle_mod = -increment * 2
            prev_dist = self.check_aim(start_angle, -increment)
            new_dist = self.check_aim(start_angle, angle_mod)
            while prev_dist > new_dist:
                prev_dist = new_dist
                angle_mod -= increment
                new_dist = self.check_aim(start_angle, angle_mod)

            # Fine adjustment
            prev_dist = new_dist
            angle_mod += fine_increment
            new_dist = self.check_aim(start_angle, angle_mod)
            while prev_dist > new_dist:
                prev_dist = new_dist
                angle_mod += fine_increment
                new_dist = self.check_aim(start_angle, angle_mod)

            return start_angle + angle_mod - fine_increment
        else:
            return start_angle

    def get_ai_actions(self):
        ai = AIMove()

        lines = [shell.get_line() for shell in self.enemy_shells]

        changed = False

        for line in lines:
            cur_dist = line.dist(self.ai_tank.get_x(), self.ai_tank.get_y())
            newDest = [self.ai_tank.get_x(), self.ai_tank.get_y()]
            maxDist = cur_dist
            if cur_dist < 30:
                for deltaX in range(-4, 5, 4):
                    for deltaY in range(-4, 5, 4):
                        if deltaX != 0 or deltaY != 0:
                            newDist = line.dist(self.ai_tank.get_x(
                            ) + deltaX, self.ai_tank.get_y() + deltaY)
                            if newDist > maxDist:
                                newDest = [self.ai_tank.get_x(
                                ) + deltaX, self.ai_tank.get_y() + deltaY]
                                maxDist = newDist
            if maxDist != cur_dist:
                changed = True
                # markers.append(Marker(newDest[0], newDest[1]))
                self.reset_travel_time()
                self.ai_dest = tuple(newDest)
                self.ai_vels = hf.get_vel_components(self.ai_tank.get_speed(), hf.get_angle_to_hit(
                    self.ai_dest[0], self.ai_dest[1], self.ai_tank.get_x(), self.ai_tank.get_y()))

        if not changed and self.ai_tank.get_rect().collidepoint(self.ai_dest) or time.time() - self.travel_time > 3:
            self.new_dest()
            self.reset_travel_time()
        else:
            ai.change_x_by(self.ai_vels[0])
            ai.change_y_by(self.ai_vels[1])

        # Swap which line is commented if the game lags. Currently predicting where to shoot is inefficient
        #ai.set_turret_angle(hf.get_angle_to_hit(enemy_tank.get_x(), enemy_tank.get_y(), tank.get_x(), tank.get_y()))
        ai.set_turret_angle(self.aim(2, 0.5))

        ai.set_attempt_to_fire(True)

        return ai
