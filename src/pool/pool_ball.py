from physics.coordinates import Coordinates
from physics.vector import Vector
from pool.ball_type import BallType


class PoolBall:
    """
    Represents a single pool ball.
    """

    # MASS = 0.17  # kg
    # DIAMETER = 0.05715  # m

    def __init__(self,
                 ball_type: BallType,
                 pos: Coordinates,
                 mass: float,
                 radius: float,
                 vel=None):
        self.ball_type = ball_type
        self.pos = pos
        self.mass = mass
        self.radius = radius
        if vel is None:
            self.vel = Vector(0, 0)

    def apply_force(self, force: Vector):
        """
        Apply x and y components of force to this ball.
        """

        # Acceleration = Force / Mass
        acc_x = force.x / self.mass
        acc_y = force.y / self.mass

        self.vel.x += acc_x
        self.vel.y += acc_y

    def time_step(self):
        """
        Update position after 1 second.
        """

        # Distance = Velocity * Time
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        # TODO Velocity slowdown
        self.vel.x *= 0.99
        self.vel.y *= 0.99

    def __str__(self):
        return "PoolBall {} at ({},{})".format(self.ball_type.name, self.pos.x, self.pos.y)
