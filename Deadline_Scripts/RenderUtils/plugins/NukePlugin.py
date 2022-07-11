"""
This will be loaded to grab all the nuke info needed to build the plugin info file.
Nuke version
Scene Name
"""

# Standard Imports
import os

# Custom Imports
from .BasePlugin import BasePlugin


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__('nuke')

    @staticmethod
    def _get_version():
        """ Gets the version of Nuke being worked from. """
        import nuke
        return str(nuke.NUKE_VERSION_MAJOR) + '.' + str(nuke.NUKE_VERSION_MINOR)

    @staticmethod
    def _get_scene_file():
        """ Gets the name of the file being worked on. """
        import nuke
        return nuke.root().name().replace("/", os.path.sep)

    def set_version(self, version):
        """
        Sets the Nuke version to use on Deadline to the passed version string
        :type version: str
        :param version:
        """
        self['Version'] = str(version)

    def set_scene_file(self, scene_file):
        """
        Sets the scene file for Nuke to open on Deadline
        :type scene_file: str
        :param scene_file:
        """
        self['SceneFile'] = scene_file.replace('\\', '/')


def main():
    x = Plugin()
    for key, value in list(x.items()):
        print(key + ": ", end=' ')
        print(value)

if __name__ == '__main__':
    main()
