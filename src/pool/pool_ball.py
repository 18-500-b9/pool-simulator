import numpy as np

from physics.collisions import *
from pool.ball_type import BallType


class PoolBall():
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

    @staticmethod
    def get_theta(ball_a, ball_b):
        """
        Calculate the angle, relative to the x-axis, between 2 balls.
        """

        # Set ball_a to be the origin, find ball_b's relative position
        x = ball_b.x - ball_a.x
        y = ball_b.y - ball_a.y

        return np.arctan(y / x)

    @staticmethod
    def distance(a: Coordinates, b: Coordinates):
        """
        Return the distance between these two points.
        """

        return np.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

    def time_step(self):
        """
        Update position after 1 second.
        """

        # Distance = Velocity * Time
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        # if self.ball_type == BallType.CUE:
        # print(self)

    def __str__(self):
        return "PoolBall {} at ({},{})".format(self.ball_type.name, self.pos.x, self.pos.y)
