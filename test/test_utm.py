import utm as UTM
import unittest

try:
    import numpy as np
    use_numpy = True
except ImportError:
    use_numpy = False


class UTMTestCase(unittest.TestCase):
    def assert_utm_equal(self, a, b):
        if use_numpy and isinstance(b[0], np.ndarray):
            self.assertTrue(np.allclose(a[0], b[0]))
            self.assertTrue(np.allclose(a[1], b[1]))
        else:
            self.assertAlmostEqual(a[0], b[0], 0)
            self.assertAlmostEqual(a[1], b[1], 0)
        self.assertEqual(a[2], b[2])
        self.assertEqual(a[3].upper(), b[3].upper())

    def assert_latlon_equal(self, a, b):
        if use_numpy and isinstance(b[0], np.ndarray):
            self.assertTrue(np.allclose(a[0], b[0], rtol=1e-4, atol=1e-4))
            self.assertTrue(np.allclose(a[1], b[1], rtol=1e-4, atol=1e-4))
        else:
            self.assertAlmostEqual(a[0], b[0], 4)
            self.assertAlmostEqual(a[1], b[1], 4)


class KnownValues(UTMTestCase):
    known_values = [
        # Aachen, Germany
        (
            (50.77535, 6.08389),
            (294409, 5628898, 32, 'U'),
            {'northern': True},
        ),
        # New York, USA
        (
            (40.71435, -74.00597),
            (583960, 4507523, 18, 'T'),
            {'northern': True},
        ),
        # Wellington, New Zealand
        (
            (-41.28646, 174.77624),
            (313784, 5427057, 60, 'G'),
            {'northern': False},
        ),
        # Capetown, South Africa
        (
            (-33.92487, 18.42406),
            (261878, 6243186, 34, 'H'),
            {'northern': False},
        ),
        # Mendoza, Argentina
        (
            (-32.89018, -68.84405),
            (514586, 6360877, 19, 'h'),
            {'northern': False},
        ),
        # Fairbanks, Alaska, USA
        (
            (64.83778, -147.71639),
            (466013, 7190568, 6, 'W'),
            {'northern': True},
        ),
        # Ben Nevis, Scotland, UK
        (
            (56.79680, -5.00601),
            (377486, 6296562, 30, 'V'),
            {'northern': True},
        ),
        # Latitude 84
        (
            (84, -5.00601),
            (476594, 9328501, 30, 'X'),
            {'northern': True},
        ),
    ]

    def test_from_latlon(self):
        '''from_latlon should give known result with known input'''
        for latlon, utm, _ in self.known_values:
            result = UTM.from_latlon(*latlon)
            self.assert_utm_equal(utm, result)

    def test_from_latlon_numpy(self):
        if not use_numpy:
            return
        lats = np.array([0.0, 3.0, 6.0])
        lons = np.array([0.0, 1.0, 3.4])
        result = UTM.from_latlon(lats, lons)
        self.assert_utm_equal((np.array([166021.44317933032,
                                         277707.83075574087,
                                         544268.12794623]),
                               np.array([0.0,
                                         331796.29167519242,
                                         663220.7198366751]),
                               31, 'N'), result)

        for latlon, utm, _ in self.known_values:
            result = UTM.from_latlon(*[np.array([x]) for x in latlon])
            self.assert_utm_equal(utm, result)

    def test_to_latlon(self):
        '''to_latlon should give known result with known input'''
        for latlon, utm, utm_kw in self.known_values:
            result = UTM.to_latlon(*utm)
            self.assert_latlon_equal(latlon, result)

            result = UTM.to_latlon(*utm[0:3], **utm_kw)
            self.assert_latlon_equal(latlon, result)

    def test_to_latlon_numpy(self):
        if not use_numpy:
            return
        result = UTM.to_latlon(np.array([166021.44317933032,
                                         277707.83075574087,
                                         544268.12794623]),
                               np.array([0.0,
                                         331796.29167519242,
                                         663220.7198366751]),
                               31, northern=True)
        self.assert_latlon_equal((np.array([0.0, 3.0, 6.0]),
                                  np.array([0.0, 1.0, 3.4])),
                                 result)

        for latlon, utm, utm_kw in self.known_values:
            utm = [np.array([x]) for x in utm[:2]] + list(utm[2:])
            result = UTM.to_latlon(*utm)
            self.assert_latlon_equal(latlon, result)


class BadInput(UTMTestCase):
    def test_from_latlon_range_checks(self):
        '''from_latlon should fail with out-of-bounds input'''
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, -100, 0)
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, -80.1, 0)
        for i in range(-8000, 8400):
            UTM.from_latlon(i / 100.0, 0)
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, 84.1, 0)
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, 100, 0)

        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, 0, -300)
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, 0, -180.1)
        for i in range(-18000, 18000):
            UTM.from_latlon(0, i / 100.0)
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, 0, 180.1)
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, 0, 300)

        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, -100, -300)
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, 100, -300)
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, -100, 300)
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, 100, 300)

        # test forcing zone ranges
        # NYC should be zone 18T
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, 40.71435, -74.00597, 70, 'T')
        self.assertRaises(UTM.OutOfRangeError, UTM.from_latlon, 40.71435, -74.00597, 18, 'A')

    def test_to_latlon_range_checks(self):
        '''to_latlon should fail with out-of-bounds input'''

        # test easting range

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 0, 5000000, 32, 'U')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 99999, 5000000, 32, 'U')

        for i in range(100000, 999999, 1000):
            UTM.to_latlon(i, 5000000, 32, 'U')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 1000000, 5000000, 32, 'U')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 100000000000, 5000000, 32, 'U')

        # test northing range

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, -100000, 32, 'U')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, -1, 32, 'U')
        for i in range(10, 10000000, 1000):
            UTM.to_latlon(500000, i, 32, 'U')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, 10000001, 32, 'U')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, 50000000, 32, 'U')

        # test zone numbers

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, 5000000, 0, 'U')

        for i in range(1, 60):
            UTM.to_latlon(500000, 5000000, i, 'U')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, 5000000, 61, 'U')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, 5000000, 1000, 'U')

        # test zone letters

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, 5000000, 32, 'A')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, 5000000, 32, 'B')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, 5000000, 32, 'I')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, 5000000, 32, 'O')

        for i in range(ord('C'), ord('X')):
            i = chr(i)
            if i != 'I' and i != 'O':
                UTM.to_latlon(500000, 5000000, 32, i)

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, 5000000, 32, 'Y')

        self.assertRaises(
            UTM.OutOfRangeError, UTM.to_latlon, 500000, 5000000, 32, 'Z')


class Zone32V(unittest.TestCase):

    def assert_zone_equal(self, result, expected_number, expected_letter):
        self.assertEqual(result[2], expected_number)
        self.assertEqual(result[3].upper(), expected_letter.upper())

    def test_inside(self):
        self.assert_zone_equal(UTM.from_latlon(56, 3), 32, 'V')
        self.assert_zone_equal(UTM.from_latlon(56, 6), 32, 'V')
        self.assert_zone_equal(UTM.from_latlon(56, 9), 32, 'V')
        self.assert_zone_equal(UTM.from_latlon(56, 11.999999), 32, 'V')

        self.assert_zone_equal(UTM.from_latlon(60, 3), 32, 'V')
        self.assert_zone_equal(UTM.from_latlon(60, 6), 32, 'V')
        self.assert_zone_equal(UTM.from_latlon(60, 9), 32, 'V')
        self.assert_zone_equal(UTM.from_latlon(60, 11.999999), 32, 'V')

        self.assert_zone_equal(UTM.from_latlon(63.999999, 3), 32, 'V')
        self.assert_zone_equal(UTM.from_latlon(63.999999, 6), 32, 'V')
        self.assert_zone_equal(UTM.from_latlon(63.999999, 9), 32, 'V')
        self.assert_zone_equal(UTM.from_latlon(63.999999, 11.999999), 32, 'V')

    def test_left_of(self):
        self.assert_zone_equal(UTM.from_latlon(55.999999, 2.999999), 31, 'U')
        self.assert_zone_equal(UTM.from_latlon(56, 2.999999), 31, 'V')
        self.assert_zone_equal(UTM.from_latlon(60, 2.999999), 31, 'V')
        self.assert_zone_equal(UTM.from_latlon(63.999999, 2.999999), 31, 'V')
        self.assert_zone_equal(UTM.from_latlon(64, 2.999999), 31, 'W')

    def test_right_of(self):
        self.assert_zone_equal(UTM.from_latlon(55.999999, 12), 33, 'U')
        self.assert_zone_equal(UTM.from_latlon(56, 12), 33, 'V')
        self.assert_zone_equal(UTM.from_latlon(60, 12), 33, 'V')
        self.assert_zone_equal(UTM.from_latlon(63.999999, 12), 33, 'V')
        self.assert_zone_equal(UTM.from_latlon(64, 12), 33, 'W')

    def test_below(self):
        self.assert_zone_equal(UTM.from_latlon(55.999999, 3), 31, 'U')
        self.assert_zone_equal(UTM.from_latlon(55.999999, 6), 32, 'U')
        self.assert_zone_equal(UTM.from_latlon(55.999999, 9), 32, 'U')
        self.assert_zone_equal(UTM.from_latlon(55.999999, 11.999999), 32, 'U')
        self.assert_zone_equal(UTM.from_latlon(55.999999, 12), 33, 'U')

    def test_above(self):
        self.assert_zone_equal(UTM.from_latlon(64, 3), 31, 'W')
        self.assert_zone_equal(UTM.from_latlon(64, 6), 32, 'W')
        self.assert_zone_equal(UTM.from_latlon(64, 9), 32, 'W')
        self.assert_zone_equal(UTM.from_latlon(64, 11.999999), 32, 'W')
        self.assert_zone_equal(UTM.from_latlon(64, 12), 33, 'W')


class TestRightBoundaries(unittest.TestCase):

    def assert_zone_equal(self, result, expected_number):
        self.assertEqual(result[2], expected_number)

    def test_limits(self):
        self.assert_zone_equal(UTM.from_latlon(40, 0), 31)
        self.assert_zone_equal(UTM.from_latlon(40, 5.999999), 31)
        self.assert_zone_equal(UTM.from_latlon(40, 6), 32)

        self.assert_zone_equal(UTM.from_latlon(72, 0), 31)
        self.assert_zone_equal(UTM.from_latlon(72, 5.999999), 31)
        self.assert_zone_equal(UTM.from_latlon(72, 6), 31)
        self.assert_zone_equal(UTM.from_latlon(72, 8.999999), 31)
        self.assert_zone_equal(UTM.from_latlon(72, 9), 33)


class TestValidZones(unittest.TestCase):
    def test_valid_zones(self):
        # should not raise any exceptions
        UTM.check_valid_zone(10, 'C')
        UTM.check_valid_zone(10, 'X')
        UTM.check_valid_zone(10, 'p')
        UTM.check_valid_zone(10, 'q')
        UTM.check_valid_zone(20, 'X')
        UTM.check_valid_zone(1, 'X')
        UTM.check_valid_zone(60, 'e')

    def test_invalid_zones(self):
        self.assertRaises(UTM.OutOfRangeError, UTM.check_valid_zone, -100, 'C')
        self.assertRaises(UTM.OutOfRangeError, UTM.check_valid_zone, 20, 'I')
        self.assertRaises(UTM.OutOfRangeError, UTM.check_valid_zone, 20, 'O')
        self.assertRaises(UTM.OutOfRangeError, UTM.check_valid_zone, 0, 'O')


class TestForcingZones(unittest.TestCase):
    def assert_zone_equal(self, result, expected_number, expected_letter):
        self.assertEqual(result[2], expected_number)
        self.assertEqual(result[3].upper(), expected_letter.upper())

    def test_force_zone(self):
        # test forcing zone ranges
        # NYC should be zone 18T
        self.assert_zone_equal(UTM.from_latlon(40.71435, -74.00597, 19, 'T'), 19, 'T')
        self.assert_zone_equal(UTM.from_latlon(40.71435, -74.00597, 17, 'T'), 17, 'T')
        self.assert_zone_equal(UTM.from_latlon(40.71435, -74.00597, 18, 'u'), 18, 'U')
        self.assert_zone_equal(UTM.from_latlon(40.71435, -74.00597, 18, 'S'), 18, 'S')


class TestForcingAntiMeridian(unittest.TestCase):
    def assert_equal_lon(self, result, expected_lon):
        _, lon = UTM.to_latlon(*result[:4], strict=False)
        self.assertAlmostEqual(lon, expected_lon, 4)

    def test_force_east(self):
        # Force point just west of anti-meridian to east zone 1
        self.assert_equal_lon(
            UTM.from_latlon(0, 179.9, 1, 'N'), 179.9)

    def test_force_west(self):
        # Force point just east of anti-meridian to west zone 60
        self.assert_equal_lon(
            UTM.from_latlon(0, -179.9, 60, 'N'), -179.9)


if __name__ == '__main__':
    unittest.main()
