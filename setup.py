from setuptools import setup

setup(
    name='blender.distutils',
    version='1.0.0',
    description='Blender distutils addon',
    long_description=open('README.md').read(),
    url='https://github.com/charlesfleche/blender.distutils',
    author='Charles Flèche',
    author_email='charles.fleche@free.fr',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop', # Fix that
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='distutils blender'
)
