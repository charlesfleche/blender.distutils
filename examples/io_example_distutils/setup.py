from setuptools import setup, find_packages

setup(
    name='io_example_distutils',
    version='1.0.0',
    description='Blender example distutils',
    long_description=open('README.md').read(),
    url='https://github.com/charlesfleche/blender.distutils/io_example_distutils',
    author='Charles Flèche',
    author_email='charles.fleche@free.fr',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    packages=find_packages(),
    keywords='blender',
    install_requires=['dateutils']
)
