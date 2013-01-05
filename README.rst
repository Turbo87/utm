utm
===

.. image:: https://travis-ci.org/Turbo87/utm.png

Bidirectional UTM-WGS84 converter for python

Usage
-----

::

  import utm

Convert a (latitude, longitude) tuple into an UTM coordinate::

  utm.from_latlon(51.2, 7.5)
  >>> (395201, 5673135, 32, 'U')

Convert an UTM coordinate into a (latitude, longitude) tuple::

  utm.to_latlon(340000, 5710000, 32, 'U')
  >>> (51.51852098408468, 6.693872395145327)

Speed
-----

The library has been compared to the more generic pyproj library by running the
unit test suite through pyproj instead of utm. These are the results:

* with pyproj (without projection cache): 4.0 - 4.5 sec
* with pyproj (with projection cache): 0.9 - 1.0 sec
* with utm: 0.4 - 0.5 sec

Authors
-------

* Tobias Bieniek <Tobias.Bieniek@gmx.de>

License
-------

Copyright (C) 2012 Tobias Bieniek <Tobias.Bieniek@gmx.de>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
