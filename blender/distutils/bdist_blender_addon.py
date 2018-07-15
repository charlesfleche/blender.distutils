from distutils.core import Command
from distutils.dir_util import copy_tree, remove_tree
from importlib.util import find_spec
from pathlib import Path

def spec2path(spec):
    return Path(spec.origin).parent

class bdist_blender_addon(Command):
    description = "Build Blender addon"
    user_options = [
        ('addon-require=', None, 'Specify the packages to be copied and distributed with the Blender addon')
    ]
    sub_commands = (('build', lambda self: True),)

    def initialize_options(self):
        self.addon_require = []

    def finalize_options(self):
        v = self.addon_require
        self.addon_require = v.split(',') if type(v) is str else v

    def run(self):
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)

        addon_name = self.distribution.get_name()
        dist_dir = Path(self.get_finalized_command('bdist').dist_dir)
        archive_name = '{}-v{}'.format(addon_name, self.distribution.get_version())
        addon_archive = dist_dir / archive_name
        build_lib = Path(self.get_finalized_command('build').build_lib)
        build_addon = build_lib / addon_name

        for name in self.addon_require:
            p = spec2path(find_spec(name))
            copy_tree(str(p), str(build_addon/name))

        for pycache in build_addon.glob('**/__pycache__'):
            remove_tree(str(pycache))

        print(addon_archive)
        print(build_lib)
        print(addon_name)
        self.make_archive(str(addon_archive), 'zip', str(build_lib), addon_name)


__all__ = ('bdist_blender_addon')
