"""
This plugin allows a user to develop their own script to process on the farm. Similar to the python plugin however you
can pass in env variables and use them in your script.
Ex.
Setting 'DIVISION' on the job environment will allow you to call os.environ['DIVISION'] within your script
"""

# Custom Imports
from BasePlugin import BasePlugin


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__('script')

    def set_executable(self, executable):
        """
        Gets the version of Maya being worked from
        :param executable: (str) Path to an executable to run.  Ex. C:/Python27/python.exe
        """
        self['Executable'] = executable

    def set_script(self, script):
        """
        Sets a script for the executable to run.  These are almost exclusively python scripts as Deadline and RenderUtils
        are written in python.  Perhaps in the future this can be expanded.
        :param script: (str) Path to a python script to run within the executable.
        """
        self['Script'] = script

    def add_argument(self, argument):
        """
        Adds system arguments to the python script.  These can be set you as argparse strings, just in your script
        make sure you account for this.
        :param argument: (str) Argument to pass the the python script, either sys.argv or argparse will work.
        """
        if not self['Arguments']:
            self['Arguments'] = argument
            return
        self['Arguments'] += ' {}'.format(argument)


def main():
    x = Plugin()
    for key, value in x.items():
        print key + ": ",
        print value

if __name__ == '__main__':
    main()
