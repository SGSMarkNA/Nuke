"""
"""

# Custom Imports
from .. import templates


class BasePlugin(dict):
    def __init__(self, plugin_type):
        super(BasePlugin, self).__init__()

        # Pulls the info from the template
        self.grab_template(plugin_type)

    def grab_template(self, plugin_type):
        for key, value in templates.__dict__[plugin_type + "_form"].items():
            self[key] = value

    @staticmethod
    def _get_version():
        """ Placeholder, needs to be redefined in actual plugin"""
        pass

    @staticmethod
    def _get_scene_file():
        """ Placeholder, needs to be redefined in actual plugin"""
        pass
