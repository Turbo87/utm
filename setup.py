from distutils.core import setup

setup(
    name='utm',
    version='0.4.0',
    author='Tobias Bieniek',
    author_email='Tobias.Bieniek@gmx.de',
    url='https://github.com/Turbo87/utm',
    description='Bidirectional UTM-WGS84 converter for python',
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
    scripts=['scripts/utm-converter'],
)
