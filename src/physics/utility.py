"""
Utility class to hold various functions.
"""
from typing import Optional

import numpy as np

from physics.coordinates import Coordinates
from physics.vector import Vector


def get_distance(a: Coordinates, b=Coordinates(0, 0)) -> float:
    """
    Calculate the distance between two points.

    :param a: point a
    :param b: point b, default is origin (0, 0)
    :return: distance
    """

    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def get_angle(a: Coordinates, b=Coordinates(0, 0)) -> float:
    """
    Calculate the angle (relative to positive x-axis) of a relative to b.
    i.e. b becomes the origin

    :param a: point a
    :param b: point b, default is origin (0, 0)
    :return: angle of a to b (degrees)
    """

    y = a.y - b.y
    x = a.x - b.x

    # print('get_angle, relative point is ({}, {})'.format(x, y))

    if x == y == 0:
        return None  # FIXME: Best return value for 'no angle'?
    elif x == 0:
        if y > 0:
            return 90.0
        elif y < 0:
            return 270.0
    elif y == 0:
        if x > 0:
            return 0.0
        else:
            return 180.0

    # Compute raw angle (between -90 and 90)
    raw_angle = np.degrees(np.arctan(y / x))

    if x > 0 and y > 0:  # Quadrant 1
        return raw_angle
    elif x < 0 and y > 0:  # Quadrant 2
        return 180.0 + raw_angle
    elif x < 0 and y < 0:  # Quadrant 3
        return 180.0 + raw_angle
    else:  # Quadrant 4
        return (360.0 + raw_angle) % 360.0


def check_ray_circle_intersection(p1: Coordinates, p2: Coordinates, c_mid: Coordinates, c_radius: float):
    """
    Check whether a ray intersects a circle.

    :param p1: starting point of ray
    :param p2: end point of ray
    :param c_mid: coordinates for the center of the circle
    :param c_radius: radius of the circle
    :return: True if intersection; False otherwise
    """

    # Source: https://stackoverflow.com/a/1084899

    # d is direction vector of ray, from start to end
    # f is direction Vector from center sphere to ray start
    d = Vector(p2.y - p1.y, p2.x - p1.x)
    f = Vector(p1.y - c_mid.y, p1.x - c_mid.x)

    a = d.dot_product(d)
    b = 2 * f.dot_product(d)
    c = f.dot_product(f) - c_radius ** 2

    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        return False
    else:
        discriminant = np.sqrt(discriminant)

        t1 = (-b - discriminant) / (2 * a)
        t2 = (-b + discriminant) / (2 * a)

        return (0 <= t1 <= 1) or (0 <= t2 <= 1)


def check_ray_line_intersection(p1: Coordinates, p2: Coordinates,
                                p3: Coordinates, p4: Coordinates) -> Optional[Coordinates]:
    """
    Check whether a ray intersections a line.

    Source: https://stackoverflow.com/a/19550879

    :param p1: point A of line segment A
    :param p2: point B of line segment A
    :param p3: point A of line segment B
    :param p4: point B of line segment B

    :return: the point of intersection; None otherwise
    """

    s10_x = p2.x - p1.x
    s10_y = p2.y - p1.y
    s32_x = p4.x - p3.x
    s32_y = p4.y - p3.y

    denom = s10_x * s32_y - s32_x * s10_y

    if denom == 0: return None  # collinear

    denom_is_positive = denom > 0

    s02_x = p1.x - p3.x
    s02_y = p1.y - p3.y

    s_numer = s10_x * s02_y - s10_y * s02_x

    if (s_numer < 0) == denom_is_positive:
        return None  # no collision

    t_numer = s32_x * s02_y - s32_y * s02_x

    if (t_numer < 0) == denom_is_positive:
        return None  # no collision

    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive:
        return None  # no collision

    # collision detected
    t = t_numer / denom
    intersection_point = Coordinates(p1.x + (t * s10_x), p1.y + (t * s10_y))
    return intersection_point
