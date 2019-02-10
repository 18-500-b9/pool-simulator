import numpy as np


class Vector():
    '''
    Vector with x and y components.
    '''

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def magnitude(self):
        '''
        Get the magnitude of this vector.
        '''

        return np.sqrt(self.x**2 + self.y**2)

    def angle(self):
        '''
        Get the angle of this vector.
        '''

        return np.arctan(self.y / self.x)

    def __str__(self):
        return "Magnitude = {}, Angle = {}".format(
                self.magnitude(), self.angle())
