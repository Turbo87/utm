import utm as UTM
import unittest


class KnownValues(unittest.TestCase):
    known_values = [
        # Aachen, Germany
        ((50.77535, 6.08389), (294409, 5628898, 32, 'U')),
        # New York, USA
        ((40.71435, -74.00597), (583960, 4507523, 18, 'T')),
        # Wellington, New Zealand
        ((-41.28646, 174.77624), (313784, 5427057, 60, 'G')),
        # Capetown, South Africe
        ((-33.92487, 18.42406), (261878, 6243186, 34, 'H')),
        # Mendoza, Argentina
        ((-32.89018, -68.84405), (514586, 6360877, 19, 'H')),
        # Fairbanks, Alaska, USA
        ((64.83778, -147.71639), (466013, 7190568, 6, 'W')),
        # Ben Nevis, Scotland, UK
        ((56.79680, -5.00601), (377486, 6296562, 30, 'V')),
    ]

    def test_from_latlon(self):
        '''to_latlon should give known result with known input'''
        for latlon, utm in self.known_values:
            result = UTM.from_latlon(*latlon)
            self.assert_utm_equal(utm, result)

    def test_to_latlon(self):
        '''to_latlon should give known result with known input'''
        for latlon, utm in self.known_values:
            result = UTM.to_latlon(*utm)
            self.assert_latlon_equal(latlon, result)

    def assert_utm_equal(self, a, b):
        self.assertAlmostEqual(a[0], b[0], -1)
        self.assertAlmostEqual(a[1], b[1], -1)
        self.assertEqual(a[2], b[2])
        self.assertEqual(a[3], b[3])

    def assert_latlon_equal(self, a, b):
        self.assertAlmostEqual(a[0], b[0], 3)
        self.assertAlmostEqual(a[1], b[1], 3)

if __name__ == '__main__':
    unittest.main()
