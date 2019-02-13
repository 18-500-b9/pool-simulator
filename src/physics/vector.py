import physics.utility as util
from physics.coordinates import Coordinates


class Vector():
    """
    2-D vector with x and y components.
    """

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def get_magnitude(self):
        """
        Get the magnitude for this vector.
        """

        return util.get_distance(Coordinates(self.x, self.y))

    def get_angle(self):
        """
        Get the angle for this vector.
        """

        return util.get_angle(Coordinates(self.x, self.y))

    def dot_product(self, other):
        """
        Dot product dot product of this vector * other vector.
        :return: scalar dot product
        """
        return self.x * other.x + self.y * other.y

    def __add__(self, other):
        """
        Add another vector to this vector.

        :param other:
        :return: new vector representing sum
        """

        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        Subtract another vector from this vector.

        :param other:
        :return: new vector representing difference
        """

        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        """
        Multiply this vector by a scalar.

        :param scalar: value to scale vector by
        :return: new, scaled vector
        """

        return Vector(self.x*scalar, self.y*scalar)

    def __rmul__(self, scalar: float):
        """
        Multiply this vector by a scalar.

        :param scalar: value to scale vector by
        :return: new, scaled vector
        """

        return Vector(self.x*scalar, self.y*scalar)

    def __str__(self):
        return "Vector ({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)
