"""
Place this file on the server.
Make sure that the submit script points to it. Just replace this file with the file in:
\\isln-smb\aw_config\Git_Live_Code\Global_Systems\\User_Tools\Nuke_User_Tools\Deadline_Script_Execute\
"""

import os
import nuke
import argparse

# Set up arguments
parser = argparse.ArgumentParser()
parser.add_argument("-nf", "--nukefiles", help="Nuke files to be executed on Deadline")
args = parser.parse_args()

# Catch if no files were passed to the script, and raise an error to fail the job.
if not args.nukefiles:
    print("No Nuke files have been passed to this script")
    raise

# Nuke_Files will read in the argument passed to the script and convert it to a list
Nuke_Files = args.nukefiles.split('|')
nuke.scriptOpen(Nuke_Files[(int(os.environ['STARTFRAME'])) - 1])
for node in nuke.allNodes('Write'):
    if node['disable'].value():
        pass
    else:
        nuke.execute(node, 1, 1)
