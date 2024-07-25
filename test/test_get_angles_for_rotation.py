import unittest

from src.utils import get_angles_for_rotation


class Test_get_angles_for_rotation(unittest.TestCase):
    def test_two_rotation_ten(self):
        self.assertEqual(get_angles_for_rotation(2, 10), [-5.0, 5.0])

    def test_three_rotation_one(self):
        self.assertEqual(get_angles_for_rotation(3, 1), [-1.0, 0.0, 1.0])

    def test_two_rotation_zero(self):
        self.assertEqual(get_angles_for_rotation(2, 0), [0.0, 0.0])

    def test_one_rotation_zero(self):
        self.assertEqual(get_angles_for_rotation(1, 0), [0.0])

    def test_one_rotation_hundred(self):
        self.assertEqual(get_angles_for_rotation(1, 100), [0.0])
