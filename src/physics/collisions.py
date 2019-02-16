from typing import Optional

from physics.direction import Direction
from physics.utility import get_distance
from physics.vector import Vector
from pool.pool_ball import PoolBall


def check_ball_ball_collision(a: PoolBall, b: PoolBall) -> bool:
    """
    Check if two balls have collided.

    :param a: ball A
    :param b: ball B
    :return: whether these two balls are in collision
    """
    d = get_distance(a.pos, b.pos)
    is_colliding = d <= (a.radius + b.radius)

    from pool.ball_type import BallType
    if a.ball_type is BallType.THREE:
        print(a.most_recent_collision)
        print(b.most_recent_collision)

    if is_colliding and a.most_recent_collision is b and b.most_recent_collision is a:
        print("NOT COLLIDING AGAIN...")
        return False

    a.most_recent_collision = b
    b.most_recent_collision = a
    return is_colliding


def resolve_ball_ball_collision(a: PoolBall, b: PoolBall):
    """
    Sets new velocity vectors after a ball-ball collision.

    :param a: ball A
    :param b: ball B
    """

    # Taken from https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects

    a_vel_new = a.vel - (2 * b.mass) / (a.mass + b.mass) * ((a.vel - b.vel).dot_product(a.pos - b.pos)) / get_distance(
        a.pos - b.pos) ** 2 * (a.pos - b.pos)
    b_vel_new = b.vel - (2 * a.mass) / (a.mass + b.mass) * ((b.vel - a.vel).dot_product(b.pos - a.pos)) / get_distance(
        b.pos - a.pos) ** 2 * (b.pos - a.pos)

    a.vel, b.vel = a_vel_new, b_vel_new


def check_ball_wall_collision(ball: PoolBall,
                              north: float, east: float, south: float, west: float) -> Optional[Direction]:
    """
    Check if a ball has collided with a wall.

    :param ball: pool ball
    :param north: north wall boundary
    :param east: east wall boundary
    :param south: south wall boundary
    :param west: west wall boundary
    :return: the wall this ball has collided with OR None
    """

    if ball.pos.y + ball.radius >= north:
        return Direction.NORTH
    elif ball.pos.x + ball.radius >= east:
        return Direction.EAST
    elif ball.pos.y - ball.radius <= south:
        return Direction.SOUTH
    elif ball.pos.x - ball.radius <= west:
        return Direction.WEST
    else:
        return None


# TODO: Just make these take in PoolBall, lol
def resolve_ball_wall_collision(ball: PoolBall, wall: Direction):
    """
    Sets the new velocity for this ball after it has collided with a wall.
    *Assumes wall is in one of 4 directions: N, E, S, or W*

    :param ball: pool ball
    :param wall: which wall (N, E, S, W)
    """

    if wall == Direction.NORTH or wall == Direction.SOUTH:
        ball.vel = Vector(ball.vel.x, -ball.vel.y)  # Reverse y-direction
    else:  # EAST or WEST
        ball.vel = Vector(-ball.vel.x, ball.vel.y)  # Reverse x-direction
