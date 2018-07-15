Blender distutils commands
==========================

This Python module adds a new command to
`distutils <https://docs.python.org/3/library/distutils.html>`_ to build `Blender <https://blender.org>`__ addons: ``bdist_blender_addon``. It also provides a simple mechanism to package extra modules not included with Blender's Python distribution within the addon.

Example
-------

See the `info_example_distutils <examples/info_example_distutils>`_ addon to see how this ``distutils`` module is used.

Installation
------------

Installing the ``blender.distutils`` module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The module is available on PiPy and installable with ``pip``.

.. code:: sh

    $ pip install blender.distutils

It is suggested to add a
`requirements.txt <examples/info_example_distutils/requirements.txt>`_ file to the Blender addon plugin that lists the module dependencies.

::

    # This is requirements.txt

    # This module adds the setup.py bdist_blender_addon command

    blender.distutils

    # This module is required by the addon, but not distributed with blender
    # bdist_blender_addon will ship it if with the addon
    # Dependencies to be included are listed in setup.cfg

    dateutils

Add a simple ``setup.py`` to the blender addon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``bdist_blender_addon`` is a ``distutils`` command. As such, a ``setup.py`` file is required. Addon name and version are defined by this file. I suggest using `bumpversion <https://github.com/peritus/bumpversion>`_ to keep ``setup.py``, ``bl_info`` and your git tags in sync.

The `setup.py <examples/info_example_distutils/setup.py>`_ for a blender addon is actually quite straightforward. The ``install_requires`` argument should only list the first-level dependencies needed by the addon: those may require their own dependencies. The actual modules to be shipped with the addon are cherry picked in ``setup.cfg``.

.. code:: python

    from setuptools import setup, find_packages

    setup(
        name='info_example_distutils',
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

        # Here are listed first level dependencies needed by the module. Themselves
        # may require dependencies. The actual modules to be shipped with the addon
        # are cherry picked in setup.cfg
        install_requires=['dateutils']
    )

Including third-party modules not shipped with blender
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``bdist_blender_addon`` command allows to include additional python
modules that are not shipped with Blender. These modules will be
included in the root folder of the addon. Currently an explicit list of
modules, including their dependencies, needs to be configured.

Cherry pick the modules to be shipped with the blender addon
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The modules to be included to the blender addon are listed as an option
of the ``[bdist_blender_addon]`` section in ``setup.cfg``. This list
includes all the modules and their dependencies.

::

    # This is in setup.cfg

    [bdist_blender_addon]

    # Here are listed the modules (and their dependencies) to be shipped
    # with the blender module. In this example the addon requires `dateutils`,
    # which in turns requires `dateutil`, `pytz` and `six`.
    addon_require = dateutil,dateutils,pytz,six

Include the additional modules folder in the addon code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The addon needs to explicitly register the path to third party modules.
During development, those modules will be in a virtual environment. When
the addon is installed in production, those modules will be at the root
of the addon folder.

.. code:: python

    import pathlib
    import os
    import site
    import sys


    def third_party_modules_sitedir():
        # If we are in a VIRTUAL_ENV, while developing for example, we want the
        # addon to hit the modules installed in the virtual environment
        if 'VIRTUAL_ENV' in os.environ:
            env = pathlib.Path(os.environ['VIRTUAL_ENV'])
            v = sys.version_info
            path = env / 'lib/python{}.{}/site-packages'.format(v.major, v.minor)

        # However outside of a virtual environment, the additionnal modules not
        # shipped with Blender are expected to be found in the root folder of
        # the addon
        else:
            path = pathlib.Path(__file__).parent

        return str(path.resolve())

    # The additionnal modules location (virtual env or addon folder) is
    # appended here
    site.addsitedir(third_party_modules_sitedir())

    # This module is not part of the standard blender distribution
    # It is shipped alongside the plugin when `python setup.py bdist_blender_addon`
    import dateutils

Build the module
~~~~~~~~~~~~~~~~

The ``bdist_blender_addon`` command will copy the addon code, copy the
additional modules over, clean unneeded files (like the ``*.pyc``
bytecode files) and package them all in a versioned zip archive under
the ``dist`` folder.

.. code:: bash

    $ python setup.py bdist_blender_addon
    running bdist_blender_addon
    running build
    running build_py
    creating build/lib/info_example_distutils
    copying info_example_distutils/__init__.py -> build/lib/info_example_distutils
    creating build/lib/info_example_distutils/dateutil
    [long list of files being copied or added to the addon zip archive]

    $ ls dist/
    info_example_distutils-v1.0.0.zip
