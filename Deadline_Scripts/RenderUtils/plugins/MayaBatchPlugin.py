"""
This will be loaded to grab all the maya info needed to build the plugin info file.
Maya version
Scene Name
Renderer
Render layers
Frames
ect..

There are a few ways I see a maya scene being rendered.
- Render layers are separated into different jobs. (Frames turned into tasks,
    the render layer has a camera associated with it, so it would just be the one)
- Cameras are separated into different jobs. (Frames turned into tasks, choose the 
    render layer for the job)
- Frames are separate jobs (less likely but Camera and render layers are tasks)
"""
# Standard Imports
import pymel as pm

# Custom Imports
from .BasePlugin import BasePlugin


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__('mayabatch')

        # Set the maya version
        self['Version'] = self._get_maya_version()
        # Set the scene file name
        self['SceneFile'] = self._get_scene_file()
        # Set the scene project path
        self['ProjectPath'] = self._get_project_path()

    def set_key_value(self, key, value):
        self[key] = value

    def set_output(self, dir_name, file_name):
        """
        Sets the output directory along with the file name
        """
        self['OutputFilePath'] = dir_name.replace('\\', '/')
        self['OutputFilePrefix'] = file_name

    def set_width_height(self, width, height):
        """ Sets the width and height of the render. """
        self['ImageWidth'] = width
        self['ImageHeight'] = height

    def disable_render_layers_as_jobs(self):
        """ Disables setting render layers as separate jobs. """
        self['UsingRenderLayers'] = 0

    @staticmethod
    def _get_maya_version():
        """ Gets the version of Maya being worked from. """
        return str(pm.versions.current())[0:4]

    @staticmethod
    def _get_project_path():
        """ Gets the project path set in the render settings. """
        return pm.core.Workspace().getcwd()

    @staticmethod
    def _get_scene_file():
        """ Gets the name of the file being worked on. """
        return pm.core.sceneName()


def main():
    x = Plugin()
    for key, value in list(x.items()):
        print(key + ": ", end=' ')
        print(value)

if __name__ == '__main__':
    main()
