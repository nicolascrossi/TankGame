class AIMove:

    def __init__(self):
        self.delta_x = 0
        self.delta_y = 0
        self.delta_turret_angle = 0
        self.turret_angle = None
        self.attempt_to_fire = False
    
    def get_deltas(self):
        return (self.delta_x, self.delta_y, self.delta_turret_angle)
    
    def get_turret_angle(self):
        return self.turret_angle
    
    def get_attempt_to_fire(self):
        return self.attempt_to_fire

    def change_x_by(self, amt):
        self.delta_x = amt
    
    def change_y_by(self, amt):
        self.delta_y = amt

    def change_turret_angle(self, amt):
        self.delta_turret_angle = amt
    
    def set_turret_angle(self, val):
        self.turret_angle = val
    
    def set_attempt_to_fire(self, val):
        self.attempt_to_fire = val