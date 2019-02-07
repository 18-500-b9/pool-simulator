class PoolBall():
    def __init__(self,
                 name, radius,
                 x_pos, y_pos,
                 x_speed=0, y_speed=0):

        self.name = name
        self.radius = radius

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.x_speed = x_speed
        self.y_speed = y_speed

    def __str__(self):
        return "PoolBall {} at ({},{})".format(self.name,
                                               self.x_pos, self.y_pos)
