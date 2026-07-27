from setuptools import setup
from pathlib import Path
import re

this_directory = Path(__file__).parent

try:
    version_file_content = (this_directory / "utm/_version.py").read_text()
except:
    raise RuntimeError("Failed to read version file")

version_regex = re.compile(r"^__version__ = (['\"])(?P<version>.*)\1", re.M)
if (version_match := version_regex.search(version_file_content)):
    version = version_match.group("version")
else:
    raise RuntimeError("Failed to parse version")

long_description = (this_directory / "README.rst").read_text()

setup(
    name='utm',
    version=version,
    author='Tobias Bieniek',
    author_email='Tobias.Bieniek@gmx.de',
    url='https://github.com/Turbo87/utm',
    description='Bidirectional UTM-WGS84 converter for python',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords=['utm', 'wgs84', 'coordinate', 'converter'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    packages=['utm'],
    python_requires=">=3.10",
    scripts=['scripts/utm-converter'],
)
