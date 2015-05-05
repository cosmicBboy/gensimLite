try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A lightweight wrapper around Gensim',
    'author': 'Niels Bantilan',
    'url': 'https://github.com/cosmicBboy/gensimLite',
    'download_url': 'https://github.com/cosmicBboy/gensimLite',
    'author_email': 'niels.bantilan@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['gensimLite'],
    'scripts': [],
    'name': 'GensimLite'
}

setup(**config)