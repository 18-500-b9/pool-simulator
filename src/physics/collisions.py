from typing import Optional

from physics.coordinates import Coordinates
from physics.direction import Direction
from physics.utility import get_distance
from physics.vector import Vector


# TODO: Just make these take in PoolBall, lol
def check_ball_ball_collision(a_center: Coordinates, a_radius: float,
                              b_center: Coordinates, b_radius: float) -> bool:
    """
    Check if two balls have collided.

    :param a_center: center of ball A
    :param a_radius: radius of ball A
    :param b_center: center of ball B
    :param b_radius: radius of ball B
    :return: whether these two balls are in collision
    """
    d = get_distance(a_center, b_center)
    return d <= (a_radius + b_radius)


# TODO: Just make these take in PoolBall, lol
def resolve_ball_ball_collision(a_pos: Coordinates, a_vel: Vector, a_mass: float,
                                b_pos: Coordinates, b_vel: Vector, b_mass: float) -> (Vector, Vector):
    """
    Returns new velocity vectors after a ball-ball collision.

    :param a_pos: center of ball A at time of impact
    :param a_vel:  velocity of ball A
    :param a_mass: mass of ball A
    :param b_pos: center of ball B at time of impact
    :param b_vel:  velocity of ball B
    :param b_mass: mass of ball B
    :return: (new velocity of ball A, new velocity of ball B)
    """

    # Taken from https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects

    a_vel_new = a_vel - (2 * b_mass) / (a_mass + b_mass) * ((a_vel - b_vel).dot_product(a_pos - b_pos)) / get_distance(
        a_pos - b_pos) ** 2 * (a_pos - b_pos)
    b_vel_new = b_vel - (2 * a_mass) / (a_mass + b_mass) * ((b_vel - a_vel).dot_product(b_pos - a_pos)) / get_distance(
        b_pos - a_pos) ** 2 * (b_pos - a_pos)

    return a_vel_new, b_vel_new


# TODO: Just make these take in PoolBall, lol
def check_ball_wall_collision(ball_center: Coordinates, ball_radius: float,
                              north: float, east: float, south: float, west: float) -> Optional[Direction]:
    """
    Check if a ball has collided with a wall.

    :param ball_center: center of ball
    :param ball_radius: radius of ball
    :param north: north wall boundary
    :param east: east wall boundary
    :param south: south wall boundary
    :param west: west wall boundary
    :return: the wall this ball has collided with OR None
    """

    if ball_center.y + ball_radius >= north:
        return Direction.NORTH
    elif ball_center.x + ball_radius >= east:
        return Direction.EAST
    elif ball_center.y - ball_radius <= south:
        return Direction.SOUTH
    elif ball_center.x - ball_radius <= west:
        return Direction.WEST
    else:
        return None


# TODO: Just make these take in PoolBall, lol
def resolve_ball_wall_collision(ball_vel: Vector, wall: Direction):
    """
    Returns the new velocity for this ball that has collided with a wall.
    *Assumes wall is in one of 4 directions: N, E, S, or W*

    :param ball_vel: entry ball velocity
    :param wall: which wall (N, E, S, W)
    :return: exit ball velocity
    """

    if wall == Direction.NORTH or wall == Direction.SOUTH:
        return Vector(ball_vel.x, -ball_vel.y)  # Reverse y-direction
    else:  # EAST or WEST
        return Vector(-ball_vel.x, ball_vel.y)  # Reverse x-direction
