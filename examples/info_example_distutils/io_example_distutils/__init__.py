import datetime
import bpy
import pathlib
import os
import site
import sys

# Register path to third-party modules according to VIRTUAL_ENV if defined
def sitedir():
    if 'VIRTUAL_ENV' in os.environ:
        env = pathlib.Path(os.environ['VIRTUAL_ENV'])
        v = sys.version_info
        path = env / 'lib/python{}.{}/site-packages'.format(v.major, v.minor)
    else:
        path = pathlib.Path(__file__).parent
    return str(path.resolve())
site.addsitedir(sitedir())

# This module is not part of the standard blender distribution
# It is shipped alongside the plugin when `python setup.py bdist_blender_addon`
import dateutils

bl_info = {
    'name': 'Example distutils',
    'author': "Charles Flèche (charles.fleche@free.fr)",
    'version': (1, 0, 0),
    'blender': (2, 76, 0),
    'location': "File > Export",
    'description': "Blender distutils example",
    'category': 'Import-Export',
}

class ExampleDistutils(bpy.types.Operator):
    bl_idname = 'info.example_distutils'
    bl_label = 'Example distutils'

    def execute(self, context):
        day = dateutils.day_of_year(datetime.datetime.now())
        msg = 'Example distutils: today is day #{}'.format(day)
        self.report({'INFO'}, msg)
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
