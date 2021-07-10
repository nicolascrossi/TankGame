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