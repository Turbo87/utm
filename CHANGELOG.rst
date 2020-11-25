Changelog
=========

v0.7.0
------

* Add support for Python 3.7, 3.8 and 3.9 (#54)
* Drop support for Python 3.4


v0.6.0
------

* Drop support for Python 2.6 and 3.3 (#53)
* Improve documentation (#50)
* Fix issue near anti-meridian when forcing zones (#47)
* Improve `to_latlon()` accuracy (#49)


v0.5.0
------

* Add zone checking when forced
* Implement numpy support
* Fix UTM zones boundaries


v0.4.2
------

* added optional ``strict`` option to ``to_latlon()``
* added ``LICENSE`` file


v0.4.1
------

* fixed missing zone letter for latitude 84 deg.
* fixed ``from_lat_lon()`` longitude error message
* fixed zone numbers for 32V and related regions


v0.4.0
------

* added optional ``force_zone_number`` parameter to ``from_latlon()`` (`#8 <https://github.com/Turbo87/utm/pull/8>`_)
* fixed minor precision error (`#9 <https://github.com/Turbo87/utm/pull/9>`_)


v0.3.1
------

* added optional ``northern`` parameter to ``to_latlon()``
* use `py.test <http://pytest.org/latest/>`_ instead of `nosetest`


v0.3.0
------

* return floats from ``from_latlon()``


v0.2.5
------

* more unit tests


v0.2.4
------

* performance improvements


v0.2.3
------

* `TravisCI <https://travis-ci.org/Turbo87/utm>`_ support


v0.2.2
------

* support for lowercase zone letters
* documentation fixes
* raise ``OutOfRangeError`` exception for bad input parameters


v0.2.1
------

* install utm-converter properly


v0.2.0
------

* added unit tests


v0.1.0
------

* initial release
