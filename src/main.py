import sys

import pygame

import numpy as np

from physics.collisions import *
from physics.utility import get_angle
from pool.ball_type import BallType
from pool.pool_ball import PoolBall
from pool.pool_table import PoolTable

SCREEN_DIMENSIONS = WIDTH, HEIGHT = 800, 300
SCREEN = None

# Global state of all balls (TODO: Wrap into class?)
BALLS = []


def init():
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode(SCREEN_DIMENSIONS)


def clear_screen():
    global SCREEN
    SCREEN.fill((0, 0, 0))


def draw_pool_table(table: PoolTable):
    global SCREEN
    pygame.draw.rect(SCREEN, (0, 200, 0), pygame.Rect(0, 0, table.length, table.width), 0)


def draw_pool_cue(table: PoolTable):
    global SCREEN

    if table.cue_angle == 0.0:
        return

    cue_ball_pos = table.balls[BallType.CUE].pos

    cue_stick_length = np.sqrt(WIDTH**2 + HEIGHT**2)
    cue_stick_x = cue_ball_pos.x + cue_stick_length * np.cos(np.radians(table.cue_angle))
    cue_stick_y = cue_ball_pos.y - cue_stick_length * np.sin(np.radians(table.cue_angle))

    pygame.draw.line(SCREEN, (139, 69, 19), (cue_ball_pos.x, cue_ball_pos.y), (cue_stick_x, cue_stick_y), 3)


def draw_pool_ball(ball: PoolBall):
    global SCREEN

    ball_color = ball.ball_type.color
    ball_pos = (int(ball.pos.x), int(ball.pos.y))

    # Draw a circle
    pygame.draw.circle(SCREEN, ball_color, ball_pos, ball.radius)


def main():
    init()

    # Create pool table
    table = PoolTable(length=600)

    # DEBUG
    table.balls[BallType.CUE].vel.x = 15.0

    # Get just the list of balls to iterate easily
    balls = list(table.balls.values())

    while 1:
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
                    mag = 100.0
                    force = Vector(mag*np.cos(np.radians(table.cue_angle)), -mag*np.sin(np.radians(table.cue_angle)))
                    table.balls[BallType.CUE].apply_force(force)

        # Update ball positions
        for ball in balls:
            ball.time_step()

        # Check/resolve collisions
        for i in range(len(balls)):
            # Check ball-wall collision
            ball_wall_collision = check_ball_wall_collision(balls[i], table.width, table.length, 0.0, 0.0)
            if ball_wall_collision is not None:
                # print("BALL {}, WALL {}".format(balls[i], ball_wall_collision))

                resolve_ball_wall_collision(balls[i], ball_wall_collision)

            for j in range(i + 1, len(balls)):
                if check_ball_ball_collision(balls[i], balls[j]):
                    # print("BALL {}, BALL {}".format(balls[i], balls[j]))

                    resolve_ball_ball_collision(balls[i], balls[j])

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
