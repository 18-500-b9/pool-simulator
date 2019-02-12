import numpy as np


class Point():

    '''
    Cartesian coordinates.
    '''

    def __init__(self, x: 'float', y: 'float'):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Vector():
    '''
    2-D vector with x and y components.
    '''

    def __init__(self, x: 'float', y: 'float'):
        self.x = x
        self.y = y
        self.mag = Vector.get_magnitude(x, y)
        self.ang = Vector.get_angle(x, y)

    def set(self, x, y):
        '''
        Set the x and y components for this vector.
        '''
        self.x = x
        self.y = y
        self.mag = Vector.get_magnitude(x, y)
        self.ang = Vector.get_angle(x, y)

    @staticmethod
    def get_magnitude(x, y):
        '''
        Get the magnitude, given x and y components.
        '''

        return np.sqrt(x**2 + y**2)

    @staticmethod
    def get_angle(x, y):
        '''
        Given x and y, compute the angle (degrees), north of the x-axis.
        '''

        # On the x or y axis
        if x == 0:
            if y > 0:
                return 90
            elif y < 0:
                return 270
        elif y == 0:
            if x > 0:
                return 0
            else:
                return 180

        # Compute raw angle (between -90 and 90)
        raw_angle = np.degrees(np.arctan(y/x))

        if x > 0 and y > 0:  # Quadrant 1
            return raw_angle
        elif x < 0 and y > 0:  # Quadrant 2
            return 180 + raw_angle
        elif x < 0 and y < 0:  # Quadrant 3
            return 180 + raw_angle
        else:  # Quadrant 4
            return (360 + raw_angle) % 360

    def __str__(self):
        return "Magnitude = {}, Angle = {}".format(self.mag, self.ang)
