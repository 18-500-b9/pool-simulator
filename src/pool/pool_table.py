from typing import List

import numpy as np

from physics.collisions import check_ball_ball_collision, resolve_ball_ball_collision, resolve_ball_wall_collision, \
    check_ball_wall_collision
from physics.coordinates import Coordinates
from physics.utility import get_distance, check_ray_circle_intersection, check_ray_line_intersection
from pool.ball_type import BallType
from pool.game_type import GameType
from pool.pool_ball import PoolBall

LONG_DIAMONDS = 8
SHORT_DIAMONDS = 4
CUE_START_DIAMOND = 2
RACK_START_DIAMOND = 6


class PoolTable:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

        self.length = right - left
        self.width = abs(top - bottom)

        self.balls = PoolTable.get_balls(GameType.NINE_BALL)
        self.rack_balls(GameType.NINE_BALL)

        self.cue_angle = 0.0
        self.cue_line_end = None

        # For drawing rail and pockets
        self.rail_width = 0

        self.hole_centers = self.get_pockets()
        self.hole_radius = 2.25 * self.balls[BallType.CUE].radius

        self.corner_pocket_width = 5
        self.side_pocket_width = 5

        self.corner_pocket_angle = 5
        self.side_pocket_angle = 5

    @staticmethod
    def get_balls(game: GameType):
        m = 10
        r = 10

        ball_c = PoolBall(BallType.CUE, Coordinates(0, 0), m, r)
        ball_1 = PoolBall(BallType.ONE, Coordinates(0, 0), m, r)
        ball_2 = PoolBall(BallType.TWO, Coordinates(0, 0), m, r)
        ball_3 = PoolBall(BallType.THREE, Coordinates(0, 0), m, r)
        ball_4 = PoolBall(BallType.FOUR, Coordinates(0, 0), m, r)
        ball_5 = PoolBall(BallType.FIVE, Coordinates(0, 0), m, r)
        ball_6 = PoolBall(BallType.SIX, Coordinates(0, 0), m, r)
        ball_7 = PoolBall(BallType.SEVEN, Coordinates(0, 0), m, r)
        ball_8 = PoolBall(BallType.EIGHT, Coordinates(0, 0), m, r)
        ball_9 = PoolBall(BallType.NINE, Coordinates(0, 0), m, r)

        balls = {
            BallType.CUE: ball_c,
            BallType.ONE: ball_1,
            BallType.TWO: ball_2,
            BallType.THREE: ball_3,
            BallType.FOUR: ball_4,
            BallType.FIVE: ball_5,
            BallType.SIX: ball_6,
            BallType.SEVEN: ball_7,
            BallType.EIGHT: ball_8,
            BallType.NINE: ball_9,
        }

        return balls

    def get_pockets(self) -> List[Coordinates]:
        """
        Get 6 coordinates for the center of the pockets.
        Assuming upper left corner is origin (PyGame).
        """

        return [
            Coordinates(self.left, self.top),
            Coordinates(self.left + self.length / 2, self.top),
            Coordinates(self.left + self.length, self.top),
            Coordinates(self.right, self.bottom),
            Coordinates(self.right - self.length / 2, self.bottom),
            Coordinates(self.right - self.length, self.bottom),
        ]

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
        balls[BallType.CUE].pos.y = self.width / 2 + 20

        if game == GameType.THREE_BALL:
            # Coordinates of leading 1 ball
            balls[BallType.ONE].pos.x = (RACK_START_DIAMOND / LONG_DIAMONDS) * self.length
            balls[BallType.ONE].pos.y = self.width / 2

            balls[BallType.TWO].pos.x = balls[BallType.ONE].pos.x + np.sqrt(3) * r
            balls[BallType.TWO].pos.y = balls[BallType.ONE].pos.y + r

            balls[BallType.THREE].pos.x = balls[BallType.ONE].pos.x + np.sqrt(3) * r
            balls[BallType.THREE].pos.y = balls[BallType.ONE].pos.y - r

        elif game == GameType.NINE_BALL:
            # Coordinates of leading 1 ball
            balls[BallType.ONE].pos.x = (RACK_START_DIAMOND / LONG_DIAMONDS) * self.length
            balls[BallType.ONE].pos.y = self.width / 2

            balls[BallType.TWO].pos.x = balls[BallType.ONE].pos.x + np.sqrt(3) * r
            balls[BallType.TWO].pos.y = balls[BallType.ONE].pos.y + r

            balls[BallType.THREE].pos.x = balls[BallType.ONE].pos.x + np.sqrt(3) * r
            balls[BallType.THREE].pos.y = balls[BallType.ONE].pos.y - r

            balls[BallType.FOUR].pos.x = balls[BallType.TWO].pos.x + np.sqrt(3) * r
            balls[BallType.FOUR].pos.y = balls[BallType.TWO].pos.y + r

            balls[BallType.NINE].pos.x = balls[BallType.TWO].pos.x + np.sqrt(3) * r
            balls[BallType.NINE].pos.y = balls[BallType.TWO].pos.y - r

            balls[BallType.FIVE].pos.x = balls[BallType.THREE].pos.x + np.sqrt(3) * r
            balls[BallType.FIVE].pos.y = balls[BallType.THREE].pos.y - r

            balls[BallType.SIX].pos.x = balls[BallType.NINE].pos.x + np.sqrt(3) * r
            balls[BallType.SIX].pos.y = balls[BallType.NINE].pos.y + r

            balls[BallType.SEVEN].pos.x = balls[BallType.NINE].pos.x + np.sqrt(3) * r
            balls[BallType.SEVEN].pos.y = balls[BallType.NINE].pos.y - r

            balls[BallType.EIGHT].pos.x = balls[BallType.SEVEN].pos.x + np.sqrt(3) * r
            balls[BallType.EIGHT].pos.y = balls[BallType.SEVEN].pos.y + r

    def pocket_balls(self):
        """
        Call this method to check if any balls should be pocketed and remove them from play.

        :return:
        """

        pocketed_ball_names = []

        for ball_name in self.balls:
            ball = self.balls[ball_name]
            for pocket_pos in self.hole_centers:
                d = get_distance(ball.pos, pocket_pos)
                pocketed = d < self.hole_radius
                if pocketed:
                    print("Ball {} is pocketed into {}".format(ball_name, pocket_pos))
                    pocketed_ball_names.append(ball_name)

        # Remove these balls from play
        for ball_name in pocketed_ball_names:
            if ball_name is not BallType.CUE:  # Don't pocket cue ball
                del self.balls[ball_name]
            else:
                # Restart cue ball position
                self.balls[ball_name].pos.x = (CUE_START_DIAMOND / LONG_DIAMONDS) * self.length
                self.balls[ball_name].pos.y = self.width / 2 + 20
                self.balls[ball_name].vel.x = self.balls[ball_name].vel.y = 0

    def time_step(self):
        balls = list(self.balls.values())

        # Update ball positions
        for ball in balls:
            ball.time_step()

        # Check/resolve collisions
        for i in range(len(balls)):
            # Check ball-wall collision
            ball_wall_collision = check_ball_wall_collision(balls[i], (self.top, self.left), (self.bottom, self.right))
            if ball_wall_collision is not None:
                # print("BALL {}, WALL {}".format(balls[i], ball_wall_collision))

                resolve_ball_wall_collision(balls[i], ball_wall_collision)

            for j in range(i + 1, len(balls)):
                if check_ball_ball_collision(balls[i], balls[j]):
                    # print("BALL {}, BALL {}".format(balls[i], balls[j]))

                    resolve_ball_ball_collision(balls[i], balls[j])

        # Check pocketed balls
        self.pocket_balls()

        # Get cue ball path
        self.cue_ball_path()

    def cue_ball_path(self) -> (Coordinates, Coordinates):
        """
        Get the endpoints for the line from the cue ball to the nearest target.

        :return:
        """

        cue_ball_pos = None
        for ball_type, ball in self.balls.items():
            if ball_type is BallType.CUE:
                cue_ball_pos = ball.pos
                break

        assert (cue_ball_pos is not None)

        p1 = cue_ball_pos
        p2 = Coordinates(cue_ball_pos.x + self.length * np.cos(np.radians(self.cue_angle)),
                         cue_ball_pos.y - self.length * np.sin(np.radians(self.cue_angle)))

        # See if there's a ball in the way
        for ball_type, ball in self.balls.items():
            if ball.ball_type is BallType.CUE: continue

            if check_ray_circle_intersection(cue_ball_pos, p2, ball.pos, ball.radius):
                # print("CUE BALL LINE INTERSECTING {}".format(ball))
                self.cue_line_end = ball.pos
                return

        # Get the nearest intersecting cushion
        nw = Coordinates(self.left, self.top)
        ne = Coordinates(self.right, self.top)
        se = Coordinates(self.right, self.bottom)
        sw = Coordinates(self.left, self.bottom)
        cushion_intersections = [check_ray_line_intersection(p1, p2, nw, ne),
                                 check_ray_line_intersection(p1, p2, ne, se),
                                 check_ray_line_intersection(p1, p2, se, sw),
                                 check_ray_line_intersection(p1, p2, sw, nw)]

        for point in cushion_intersections:
            if point is not None:
                self.cue_line_end = point

    def target_ball_path(self):
        return
