import numpy as np

from physics.coordinates import Coordinates
from physics.vector import Vector


class PoolBall():
    """
    Represents a single pool ball.
    """

    # MASS = 0.17  # kg
    # DIAMETER = 0.05715  # m

    def __init__(self,
                 name: str,
                 pos: Coordinates,
                 mass: float,
                 radius: float,
                 vel=Vector(0, 0)):

        self.name = name
        self.pos = pos
        self.mass = mass
        self.radius = radius
        self.vel = vel

    def apply_force(self, force: Vector):
        """
        Apply x and y components of force to this ball.
        """

        # Acceleration = Force / Mass
        acc_x = force.x / self.mass
        acc_y = force.y / self.mass

        self.vel.x += acc_x
        self.vel.y += acc_y

    def get_momentum(self):
        """
        Returns this ball's current momentum as a Vector.
        """

        return Vector(self.mass*self.vel.x, self.mass*self.vel.y)

    @staticmethod
    def get_theta(ball_a, ball_b):
        """
        Calculate the angle, relative to the x-axis, between 2 balls.
        """

        # Set ball_a to be the origin, find ball_b's relative position
        x = ball_b.x - ball_a.x
        y = ball_b.y - ball_a.y

        return np.arctan(y/x)

    @staticmethod
    def distance(a: Coordinates, b: Coordinates):
        """
        Return the distance between these two points.
        """

        return np.sqrt((b.x-a.x)**2 + (b.y-a.y)**2)

    def check_collision_with(self, other):
        """
        Check if this ball is colliding with another ball.
        """

        # First get distance between the two balls
        distance = PoolBall.distance(self.pos, other.pos)

        is_colliding = distance <= (self.radius + other.radius)

        return is_colliding

    def collide_with(self, other):
        """
        Collide with other ball.
        TODO: Currently assuming elastic collision.
        """
        # Momentum (p)

    def time_step(self):
        """
        Update position after 1 second.
        """

        # Distance = Velocity * Time
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

    def __str__(self):
        return "PoolBall {} at ({},{})".format(self.name,
                                               self.x_pos, self.y_pos)
