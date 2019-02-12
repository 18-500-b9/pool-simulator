import unittest
import sys

sys.path.append('../../src')
from physics.vector import Vector

import numpy as np

class VectorTest(unittest.TestCase):

    def test_init(self):
        v = Vector(1, 1)

        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 1.0)

        # Type check
        self.assertIsInstance(v.x, float)
        self.assertIsInstance(v.y, float)
        self.assertIsInstance(v.mag, float)
        self.assertIsInstance(v.ang, float)

    def test_equals(self):
        v0 = Vector(1, 1)
        v1 = Vector(1, 1)

        self.assertEqual(v0, v1)

    def test_not_equals(self):
        v0 = Vector(1, 1)
        v1 = Vector(1, 1.1)

        self.assertNotEqual(v0, v1)

    def test_magnitude(self):
        v = Vector(3.0, 4.0)

        self.assertEqual(v.mag, 5.0)

    def test_angle(self):
        v = Vector(3.0, 4.0)

        self.assertEqual(v.ang, np.degrees(np.arctan(4.0/3.0)))

    def test_zero(self):
        v = Vector(0.0, 0.0)

        self.assertEqual(v.x, 0.0)
        self.assertEqual(v.y, 0.0)
        self.assertEqual(v.mag, 0.0)
        self.assertEqual(v.ang, None)

    def test_angle_straight(self):
        # Test each straight
        v1 = Vector(1, 0)
        v2 = Vector(0, 1)
        v3 = Vector(-1, 0)
        v4 = Vector(0, -1)

        self.assertEqual(v1.ang, 0)
        self.assertEqual(v2.ang, 90)
        self.assertEqual(v3.ang, 180)
        self.assertEqual(v4.ang, 270)

    def test_angle_quadrants(self):
        # Test each quadrant
        v1 = Vector(1, 1)
        v2 = Vector(-1, 1)
        v3 = Vector(-1, -1)
        v4 = Vector(1, -1)

        self.assertEqual(v1.ang, 45)
        self.assertEqual(v2.ang, 135)
        self.assertEqual(v3.ang, 225)
        self.assertEqual(v4.ang, 315)


if __name__ == '__main__':
    unittest.main()
