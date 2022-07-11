"""
This will be loaded to grab all the nuke info needed to build the plugin info file.
Nuke version
Scene Name
"""

# Standard Imports
import os
import nuke

# Custom Imports
from BasePlugin import BasePlugin


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__('nuke')

        # Set the Nuke version
        self['Version'] = self._get_version()
        # Set the scene file name
        self['SceneFile'] = self._get_scene_file()

    @staticmethod
    def _get_version():
        """ Gets the version of Nuke being worked from. """
        return str(nuke.NUKE_VERSION_MAJOR) + '.' + str(nuke.NUKE_VERSION_MINOR)

    @staticmethod
    def _get_scene_file():
        """ Gets the name of the file being worked on. """
        return nuke.root().name().replace("/", os.path.sep)


def main():
    x = Plugin()
    for key, value in list(x.items()):
        print(key + ": ", end=' ')
        print(value)

if __name__ == '__main__':
    main()
