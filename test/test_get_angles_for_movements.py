import unittest

from src.utils import get_angles_for_azimut_init

class Test_get_angles_for_azimut_init(unittest.TestCase):
    def test_from_0_to_90_by_ten(self):
        self.assertEqual(get_angles_for_azimut_init(0, 90, 10), [0.0, 9.0, 18.0, 27.0, 36.0, 45.0, 54.0, 63.0, 72.0, 81.0])

    def test_from_0_to_180_by_ten(self):
        self.assertEqual(get_angles_for_azimut_init(0, 180, 10), [0.0, 18.0, 36.0, 54.0, 72.0, 90.0, 108.0, 126.0, 144.0, 162.0])
      
    def test_from_0_to_90_by_twenty(self):
        self.assertEqual(get_angles_for_azimut_init(0, 90, 20), [0.0, 4.5, 9.0, 13.5, 18.0, 22.5, 27.0, 31.5, 36.0, 40.5, 45.0, 49.5, 54.0, 58.5, 63.0, 67.5, 72.0, 76.5, 81.0, 85.5])

    def test_from_0_to_90_by_zero(self):
        self.assertEqual(get_angles_for_azimut_init(0, 90, 0), [0.0])
    
    def test_from_0_to_0_by_ten(self):
        self.assertEqual(get_angles_for_azimut_init(0, 0, 3), [0.0, 0.0, 0.0])
    
    def test_from_0_to_0_by_zero(self):
        self.assertEqual(get_angles_for_azimut_init(0, 0, 0), [0.0])