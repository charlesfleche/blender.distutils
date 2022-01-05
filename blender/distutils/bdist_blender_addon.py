from distutils.core import Command
from distutils.dir_util import copy_tree, remove_tree, mkpath
from distutils.file_util import copy_file, write_file
from distutils.util import get_platform
from importlib.util import find_spec
from pathlib import Path

def spec2path(spec):
    if spec.origin.endswith("__init__.py"):
        # This works for most packages that are __init__.py based.
        print("Blender.DistUtils: Found full package to copy: " + spec.name)
        return (Path(spec.origin).parent,True)
    else:
        # This is a fix for single-file packages that don't have __init__.py.
        print("Blender.DistUtils: Found single file to copy: "+ spec.name)
        return (Path(spec.origin),False)

class bdist_blender_addon(Command):
    description = "Build Blender addon"
    user_options = [
        ('addon-require=', None, 'Specify the packages to be copied and distributed with the Blender addon'),
        ('tag-plat', None, 'Add the platform name to the generated filename'),
        ('plat-name=', None, 'Platform name to embed in generated filenames (default: {})'.format(get_platform())),
    ]
    sub_commands = (('build', lambda self: True),)

    def initialize_options(self):
        self.addon_require = []
        self.tag_plat = None
        self.plat_name = None

    def finalize_options(self):
        v = self.addon_require
        self.addon_require = v.split(',') if type(v) is str else v
        if self.plat_name is None:
            self.plat_name = get_platform()

    def run(self):
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)

        addon_name = self.distribution.get_name()
        dist_dir = Path(self.get_finalized_command('bdist').dist_dir)
        archive_name = '{}-v{}'.format(addon_name, self.distribution.get_version())
        if self.tag_plat:
            archive_name = '{}.{}'.format(archive_name, self.plat_name)
        addon_archive = dist_dir / archive_name
        build_lib = Path(self.get_finalized_command('build').build_lib)
        build_addon = build_lib / addon_name

        for name in self.addon_require:
            p = spec2path(find_spec(name))
            if(p[1]):
                structure = name.split(".")
                if len(structure) > 1:
                    # Need to create separate files for it
                    print("Splitting the compound directory")
                    destination = build_addon
                    for pathsection in structure:
                        destination = destination / pathsection
                        mkpath(str(destination))
                        write_file(str(destination / "__init__.py"),"")
                    copy_tree(str(p[0]), str(destination))
                else:
                    copy_tree(str(p[0]), str(build_addon/name))
            else:
                copy_file(str(p[0]), str(build_addon))

        for pycache in build_addon.glob('**/__pycache__'):
            remove_tree(str(pycache))

        print(addon_archive)
        print(build_lib)
        print(addon_name)
        self.make_archive(str(addon_archive), 'zip', str(build_lib), addon_name)


__all__ = ('bdist_blender_addon')
