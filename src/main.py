import sys

import numpy as np
import pygame

from physics.collisions import *
from physics.utility import get_angle
from pool.ball_type import BallType
from pool.pool_ball import PoolBall
from pool.pool_table import PoolTable

SCREEN_DIMENSIONS = WIDTH, HEIGHT = 800, 800
TABLE_LENGTH = 500
TABLE_OFFSET_X, TABLE_OFFSET_Y = 10, 10
SCREEN = None

"""
Helper functions.
"""
def to_pygame(xy: Coordinates, height: float) -> (float, float):
    """
    Convert Coordinates into PyGame coordinates tuple (lower-left => top-left).
    """

    return int(xy.x) + TABLE_OFFSET_X, int(height - xy.y) + TABLE_OFFSET_Y

"""
PyGame functions.
"""

def init():
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode(SCREEN_DIMENSIONS)


def clear_screen():
    global SCREEN
    SCREEN.fill((0, 0, 0))


def draw_pool_table(table: PoolTable):
    global SCREEN

    # Draw table cloth
    pygame.draw.rect(SCREEN, (0, 200, 0), pygame.Rect(TABLE_OFFSET_X, TABLE_OFFSET_Y, table.length, table.width), 0)

    # Draw table pockets
    for hole_center in table.hole_centers:
        pygame.draw.circle(SCREEN, (0, 0, 0), to_pygame(hole_center, table.width), int(table.hole_radius))


def draw_pool_cue(table: PoolTable):
    global SCREEN

    if table.cue_angle == 0.0:
        return

    cue_ball_pos = table.balls[BallType.CUE].pos

    if table.cue_line_end is None:
        cue_stick_length = np.sqrt(table.length**2 + table.width**2)
    else:
        cue_stick_length = get_distance(cue_ball_pos, table.cue_line_end)
    cue_stick_x = cue_ball_pos.x + cue_stick_length * np.cos(np.radians(table.cue_angle))
    cue_stick_y = cue_ball_pos.y - cue_stick_length * np.sin(np.radians(table.cue_angle))

    pygame.draw.line(SCREEN, (139, 69, 19), (cue_ball_pos.x, cue_ball_pos.y), (cue_stick_x, cue_stick_y), 3)


def draw_pool_ball(ball: PoolBall):
    global SCREEN

    ball_color = ball.ball_type.color
    # print('draw_pool_ball, {} at {}, {}'.format(ball.ball_type.name, ball.pos.x, ball.pos.y))
    ball_pos = (int(ball.pos.x), int(ball.pos.y))

    # Draw a circle
    pygame.draw.circle(SCREEN, ball_color, ball_pos, ball.radius)


def main():
    init()

    # Create pool table
    table = PoolTable(TABLE_OFFSET_X, TABLE_OFFSET_Y,
                      TABLE_OFFSET_X+TABLE_LENGTH, TABLE_OFFSET_Y+TABLE_LENGTH/2)

    # DEBUG
    # table.balls[BallType.CUE].vel.x = 15.0


    while 1:
        # Get just the list of balls to iterate easily
        balls = list(table.balls.values())

        clear_screen()

        # Check Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                target_pos = Coordinates(pygame.mouse.get_pos()[0], HEIGHT-pygame.mouse.get_pos()[1])
                # print('target_pos:', target_pos)
                # FIXME: Hacky way to resolve pygame origin vs my origin
                cue_pos = Coordinates(table.balls[BallType.CUE].pos.x, HEIGHT-table.balls[BallType.CUE].pos.y)
                # print('cue_pos:', cue_pos)

                table.cue_angle = get_angle(target_pos, cue_pos)
                # print('AFTER SETTING cue_angle', table.cue_angle)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Strike cue ball
                    mag = 50.0
                    force = Vector(mag*np.cos(np.radians(table.cue_angle)), -mag*np.sin(np.radians(table.cue_angle)))
                    table.balls[BallType.CUE].apply_force(force)
                elif event.key == pygame.K_p:
                    # DEBUG set all speeds to 0
                    for ball in balls:
                        ball.vel.x, ball.vel.y = 0, 0

        # Table time step
        table.time_step()

        # Draw pool table
        draw_pool_table(table)

        # Draw pool cue line
        draw_pool_cue(table)

        # Draw all pool balls
        for ball in balls:
            draw_pool_ball(ball)

        pygame.display.flip()


if __name__ == '__main__':
    main()
