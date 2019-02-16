import numpy as np

from physics.coordinates import Coordinates
from pool.ball_type import BallType
from pool.game_type import GameType
from pool.pool_ball import PoolBall

LONG_DIAMONDS = 8
SHORT_DIAMONDS = 4
CUE_START_DIAMOND = 2
RACK_START_DIAMOND = 6


class PoolTable:
    def __init__(self, length: float):
        self.length = float(length)
        self.width = float(length) / 2  # Pool tables have 2:1 ratio

        self.balls = PoolTable.get_balls(GameType.THREE_BALL)
        self.rack_balls(GameType.THREE_BALL)

    @staticmethod
    def get_balls(game: GameType):
        m = 10
        r = 10

        ball_c = PoolBall(BallType.CUE, Coordinates(0, 0), m, r)
        ball_1 = PoolBall(BallType.ONE, Coordinates(0, 0), m, r)
        # ball_2 = PoolBall(BallType.TWO, Coordinates(0, 0), m, r)
        # ball_3 = PoolBall(BallType.THREE, Coordinates(0, 0), m, r)

        balls = {
            BallType.CUE: ball_c,
            BallType.ONE: ball_1,
            # BallType.TWO: ball_2,
            # BallType.THREE: ball_3,
        }

        return balls

    def rack_balls(self, game: GameType):
        """
        Set the position of balls for racking position.
        *All balls assumed to have the same radius.*

        :param game: type of game to be racked for
        """

        # TODO: Need random/shuffling of balls except for fixed balls (ONE, NINE)
        balls = self.balls
        r = balls[BallType.ONE].radius

        # Set cue ball position
        balls[BallType.CUE].pos.x = (CUE_START_DIAMOND / LONG_DIAMONDS) * self.length
        balls[BallType.CUE].pos.y = self.width / 2

        if game == GameType.THREE_BALL:
            # Coordinates of leading 1 ball
            balls[BallType.ONE].pos.x = (RACK_START_DIAMOND / LONG_DIAMONDS) * self.length
            balls[BallType.ONE].pos.y = self.width / 2 - 3

            # balls[BallType.TWO].pos.x = balls[BallType.ONE].pos.x + np.sqrt(3) * r
            # balls[BallType.TWO].pos.y = balls[BallType.ONE].pos.y + r

            # balls[BallType.THREE].pos.x = balls[BallType.ONE].pos.x + np.sqrt(3) * r
            # balls[BallType.THREE].pos.y = balls[BallType.ONE].pos.y - r