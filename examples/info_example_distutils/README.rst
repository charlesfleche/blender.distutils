Blender distutils example
=========================

This example shows how to write the `setup.py <https://python.org>`_ of a
Blender addon using the ``blender.distutils`` module. It requires a
Python module not shipped with Blender: ``dateutils``.

The addon itself adds a new Blender operator
``export_scene.example_distutils`` which displays a simple message (the
current day of the year) when activated.
