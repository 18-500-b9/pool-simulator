from physics.coordinates import Coordinates
from physics.utility import get_distance, get_angle
from physics.vector import Vector


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

    a_vel_new = a_vel - (2*b_mass)/(a_mass+b_mass) * ((a_vel-b_vel).dot_product(a_pos-b_pos))/get_distance(a_pos-b_pos)**2 * (a_pos-b_pos)
    b_vel_new = b_vel - (2*a_mass)/(a_mass+b_mass) * ((b_vel-a_vel).dot_product(b_pos-a_pos))/get_distance(b_pos-a_pos)**2 * (b_pos-a_pos)

    # a_vel_new = Vector((a_vel.x * (a_mass - b_mass) + (2 * b_mass * b_vel.x)) / (a_mass + b_mass),
    #                    (a_vel.y * (a_mass - b_mass) + (2 * b_mass * b_vel.y)) / (a_mass + b_mass))
    # b_vel_new = Vector((b_vel.x * (b_mass - a_mass) + (2 * a_mass * a_vel.x)) / (a_mass + b_mass),
    #                    (b_vel.y * (b_mass - a_mass) + (2 * a_mass * a_vel.y)) / (a_mass + b_mass))


    return a_vel_new, b_vel_new

def check_ball_wall_collision(ball_center: Coordinates, ball_radius: float,
                              north: float, east: float, south: float, west: float) -> bool:
    """
    Check if a ball has collided with a wall.

    :param ball_center: center of ball
    :param ball_radius: radius of ball
    :param north: north wall boundary
    :param east: east wall boundary
    :param south: south wall boundary
    :param west: west wall boundary
    :return: whether this ball has collided with a wall
    """

    return (ball_center.y + ball_radius >= north or
            ball_center.x + ball_radius >= east or
            ball_center.y - ball_radius <= south or
            ball_center.x - ball_radius <= west)
