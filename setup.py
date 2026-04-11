from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'icosphere',
    version = '0.2.0',
    description = 'Creates a geodesic icosahedron given a subdivision frequency.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/vedranaa/icosphere',
    author = 'Vedrana Andersen Dahl',
    author_email = 'vand@dtu.dk',
    license ='lgpl-2.1',
    py_modules = ['icosphere']
    )