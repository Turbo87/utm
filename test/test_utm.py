from __future__ import division

import utm as UTM

import functools
import pytest

try:
    import numpy as np

    use_numpy = True
except ImportError:
    use_numpy = False


def assert_utm_equal(a, b):
    if use_numpy and isinstance(b[0], np.ndarray):
        assert np.allclose(a[0], b[0])
        assert np.allclose(a[1], b[1])
    else:
        assert a[0] == pytest.approx(b[0], abs=1)
        assert a[1] == pytest.approx(b[1], abs=1)
    assert a[2] == b[2]
    assert a[3].upper() == b[3].upper()


def assert_latlon_equal(a, b):
    if use_numpy and isinstance(b[0], np.ndarray):
        def longitude_close(lon1, lon2, rtol=1e-4, atol=1e-4):
            # Check if longitudes are close after normalization
            is_close = functools.partial(np.isclose, lon1, rtol=rtol, atol=atol)
            return is_close(lon2) or is_close(lon2 - 360) or is_close(lon2 + 360)

        assert np.allclose(a[0], b[0], rtol=1e-4, atol=1e-4)
        if isinstance(a[1], np.ndarray):
            assert all(longitude_close(lon_a, lon_b) for lon_a, lon_b in zip(a[1].flatten(), b[1].flatten()))
        else:
            assert all(longitude_close(a[1], lon_b) for lon_b in b[1].flatten())
    else:
        assert a[0] == pytest.approx(b[0], 4)
        assert (
            a[1] == pytest.approx(b[1], 4) or
            a[1] == pytest.approx(b[1] - 360, 4) or
            a[1] == pytest.approx(b[1] + 360, 4)
        )


known_values = [
    # Aachen, Germany
    (
        (50.77535, 6.08389),
        (294409, 5628898, 32, "U"),
        {"northern": True},
    ),
    # New York, USA
    (
        (40.71435, -74.00597),
        (583960, 4507523, 18, "T"),
        {"northern": True},
    ),
    # Wellington, New Zealand
    (
        (-41.28646, 174.77624),
        (313784, 5427057, 60, "G"),
        {"northern": False},
    ),
    # Capetown, South Africa
    (
        (-33.92487, 18.42406),
        (261878, 6243186, 34, "H"),
        {"northern": False},
    ),
    # Mendoza, Argentina
    (
        (-32.89018, -68.84405),
        (514586, 6360877, 19, "h"),
        {"northern": False},
    ),
    # Fairbanks, Alaska, USA
    (
        (64.83778, -147.71639),
        (466013, 7190568, 6, "W"),
        {"northern": True},
    ),
    # Ben Nevis, Scotland, UK
    (
        (56.79680, -5.00601),
        (377486, 6296562, 30, "V"),
        {"northern": True},
    ),
    # Bergen, Norway
    (
        (60.38952, 5.320675),
        (297264, 6700454, 32, "V"),
        {"northern": True},
    ),
    # Alkefjellet, Spitsbergen, Svalbard
    (
        (79.45574, 18.76338),
        (576830, 8823320, 33, "X"),
        {"northern": True},
    ),
    # Latitude 84
    (
        (84, -5.00601),
        (476594, 9328501, 30, "X"),
        {"northern": True},
    ),
    # East-most point on the Equator
    (
        (0, 180),
        (166021, 0, 1, "N"),
        {"northern": True},
    ),
    # West-most point on the Equator
    (
        (0, -180),
        (166021, 0, 1, "N"),
        {"northern": True}
    ),
]


@pytest.mark.parametrize("latlon, utm, utm_kw", known_values)
def test_from_latlon(latlon, utm, utm_kw):
    """from_latlon should give known result with known input"""
    result = UTM.from_latlon(*latlon)
    assert_utm_equal(utm, result)


@pytest.mark.skipif(not use_numpy, reason="numpy not installed")
@pytest.mark.parametrize("latlon, utm, utm_kw", known_values)
def test_from_latlon_numpy(latlon, utm, utm_kw):
    result = UTM.from_latlon(*[np.array([x]) for x in latlon])
    assert_utm_equal(utm, result)


@pytest.mark.skipif(not use_numpy, reason="numpy not installed")
def test_from_latlon_numpy_static():
    lats = np.array([0.0, 3.0, 6.0])
    lons = np.array([0.0, 1.0, 3.4])
    result = UTM.from_latlon(lats, lons)
    assert_utm_equal(
        (
            np.array(
                [166021.44317933032, 277707.83075574087, 544268.12794623]
            ),
            np.array([0.0, 331796.29167519242, 663220.7198366751]),
            31,
            "N",
        ),
        result,
    )


@pytest.mark.parametrize("latlon, utm, utm_kw", known_values)
def test_to_latlon(latlon, utm, utm_kw):
    """to_latlon should give known result with known input"""
    result = UTM.to_latlon(*utm)
    assert_latlon_equal(latlon, result)

    result = UTM.to_latlon(*utm[0:3], **utm_kw)
    assert_latlon_equal(latlon, result)


@pytest.mark.skipif(not use_numpy, reason="numpy not installed")
@pytest.mark.parametrize("latlon, utm, utm_kw", known_values)
def test_to_latlon_numpy(latlon, utm, utm_kw):
    utm = [np.array([x]) for x in utm[:2]] + list(utm[2:])
    result = UTM.to_latlon(*utm)
    assert_latlon_equal(latlon, result)


@pytest.mark.skipif(not use_numpy, reason="numpy not installed")
def test_to_latlon_numpy_static():
    result = UTM.to_latlon(
        np.array([166021.44317933032, 277707.83075574087, 544268.12794623]),
        np.array([0.0, 331796.29167519242, 663220.7198366751]),
        31,
        northern=True,
    )
    assert_latlon_equal(
        (np.array([0.0, 3.0, 6.0]), np.array([0.0, 1.0, 3.4])), result
    )


def test_from_latlon_range_ok():
    """from_latlon should work for good values"""
    for i in range(-8000, 8400):
        assert UTM.from_latlon(i / 100, 0)
    for i in range(-18000, 18000):
        assert UTM.from_latlon(0, i / 100)


@pytest.mark.parametrize(
    "lat, lon",
    [
        (-100, 0),
        (-80.1, 0),
        (84.1, 0),
        (100, 0),
        (0, -300),
        (0, -180.1),
        (0, 180.1),
        (0, 300),
        (-100, -300),
        (100, -300),
        (-100, 300),
        (100, 300),
    ],
)
def test_from_latlon_range_fails(lat, lon):
    """from_latlon should fail with out-of-bounds input"""
    with pytest.raises(UTM.OutOfRangeError):
        UTM.from_latlon(lat, lon)


@pytest.mark.parametrize(
    "lat, lon, force_zone_number, force_zone_letter",
    [(40.71435, -74.00597, 70, "T"), (40.71435, -74.00597, 18, "A")],
)
def test_from_latlon_range_forced_fails(
    lat, lon, force_zone_number, force_zone_letter
):
    """from_latlon should fail with out-of-bounds input"""
    with pytest.raises(UTM.OutOfRangeError):
        UTM.from_latlon(lat, lon, force_zone_number, force_zone_letter)


def test_to_latlon_range_ok():
    """to_latlon should work for good values"""
    for i in range(100000, 999999, 1000):
        assert UTM.to_latlon(i, 5000000, 32, "U")
    for i in range(10, 10000000, 1000):
        assert UTM.to_latlon(500000, i, 32, "U")
    for i in range(1, 60):
        assert UTM.to_latlon(500000, 5000000, i, "U")
    for i in range(ord("C"), ord("X")):
        i = chr(i)
        if i != "I" and i != "O":
            UTM.to_latlon(500000, 5000000, 32, i)


@pytest.mark.parametrize(
    "easting, northing, zone_number, zone_letter",
    [
        (0, 5000000, 32, "U"),
        (99999, 5000000, 32, "U"),
        (1000000, 5000000, 32, "U"),
        (100000000000, 5000000, 32, "U"),
        (500000, -100000, 32, "U"),
        (500000, -1, 32, "U"),
        (500000, 10000001, 32, "U"),
        (500000, 50000000, 32, "U"),
        (500000, 5000000, 0, "U"),
        (500000, 5000000, 61, "U"),
        (500000, 5000000, 1000, "U"),
        (500000, 5000000, 32, "A"),
        (500000, 5000000, 32, "B"),
        (500000, 5000000, 32, "I"),
        (500000, 5000000, 32, "O"),
        (500000, 5000000, 32, "Y"),
        (500000, 5000000, 32, "Z"),
    ],
)
def test_to_latlon_range_checks(easting, northing, zone_number, zone_letter):
    """to_latlon should fail with out-of-bounds input"""
    with pytest.raises(UTM.OutOfRangeError):
        UTM.to_latlon(0, 5000000, 32, "U")


@pytest.mark.parametrize(
    "lat, lon, expected_number, expected_letter",
    [
        # test inside:
        (56, 3, 32, "V"),
        (56, 6, 32, "V"),
        (56, 9, 32, "V"),
        (56, 11.999999, 32, "V"),
        (60, 3, 32, "V"),
        (60, 6, 32, "V"),
        (60, 9, 32, "V"),
        (60, 11.999999, 32, "V"),
        (63.999999, 3, 32, "V"),
        (63.999999, 6, 32, "V"),
        (63.999999, 9, 32, "V"),
        (63.999999, 11.999999, 32, "V"),
        # test left of:
        (55.999999, 2.999999, 31, "U"),
        (56, 2.999999, 31, "V"),
        (60, 2.999999, 31, "V"),
        (63.999999, 2.999999, 31, "V"),
        (64, 2.999999, 31, "W"),
        # test right of:
        (55.999999, 12, 33, "U"),
        (56, 12, 33, "V"),
        (60, 12, 33, "V"),
        (63.999999, 12, 33, "V"),
        (64, 12, 33, "W"),
        # test below:
        (55.999999, 3, 31, "U"),
        (55.999999, 6, 32, "U"),
        (55.999999, 9, 32, "U"),
        (55.999999, 11.999999, 32, "U"),
        (55.999999, 12, 33, "U"),
        # test above:
        (64, 3, 31, "W"),
        (64, 6, 32, "W"),
        (64, 9, 32, "W"),
        (64, 11.999999, 32, "W"),
        (64, 12, 33, "W"),
        # test edge:
        (0, 180, 1, "N"),
        (0, -180, 1, "N"),
        (84, 180, 1, "X"),
        (84, -180, 1, "X"),
    ],
)
def test_from_latlon_zones(lat, lon, expected_number, expected_letter):
    result = UTM.from_latlon(lat, lon)
    assert result[2] == expected_number
    assert result[3].upper() == expected_letter.upper()


@pytest.mark.parametrize(
    "lat, lon, expected_number",
    [
        (40, 0, 31),
        (40, 5.999999, 31),
        (40, 6, 32),
        (72, 0, 31),
        (72, 5.999999, 31),
        (72, 6, 31),
        (72, 8.999999, 31),
        (72, 9, 33),
    ],
)
def test_limits(lat, lon, expected_number):
    assert UTM.from_latlon(lat, lon)[2] == expected_number


@pytest.mark.parametrize(
    "zone_number, zone_letter",
    [
        (10, "C"),
        (10, "X"),
        (10, "p"),
        (10, "q"),
        (20, "X"),
        (1, "X"),
        (60, "e"),
    ],
)
def test_valid_zones(zone_number, zone_letter):
    # should not raise any exceptions
    assert UTM.check_valid_zone(zone_number, zone_letter) is None


@pytest.mark.parametrize(
    "zone_number, zone_letter", [(-100, "C"), (20, "I"), (20, "O"), (0, "O")]
)
def test_invalid_zones(zone_number, zone_letter):
    with pytest.raises(UTM.OutOfRangeError):
        UTM.check_valid_zone(zone_number, zone_letter)


@pytest.mark.parametrize(
    "lat, lon, utm, utm_kw, expected_number, expected_letter",
    [
        (40.71435, -74.00597, 19, "T", 19, "T"),
        (40.71435, -74.00597, 17, "T", 17, "T"),
        (40.71435, -74.00597, 18, "u", 18, "U"),
        (40.71435, -74.00597, 18, "S", 18, "S"),
    ],
)
def test_force_zone(lat, lon, utm, utm_kw, expected_number, expected_letter):
    # test forcing zone ranges
    # NYC should be zone 18T
    result = UTM.from_latlon(lat, lon, utm, utm_kw)
    assert result[2] == expected_number
    assert result[3].upper() == expected_letter.upper()


def assert_equal_lat(result, expected_lat, northern=None):
    args = result[:3] if northern else result[:4]
    lat, _ = UTM.to_latlon(*args, northern=northern, strict=False)
    assert lat == pytest.approx(expected_lat, abs=0.001)


def assert_equal_lon(result, expected_lon):
    _, lon = UTM.to_latlon(*result[:4], strict=False)
    assert lon == pytest.approx(expected_lon, abs=0.001)


def test_force_east():
    # Force point just west of anti-meridian to east zone 1
    assert_equal_lon(UTM.from_latlon(0, 179.9, 1, "N"), 179.9)


def test_force_west():
    # Force point just east of anti-meridian to west zone 60
    assert_equal_lon(UTM.from_latlon(0, -179.9, 60, "N"), -179.9)


def test_force_north():
    # Force southern point to northern zone letter
    assert_equal_lat(UTM.from_latlon(-0.1, 0, 31, 'N'), -0.1)

    # Again, using force northern
    assert_equal_lat(
        UTM.from_latlon(-0.1, 0, 31, force_northern=True), -0.1, northern=True)


def test_force_south():
    # Force northern point to southern zone letter
    assert_equal_lat(UTM.from_latlon(0.1, 0, 31, 'M'), 0.1)

    # Again, using force northern as False
    assert_equal_lat(
        UTM.from_latlon(0.1, 0, 31, force_northern=True), 0.1, northern=True)


@pytest.mark.skipif(not use_numpy, reason="numpy not installed")
def test_no_force_numpy():
    # Point above and below equator
    lats = np.array([-0.1, 0.1])
    with pytest.raises(ValueError,
                       match="latitudes must all have the same sign"):
      UTM.from_latlon(lats, np.array([0, 0]))


@pytest.mark.skipif(not use_numpy, reason="numpy not installed")
@pytest.mark.parametrize("zone", ('N', 'M'))
def test_force_numpy(zone):
    # Point above and below equator
    lats = np.array([-0.1, 0.1])

    result = UTM.from_latlon(
        lats, np.array([0, 0]), force_zone_letter=zone)
    for expected_lat, easting, northing in zip(lats, *result[:2]):
        assert_equal_lat(
            (easting, northing, result[2], result[3]), expected_lat)


@pytest.mark.skipif(not use_numpy, reason="numpy not installed")
@pytest.mark.parametrize("force_northern", (True, False))
def test_force_numpy_force_northern_true(force_northern):
    # Point above and below equator
    lats = np.array([-0.1, 0.1])

    result = UTM.from_latlon(
        lats, np.array([0, 0]), force_northern=force_northern)
    for expected_lat, easting, northing in zip(lats, *result[:2]):
        assert_equal_lat(
            (easting, northing, result[2], result[3]), expected_lat,
            northern=force_northern)


def test_force_both():
    # Force both letter and northern not allowed
    with pytest.raises(ValueError, match="set either force_zone_letter or "
                                         "force_northern, but not both"):
        UTM.from_latlon(-0.1, 0, 31, 'N', True)


def test_version():
    assert isinstance(UTM.__version__, str) and "." in UTM.__version__


@pytest.mark.skipif(not use_numpy, reason="numpy not installed")
def test_numpy_args_not_modified():
    TEST_EASTING = 387358.0
    TEST_NORTHING = 8145567.0
    easting = np.array(TEST_EASTING)
    northing = np.array(TEST_NORTHING)
    zone = 55
    letter = "K"
    UTM.to_latlon(easting, northing, zone, letter)
    assert easting == TEST_EASTING
    assert northing == TEST_NORTHING


@pytest.mark.parametrize(
    "zone_number, expected_lon",
    [
        (1,  -177),
        (12, -111),
        (16,  -87),
        (31,    3),
        (37,   39),
    ],
)
def test_zone_number_to_central_longitude(zone_number, expected_lon):
    lon = UTM.zone_number_to_central_longitude(zone_number)
    assert lon == expected_lon


@pytest.mark.parametrize(
    "zone_letter, expected_lat",
    [
        ("X",  78),
        ("C", -76),
        ("E", -60),
        ("F", -52),
        ("Q",  20),
    ],
)
def test_zone_letter_to_central_latitude(zone_letter, expected_lat):
    lat = UTM.zone_letter_to_central_latitude(zone_letter)
    assert lat == expected_lat
