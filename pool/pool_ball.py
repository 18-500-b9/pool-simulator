from helper import Vector


class PoolBall():
    '''
    Represents a single pool ball.
    '''

    MASS = 0.17  # kg
    DIAMETER = 0.05715  # m

    def __init__(self, name: str, radius: float,
                 pos: Vector, vel=Vector(0, 0)):

        self.name = name
        self.radius = radius

        self.pos = pos
        self.vel = vel

    def apply_force(self, force: Vector):
        '''
        Apply x and y components of force to this ball.
        '''

        # Acceleration = Force / Mass
        acc_x = force.x / self.MASS
        acc_y = force.y / self.MASS

        self.vel.x += acc_x
        self.vel.y += acc_y

    def time_step(self):
        '''
        Update position after 1 second.
        '''

        # Distance = Velocity * Time
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

    def __str__(self):
        return "PoolBall {} at ({},{})".format(self.name,
                                               self.x_pos, self.y_pos)
