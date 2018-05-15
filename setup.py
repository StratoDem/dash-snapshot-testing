"""
StratoDem Analytics : setup
Principal Author(s) : Eric Linden
Secondary Author(s) :
Description :

Notes :

March 27, 2018
"""

from setuptools import setup

setup(
    name='dash-snapshot-testing',
    version='1.2.0',
    author='Michael Clawar, Eric Linden',
    author_email='tech@stratodem.com',
    packages=['snapshot_test'],
    license='MIT',
    description='Dash snapshot testing package',
    url='https://github.com/StratoDem/dash-snapshot-testing',
    keywords='dash snapshot plotly testing unittest',
    python_requires='>=3',
    install_requires=[
        'dash>=0.19.0',
        'plotly>=2.2.3',
    ])
