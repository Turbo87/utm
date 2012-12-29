import math

__all__ = ['to_latlon', 'from_latlon']

K0 = 0.9996

E = 0.00669438
E_P2 = E / (1.0 - E)

R = 6378137

ZONE_LETTERS = [
    (84, None), (72, 'X'), (64, 'W'), (56, 'V'), (48, 'U'), (40, 'T'),
    (32, 'S'), (24, 'R'), (16, 'Q'), (8, 'P'), (0, 'N'), (-8, 'M'), (-16, 'L'),
    (-24, 'K'), (-32, 'J'), (-40, 'H'), (-48, 'G'), (-56, 'F'), (-64, 'E'),
    (-72, 'D'), (-80, 'C')
]


def to_latlon(easting, northing, zone_number, zone_letter):
    x = easting - 500000
    y = northing

    if zone_letter < 'N':
        y -= 10000000

    m = y / K0
    mu = m / (R * (1 - E / 4 - 3 * E**2 / 64 - 5 * E**3 / 256))

    e = (1 - math.sqrt(1 - E)) / (1 + math.sqrt(1 - E))

    p_rad = (mu +
             (3 * e / 2 - 27 * e**3 / 32) * math.sin(2 * mu) +
             (21 * e**3 / 16 - 55 * e**4 / 32) * math.sin(4 * mu) +
             (151 * e**3 / 96) * math.sin(6 * mu))

    p_sin = math.sin(p_rad)
    p_cos = math.cos(p_rad)
    p_tan = p_sin / p_cos

    n = R / math.sqrt(1 - E * p_sin**2)
    c = e * p_cos**2
    r = R * (1 - E) / (1 - E * p_sin**2)**1.5

    d = x / (n * K0)

    latitude = (p_rad - (n * p_tan / r) *
                (d**2 / 2 -
                 d**4 / 24 * (5 + 3 * p_tan**2 + 10 * c - 4 * c**2 - 9 * E_P2)) +
                 d**6 / 720 * (61 + 90 * p_tan**2 + 298 * c + 45 * p_tan**4 - 252 * E_P2 - 3 * c**2))

    longitude = (d -
                 d**3 / 6 * (1 + 2 * p_tan**2 + c) +
                 d**5 / 120 * (5 - 2 * c + 28 * p_tan**2 - 3 * c**2 + 8 * E_P2 + 24 * p_tan**4)) / p_cos

    return (math.degrees(latitude),
            math.degrees(longitude) + zone_number_to_central_longitude(zone_number))


def from_latlon(latitude, longitude):
    lat_rad = math.radians(latitude)
    lat_sin = math.sin(lat_rad)
    lat_cos = math.cos(lat_rad)
    lat_tan = lat_sin / lat_cos

    lon_rad = math.radians(longitude)

    zone_number = latlon_to_zone_number(latitude, longitude)
    central_lon = zone_number_to_central_longitude(zone_number)
    central_lon_rad = math.radians(central_lon)

    zone_letter = latitude_to_zone_letter(latitude)

    n = R / math.sqrt(1 - E * lat_sin**2)
    c = E_P2 * lat_cos**2

    a = lat_cos * (lon_rad - central_lon_rad)

    m = R * ((1 - E / 4 - 3 * E**2 / 64 - 5 * E**3 / 256) * lat_rad -
             (3 * E / 8 + 3 * E**2 / 32 + 45 * E**3 / 1024) * math.sin(2 * lat_rad) +
             (15 * E**2 / 256 + 45 * E**3 / 1024) * math.sin(4 * lat_rad) -
             (35 * E**3 / 3072) * math.sin(6 * lat_rad))

    easting = K0 * n * (a +
                        a**3 / 6 * (1 - lat_tan**2 + c) +
                        a**5 / 120 * (5 - 18 * lat_tan**2 + lat_tan**4 + 72 * c - 58 * E_P2)) + 500000

    northing = K0 * (m + n * lat_tan * (a**2 / 2 +
                                        a**4 / 24 * (5 - lat_tan**2 + 9 * c + 4 * c**2) +
                                        a**6 / 720 * (61 - 58 * lat_tan**2 + lat_tan**4 + 600 * c - 330 * E_P2)))

    if latitude < 0:
        northing += 10000000

    return int(easting), int(northing), zone_number, zone_letter


def latitude_to_zone_letter(latitude):
    for lat_min, zone_letter in ZONE_LETTERS:
        if latitude >= lat_min:
            return zone_letter

    return None


def latlon_to_zone_number(latitude, longitude):
    if 56 <= latitude <= 64 and 3 <= longitude <= 12:
        return 32

    if 72 <= latitude <= 84 and longitude >= 0:
        if longitude <= 9:
            return 31
        elif longitude <= 21:
            return 33
        elif longitude <= 33:
            return 35
        elif longitude <= 42:
            return 37

    return int((longitude + 180) / 6) + 1


def zone_number_to_central_longitude(zone_number):
    return (zone_number - 1) * 6 - 180 + 3
