"""
Utility class to hold various functions.
"""

import numpy as np

from physics.coordinates import Coordinates

def get_distance(a: Coordinates, b=Coordinates(0,0)) -> float:
    """
    Calculate the distance between two points.

    :param a: point a
    :param b: point b, default is origin (0, 0)
    :return: distance
    """

    return np.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

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

    # On the x or y axis
    if x == y == 0:
        return None
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
