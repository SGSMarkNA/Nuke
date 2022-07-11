import os
import subprocess

def GetDeadlineCommand():
    """
    Looks on a users machine for the location of their Deadline installation
    """
    deadlineBin = ""
    try:
        deadlineBin = os.environ['DEADLINE_PATH']
    except KeyError:
        # if the error is a key error it means that DEADLINE_PATH is not set.
        # On OSX it could be in the file /Users/Shared/Thinkbox/DEADLINE_PATH
        pass

    # On OSX, we look for the DEADLINE_PATH file if the environment variable does not exist.
    if deadlineBin == "" and os.path.exists("/Users/Shared/Thinkbox/DEADLINE_PATH"):
        with open("/Users/Shared/Thinkbox/DEADLINE_PATH") as f:
            deadlineBin = f.read().strip()

    deadlineCommand = os.path.join(deadlineBin, "deadlinecommand")

    return deadlineCommand


def CallDeadlineCommand(arguments, hideWindow=True):
    """
    Runs a command line call with the given arguments
    :param arguments: (str) Argument called by Deadlinecommand.exe
    """
    deadlineCommand = GetDeadlineCommand()

    startupinfo = None
    if hideWindow and os.name == 'nt':
        # Python 2.6 has subprocess.STARTF_USESHOWWINDOW
        # Python 2.7 has subprocess._subprocess.STARTF_USESHOWWINDOW
        # Need to check for both.
        if hasattr(subprocess, '_subprocess') and hasattr(subprocess._subprocess, 'STARTF_USESHOWWINDOW'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
        elif hasattr(subprocess, 'STARTF_USESHOWWINDOW'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    environment = {}
    for key in list(os.environ.keys()):
        environment[key] = str(os.environ[key])

    # Need to set the PATH, windows seems to load DLLs from the PATH earlier that cwd....
    if os.name == 'nt':
        deadlineCommandDir = os.path.dirname(deadlineCommand)
        if not deadlineCommandDir == "":
            environment['PATH'] = deadlineCommandDir + os.pathsep + os.environ['PATH']

    arguments.insert(0, deadlineCommand)
    output = ""

    # Specifying PIPE for all handles to workaround a Python bug on Windows.
    # The unused handles are then closed immediatley afterwards.
    proc = subprocess.Popen(arguments, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            startupinfo=startupinfo, env=environment)
    output, errors = proc.communicate()

    return output