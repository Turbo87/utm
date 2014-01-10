import utm as UTM
import unittest


class UTMTestCase(unittest.TestCase):
    def assert_utm_equal(self, a, b):
        self.assertAlmostEqual(a[0], b[0], 0)
        self.assertAlmostEqual(a[1], b[1], 0)
        self.assertEqual(a[2], b[2])
        self.assertEqual(a[3].upper(), b[3].upper())

    def assert_latlon_equal(self, a, b):
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
    ]

    def test_from_latlon(self):
        '''from_latlon should give known result with known input'''
        for latlon, utm, _ in self.known_values:
            result = UTM.from_latlon(*latlon)
            self.assert_utm_equal(utm, result)

    def test_to_latlon(self):
        '''to_latlon should give known result with known input'''
        for latlon, utm, utm_kw in self.known_values:
            result = UTM.to_latlon(*utm)
            self.assert_latlon_equal(latlon, result)

            result = UTM.to_latlon(*utm[0:3], **utm_kw)
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

if __name__ == '__main__':
    unittest.main()
