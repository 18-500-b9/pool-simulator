import pygame
import sys

import colors
from helper import Vector
from pool_ball import PoolBall

SCREEN_DIMENSIONS = WIDTH, HEIGHT = 800, 300
SCREEN = None

# Global state of all balls (TODO: Wrap into class?)
BALLS = []

def init():
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode(SCREEN_DIMENSIONS)


def get_ball_color(ball_name):
    '''
    Get color of given pool ball.
    '''
    if ball_name == '1':
        return colors.YELLOW
    elif ball_name == '2':
        return colors.BLUE
    elif ball_name == '3':
        return colors.RED
    elif ball_name == '4':
        return colors.PURPLE
    elif ball_name == '5':
        return colors.ORANGE
    elif ball_name == '6':
        return colors.GREEN
    elif ball_name == '7':
        return colors.MAROON
    elif ball_name == '8':
        return colors.BLACK
    elif ball_name == '9':
        return colors.SILVER
    else:
        return colors.WHITE


def draw_pool_ball(pool_ball):
    global SCREEN

    ball_color = get_ball_color(pool_ball.name)
    ball_pos = (int(pool_ball.pos.x), int(pool_ball.pos.y))

    # Draw a circle
    pygame.draw.circle(SCREEN, ball_color, ball_pos, 10)


def main():
    init()

    nine_ball = PoolBall('9', 1.0, Vector(0.0, 0.0))

    draw_pool_ball(nine_ball)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()


if __name__ == '__main__':
    main()
