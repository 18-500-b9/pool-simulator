import sys
import unittest

sys.path.append('../../src')

from physics.coordinates import Coordinates
from physics.vector import Vector
from physics.collisions import check_ball_ball_collision
from physics.collisions import check_ball_wall_collision
from physics.collisions import resolve_ball_ball_collision


class CoordinatesTest(unittest.TestCase):

    def assertVectorAlmostEqual(self, v_a: Vector, v_b: Vector):
        """
        Custom test method to test if 2 vectors are almost equal.

        :param v_a: first vector to compare
        :param v_b: second vector to compare
        :raises: AssertionError if not almost equal
        """
        self.assertAlmostEqual(v_a.x, v_b.x, places=14)
        self.assertAlmostEqual(v_a.y, v_b.y, places=14)

    """
    Testing check_ball_ball_collision()
    """

    def test_check_ball_ball_collision_x_axis(self):
        a_radius = 0.5
        b_radius = 0.5

        # On x-axis, not touching
        result = check_ball_ball_collision(Coordinates(0.0, 0.0), a_radius,
                                           Coordinates(1.01, 0.0), b_radius)
        self.assertFalse(result)

        # On x-axis, touching
        result = check_ball_ball_collision(Coordinates(0.0, 0.0), a_radius,
                                           Coordinates(1.00, 0.0), b_radius)
        self.assertTrue(result)

        # On x-axis, overlapping
        result = check_ball_ball_collision(Coordinates(0.0, 0.0), a_radius,
                                           Coordinates(0.99, 0.0), b_radius)
        self.assertTrue(result)

    def test_check_ball_ball_collision_y_axis(self):
        a_radius = 0.5
        b_radius = 0.5

        # On x-axis, not touching
        result = check_ball_ball_collision(Coordinates(0.0, 2.01), a_radius,
                                           Coordinates(0.0, 0.0), b_radius)
        self.assertFalse(result)

        # On x-axis, touching
        result = check_ball_ball_collision(Coordinates(0.0, 1.00), a_radius,
                                           Coordinates(0.0, 0.0), b_radius)
        self.assertTrue(result)

        # On x-axis, overlapping
        result = check_ball_ball_collision(Coordinates(0.0, 0.99), a_radius,
                                           Coordinates(0.0, 0.0), b_radius)
        self.assertTrue(result)

    """
    Testing check_ball_wall_collision()
    """

    def test_check_ball_wall_collision(self):
        ball_radius = 0.1
        n, e, s, w = 1.0, 1.0, -1.0, -1.0

        # Not touching any walls
        result = check_ball_wall_collision(Coordinates(0.0, 0.0), ball_radius, n, e, s, w)
        self.assertFalse(result)

        # Touching each wall
        result_n = check_ball_wall_collision(Coordinates(0.0, 0.9), ball_radius, n, e, s, w)
        result_e = check_ball_wall_collision(Coordinates(0.9, 0.0), ball_radius, n, e, s, w)
        result_s = check_ball_wall_collision(Coordinates(0.0, -0.9), ball_radius, n, e, s, w)
        result_w = check_ball_wall_collision(Coordinates(-0.9, 0.0), ball_radius, n, e, s, w)

        self.assertTrue(result_n)
        self.assertTrue(result_e)
        self.assertTrue(result_s)
        self.assertTrue(result_w)

        # Overlapping each wall
        result_n = check_ball_wall_collision(Coordinates(0.0, 0.91), ball_radius, n, e, s, w)
        result_e = check_ball_wall_collision(Coordinates(0.91, 0.0), ball_radius, n, e, s, w)
        result_s = check_ball_wall_collision(Coordinates(0.0, -0.91), ball_radius, n, e, s, w)
        result_w = check_ball_wall_collision(Coordinates(-0.91, 0.0), ball_radius, n, e, s, w)

        self.assertTrue(result_n)
        self.assertTrue(result_e)
        self.assertTrue(result_s)
        self.assertTrue(result_w)

        # Touching each corner
        result_ne = check_ball_wall_collision(Coordinates(0.9, 0.9), ball_radius, n, e, s, w)
        result_nw = check_ball_wall_collision(Coordinates(-0.9, 0.9), ball_radius, n, e, s, w)
        result_se = check_ball_wall_collision(Coordinates(0.9, -0.9), ball_radius, n, e, s, w)
        result_sw = check_ball_wall_collision(Coordinates(-0.9, -0.9), ball_radius, n, e, s, w)

        self.assertTrue(result_ne)
        self.assertTrue(result_nw)
        self.assertTrue(result_se)
        self.assertTrue(result_sw)

        # Overlapping each corner
        result_ne = check_ball_wall_collision(Coordinates(0.91, 0.91), ball_radius, n, e, s, w)
        result_nw = check_ball_wall_collision(Coordinates(-0.91, 0.91), ball_radius, n, e, s, w)
        result_se = check_ball_wall_collision(Coordinates(0.91, -0.91), ball_radius, n, e, s, w)
        result_sw = check_ball_wall_collision(Coordinates(-0.91, -0.91), ball_radius, n, e, s, w)

        self.assertTrue(result_ne)
        self.assertTrue(result_nw)
        self.assertTrue(result_se)
        self.assertTrue(result_sw)

    """
    Testing check_ball_wall_collision() with equal masses
    """

    def test_resolve_ball_ball_collision_1d(self):
        # 1-D, stationary target ball
        a_pos, a_vel, a_mass = Coordinates(-1.0, 0.0), Vector(2.0, 0.0), 3.0
        b_pos, b_vel, b_mass = Coordinates(0.0, 0.0), Vector(0.0, 0.0), 3.0

        result = resolve_ball_ball_collision(a_pos, a_vel, a_mass, b_pos, b_vel, b_mass)

        a_vel_new = Vector(0.0, 0.0)
        b_vel_new = Vector(2.0, 0.0)

        self.assertVectorAlmostEqual(result[0], a_vel_new)
        self.assertVectorAlmostEqual(result[1], b_vel_new)

        # 1-D, head-on collision, same speeds
        a_pos, a_vel, a_mass = Coordinates(-1.0, 0.0), Vector(2.0, 0.0), 3.0
        b_pos, b_vel, b_mass = Coordinates(0.0, 0.0), Vector(-2.0, 0.0), 3.0

        result = resolve_ball_ball_collision(a_pos, a_vel, a_mass, b_pos, b_vel, b_mass)

        a_vel_new = Vector(-2.0, 0.0)
        b_vel_new = Vector(2.0, 0.0)

        self.assertVectorAlmostEqual(result[0], a_vel_new)
        self.assertVectorAlmostEqual(result[1], b_vel_new)

        # 1-D, head-on collision, different speeds
        a_pos, a_vel, a_mass = Coordinates(-1.0, 0.0), Vector(2.0, 0.0), 3.0
        b_pos, b_vel, b_mass = Coordinates(0.0, 0.0), Vector(-1.0, 0.0), 3.0

        result = resolve_ball_ball_collision(a_pos, a_vel, a_mass, b_pos, b_vel, b_mass)

        a_vel_new = Vector(-1.0, 0.0)
        b_vel_new = Vector(2.0, 0.0)

        self.assertVectorAlmostEqual(result[0], a_vel_new)
        self.assertVectorAlmostEqual(result[1], b_vel_new)

    def test_resolve_ball_ball_collision_2d_basic(self):
        # 2-D, stationary target ball
        a_pos, a_vel, a_mass = Coordinates(-1.0, -1.0), Vector(2.0, 2.0), 3.0
        b_pos, b_vel, b_mass = Coordinates(0.0, 0.0), Vector(0.0, 0.0), 3.0

        result = resolve_ball_ball_collision(a_pos, a_vel, a_mass, b_pos, b_vel, b_mass)

        a_vel_new = Vector(0.0, 0.0)
        b_vel_new = Vector(2.0, 2.0)

        self.assertVectorAlmostEqual(result[0], a_vel_new)
        self.assertVectorAlmostEqual(result[1], b_vel_new)

        # 2-D, head-on collision, same speeds
        a_pos, a_vel, a_mass = Coordinates(-1.0, -1.0), Vector(2.0, 2.0), 3.0
        b_pos, b_vel, b_mass = Coordinates(0.0, 0.0), Vector(-2.0, -2.0), 3.0

        result = resolve_ball_ball_collision(a_pos, a_vel, a_mass, b_pos, b_vel, b_mass)

        a_vel_new = Vector(-2.0, -2.0)
        b_vel_new = Vector(2.0, 2.0)

        self.assertVectorAlmostEqual(result[0], a_vel_new)
        self.assertVectorAlmostEqual(result[1], b_vel_new)

    def test_resolve_ball_ball_collision_2d_complex(self):
        # 2-D, stationary target ball
        a_pos, a_vel, a_mass = Coordinates(-1.0, 0.0), Vector(1.0, 1.0), 3.0
        b_pos, b_vel, b_mass = Coordinates(0.0, 0.0), Vector(0.0, 0.0), 3.0

        result = resolve_ball_ball_collision(a_pos, a_vel, a_mass, b_pos, b_vel, b_mass)

        a_vel_new = Vector(0.0, 1.0)
        b_vel_new = Vector(1.0, 0.0)

        self.assertVectorAlmostEqual(result[0], a_vel_new)
        self.assertVectorAlmostEqual(result[1], b_vel_new)


if __name__ == '__main__':
    unittest.main()
