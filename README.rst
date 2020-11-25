utm
===

Bidirectional UTM-WGS84 converter for python

Usage
-----

.. code-block:: python

  >>> import utm

Latitude/Longitude to UTM
^^^^^^^^^^^^^^^^^^^^^^^^^

Convert a ``(latitude, longitude)`` tuple into an UTM coordinate:

.. code-block:: python

  >>> utm.from_latlon(51.2, 7.5)
  (395201.3103811303, 5673135.241182375, 32, 'U')

The syntax is ``utm.from_latlon(LATITUDE, LONGITUDE)``.

The return has the form ``(EASTING, NORTHING, ZONE_NUMBER, ZONE_LETTER)``.

You can also use NumPy arrays for ``LATITUDE`` and ``LONGITUDE``. In the
result ``EASTING`` and ``NORTHING`` will have the same shape.  ``ZONE_NUMBER``
and ``ZONE_LETTER`` are scalars and will be calculated for the first point of
the input. All other points will be set into the same UTM zone.  Therefore
it's a good idea to make sure all points are near each other.

.. code-block:: python

  >>> utm.from_latlon(np.array([51.2, 49.0]), np.array([7.5, 8.4]))
  (array([395201.31038113, 456114.59586214]),
   array([5673135.24118237, 5427629.20426126]),
   32,
   'U')


UTM to Latitude/Longitude
^^^^^^^^^^^^^^^^^^^^^^^^^

Convert an UTM coordinate into a ``(latitude, longitude)`` tuple:

.. code-block:: python

  >>> utm.to_latlon(340000, 5710000, 32, 'U')
  (51.51852098408468, 6.693872395145327)

The syntax is ``utm.to_latlon(EASTING, NORTHING, ZONE_NUMBER, ZONE_LETTER)``.

The return has the form ``(LATITUDE, LONGITUDE)``.

You can also use NumPy arrays for ``EASTING`` and ``NORTHING``. In the result
``LATITUDE`` and ``LONGITUDE`` will have the same shape.  ``ZONE_NUMBER`` and
``ZONE_LETTER`` are scalars.

.. code-block:: python

    >>> utm.to_latlon(np.array([395200, 456100]), np.array([5673100, 5427600]), 32, 'U')
    (array([51.19968297, 48.99973627]), array([7.49999141, 8.3998036 ]))


Since the zone letter is not strictly needed for the conversion you may also
the ``northern`` parameter instead, which is a named parameter and can be set
to either ``True`` or ``False``. Have a look at the unit tests to see how it
can be used.

The UTM coordinate system is explained on
`this <https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system>`_
Wikipedia page.

Speed
-----

The library has been compared to the more generic pyproj library by running
the unit test suite through pyproj instead of utm. These are the results:

* with pyproj (without projection cache): 4.0 - 4.5 sec
* with pyproj (with projection cache): 0.9 - 1.0 sec
* with utm: 0.4 - 0.5 sec

NumPy arrays bring another speed improvement (on a different computer than the
previous test). Using ``utm.from_latlon(x, y)`` to convert one million points:

* one million calls (``x`` and ``y`` are floats): 1,000,000 × 90µs = 90s
* one call (``x`` and ``y`` are numpy arrays of one million points): 0.26s

Development
-----------

Create a new ``virtualenv`` and install the library via ``pip install -e .``.
After that install the ``pytest`` package via ``pip install pytest`` and run
the unit test suite by calling ``pytest``.

Changelog
---------

see `CHANGELOG.rst <CHANGELOG.rst>`_ file

Authors
-------

* Bart van Andel <bavanandel@gmail.com>
* Tobias Bieniek <Tobias.Bieniek@gmx.de>
* Torstein I. Bø

License
-------

Copyright (C) 2012 Tobias Bieniek <Tobias.Bieniek@gmx.de>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
