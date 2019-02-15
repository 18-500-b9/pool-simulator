from enum import Enum


class Direction(Enum):
    """
    Cardinal compass directions
    """

    NORTH = 'NORTH'
    EAST = 'EAST'
    SOUTH = 'SOUTH'
    WEST = 'WEST'

    def __str__(self):
        return self.value

    def opposite(self):
        if self == self.NORTH:
            return self.SOUTH
        elif self == self.EAST:
            return self.WEST
        elif self == self.SOUTH:
            return self.NORTH
        else:  # WEST
            return self.EAST
