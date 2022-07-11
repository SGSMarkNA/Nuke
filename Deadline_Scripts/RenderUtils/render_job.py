"""
Deadline Render Utility
Main function is to build the job and plugin info files used by Deadline to render jobs.

Ties in with a custom plugin built for handling developer created python scripts.
"""
# Standard Imports
import sys
import os
import logging

# Custom Imports
from .repo_utils import *


class RenderJob(object):
    """
    Allows a developer to create their own Deadline submission file.
    A submission template is pulled from the repository allowing you to set values on it.
    Then when everything is set, you can submit the job.
    """
    deadlineCommand = GetDeadlineCommand()
    deadlineRepo = CallDeadlineCommand(['-GetRepositoryRoot'])
    deadlineHome = CallDeadlineCommand(['-GetCurrentUserHomeDirectory', ])

    def __init__(self):
        super(RenderJob, self).__init__()

        self.job_data = {
            'Plugin': None,  # Pulled from dcc
            'Name': None,  # Shotgun
            'Comment': None,
            'Department': None,
            'Pool': 'thr3d',
            'SecondaryPool': 'aw',
            'Group': '64gb',
            'Priority': 50,
            'MachineLimit': 0,
            'TaskTimeoutMinutes': 0,
            'EnableAutoTimeout': 'False',
            'ConcurrentTasks': 1,
            'LimitConcurrentTasksToNumberOfCpus': 'True',
            'LimitGroups': None,
            'JobDependencies': None,
            'OnJobComplete': 'Nothing',
            'ForceReloadPluging': False,
            'Frames': None,  # Pulled from job
            'ChunkSize': 1,  # Will need to allow users to set this if you need more than one task per job (ideal)
            'OutputFilename0': None,
            'ExtraInfo0': None,
            'ExtraInfo1': None,
            'ExtraInfo2': None,
            'ExtraInfo3': None,
            'ExtraInfo4': None,
            'ExtraInfo5': None,
            #'InitialStatus': 'Suspended'
        }

        # Need a running count of key / value pairs and env variables
        self.kvp_count = 0
        self.env_count = 0

        # Jobs plugin
        self.plugin = None

    def setValue(self, key, value):
        """
        Sets an arbitrary value on the job info.  This is the info on the job for the Deadline monitor.
        :param key: (str) Key name
        :param value: (str) Value
        """
        self.job_data[key] = value

    def setKeyValue(self, key, value):
        """
        Sets Key / Value pairs on the job.  These can be picked up by the job
        """
        self.job_data['ExtraInfoKeyValue{}'.format(self.kvp_count)] = "{}={}".format(key, value)
        self.kvp_count = self.kvp_count + 1

    def addPreJobScript(self, script_path):
        """
        This script will run prior to the job.
        :param script_path: 
        """
        self.job_data['PreJobScript'] = script_path

    def addEnvVariable(self, key, value):
        """
        Adds an environment variable to the job.
        If using custom script plugin these variables are available to your python script
        """
        self.job_data['EnvironmentKeyValue{}'.format(self.env_count)] = "{}={}".format(key, value)
        self.env_count = self.env_count + 1

    def setFrameRange(self, frames, by=None):
        """
        Sets the frame range for the job.
        :param frames: (str) String representation of frames to render ("1-10")
        """
        # TODO: Can add in the frame range regex
        self.job_data['Frames'] = frames

        if by:
            self.job_data['ChunkSize'] = by

    def setChunkSize(self, amount):
        """
        Sets the number of tasks per job.
        :param amount: (int) # of tasks per job.
        """
        # TODO: Have some check against the frame range
        self.job_data['ChunkSize'] = amount

    def addShotgunIntegration(self, data):
        # TODO: This should use the Shotgun commands
        """
        Will add Shotgun integration info into the dictionary.

        The Shotgun event looks for / uses the following info on a Deadline job:

        ExtraInfo0= Task        (Comp)
        ExtraInfo1= Project     (TEST-AJ-002)
        ExtraInfo2= Entity      (0003458) - Happens to be the name of a 'Shot' entity
        ExtraInfo3= Version     ([entity]_[step]_[version #])
        ExtraInfo4= Comment     (First pass of checkers)
        ExtraInfo5= User        (kevin.rakes)

        ExtraInfoKeyValue0 = UserName = kevin.rakes
        ExtraInfoKeyValue1 = Description = First pass of checkers
        ExtraInfoKeyValue2 = ProjectName = TEST-AJ-002
        ExtraInfoKeyValue3 = EntityName = 0003458
        ExtraInfoKeyValue4 = EntityType = Shot
        ExtraInfoKeyValue5 = VersionName = checker_1
        ExtraInfoKeyValue6 = ProjectId = 114
        ExtraInfoKeyValue7 = TaskId = 5840
        ExtraInfoKeyValue8 = TaskName = Comp
        ExtraInfoKeyValue9 = EntityId = 1182

        Knowing this, the following data will need to be collected:  (names, within shotgun maan codes)
        - Project   ('name', 'id')
        - Task      ('name', 'id')
        - Entity    ('name', 'id')  - Really only rendering shots, other than asset turntables.
        - Comment from the publish window
        - HumanUser ('login')

        How do we get the next version?
        """
        project_name = data['project'].get('name')
        project_id = data['project'].get('id')
        task_name = data['task'].get('name')
        task_id = data['task'].get('id')
        entity_name = data['entity'].get('name')
        entity_id = data['entity'].get('id')
        entity_type = data['entity'].get('type')
        version = data['version']
        comment = data.get('comment', '')
        user = data['user']

        self.setValue('ExtraInfo0', task_name)
        self.setValue('ExtraInfo1', project_name)
        self.setValue('ExtraInfo2', entity_name)
        self.setValue('ExtraInfo3', version)
        self.setValue('ExtraInfo4', comment)
        self.setValue('ExtraInfo5', user)

        self.setKeyValue('UserName', user)
        self.setKeyValue('Description', comment)
        self.setKeyValue('ProjectName', project_name)
        self.setKeyValue('EntityName', entity_name)
        self.setKeyValue('EntityType', entity_type)
        self.setKeyValue('VersionName', version)
        self.setKeyValue('ProjectId', project_id)
        self.setKeyValue('TaskId', task_id)
        self.setKeyValue('TaskName', task_name)
        self.setKeyValue('EntityId', entity_id)

    def setDependencies(self):
        """
        Sets job dependencies
        """
        pass

    def setMachineLimit(self, whitelist=False):
        """
        Sets machine limits on a job.  Defaulted to blacklist
        :param whitelist: (bool) If true, sets machine limit to a whitelist
        """
        pass

    def setPlugin(self, plugin):
        """
        Based on the DCC that created the RenderJob, that Plugin will be loaded.
        This can be changed to a script job by setting the plugin to 'Script'
        :param plugin: 
        """
        self.setValue('Plugin', plugin)

        _temp = __import__("RenderUtils.plugins.{}Plugin".format(plugin), globals(), locals(), ['Plugin'])
        self.plugin = _temp.Plugin()

    def write_job_files(self, id):
        """
        Writes out the job files.  job_info.txt, plugin_info.txt
        """
        if not self.plugin:
            print('Please define a plugin to before submitting a job!')
            return

        path = os.path.join(self.deadlineHome.rstrip('\n').rstrip('\r'), 'temp')
        jobInfo = os.path.join(path, 'job_info_{}.txt'.format(id))
        pluginInfo = os.path.join(path, 'plugin_info_{}.txt'.format(id))
        if not os.path.isdir(path):
            os.makedirs(path)

        # Write the job info
        with open(jobInfo, 'w') as jInfo:
            for i, j in sorted(self.job_data.items()):
                if isinstance(j, type(None)):
                    j = ''
                if isinstance(j, int):
                    j = str(j)
                jInfo.write('{}={}\n'.format(i, j))

        # Write the plugin info file
        with open(pluginInfo, 'w') as pInfo:
            for i, j in list(self.plugin.items()):
                if isinstance(j, type(None)):
                    j = ''
                if isinstance(j, int):
                    j = str(j)
                pInfo.write('{}={}\n'.format(i, j))

        return ' {} {}'.format(jobInfo, pluginInfo)

    def submitJob(self, id, *args):
        """
        Submits your job to the repository.
        """
        # For safety, reset kvp's
        self.kvp_count = 0
        self.env_count = 0

        # Write the job files
        files = self.write_job_files(id)

        proc = subprocess.Popen(self.deadlineCommand + '.exe' + files, stdout=subprocess.PIPE)
        output, errors = proc.communicate()

        jobId = None

        for line in output.splitlines():
            if line.startswith("JobID="):
                jobId = line[6:]
                break
        return jobId
