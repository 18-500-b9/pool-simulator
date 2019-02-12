import unittest
import sys

sys.path.append("../")
from pool import vector


class PoolBallTest(unittest.TestCase):

    def test_angle_straight(self):
        # Test each straight
        v1 = vector.Vector(1, 0)
        v2 = vector.Vector(0, 1)
        v3 = vector.Vector(-1, 0)
        v4 = vector.Vector(0, -1)

        self.assertEqual(v1.ang, 0)
        self.assertEqual(v2.ang, 90)
        self.assertEqual(v3.ang, 180)
        self.assertEqual(v4.ang, 270)

    def test_angle_quadrants(self):
        # Test each quadrant
        v1 = vector.Vector(1, 1)
        v2 = vector.Vector(-1, 1)
        v3 = vector.Vector(-1, -1)
        v4 = vector.Vector(1, -1)

        self.assertEqual(v1.ang, 45)
        self.assertEqual(v2.ang, 135)
        self.assertEqual(v3.ang, 225)
        self.assertEqual(v4.ang, 315)


if __name__ == '__main__':
    unittest.main()
