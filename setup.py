from setuptools import setup, find_packages

setup(
    name='blender.distutils',
    version='1.0.5',
    description='Blender distutils addon',
    long_description=open('README.rst').read(),
    url='https://github.com/charlesfleche/blender.distutils',
    author='Charles Flèche',
    author_email='charles.fleche@free.fr',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    packages=find_packages(),
    keywords='distutils blender',
    entry_points={
      'distutils.commands': [
          'bdist_blender_addon=blender.distutils.bdist_blender_addon:bdist_blender_addon'
          ]
    }
)
