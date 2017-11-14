"""
Standard templates for the Deadline Plugin files
"""
import os
import sys
import logging


nuke_form = {
    'SceneFile': None,      # Path to project file
    'Version': 10.5,        # Version of software
    'Threads': 0,
    'RamUse': 0,
    'BatchMode': True,
    'BatchModeIsMovie': False,
    'NukeX': False,
    'UseGpu': False,
    'GpuOverride': 0,
    'RenderMode': 'Use Scene Settings',
    'EnforceRenderOrder': False,
    'ContinueOnError': False,
    'PerformanceProfiler': False,
    'PerformanceProfilerDir': None,
    'Views': None,
    'StackSize': 0
}

mayabatch_form = {
    'Animation': 1,
    'Renderer': 'vray',         # 90% of the time will be VRay
    'UsingRenderLayers': 1,     # True will submit render layers as separate jobs
    'RenderLayer': None,        # As part of the publish, will need to loop through the render layers and set this
    'RenderHalfFrames': 0,
    'FrameNumberOffset': 0,
    'LocalRendering': 0,
    'StrictErrorChecking': 1,
    'MaxProcessors': 0,
    'Version': 2017,
    'UseLegacyRenderLayers': 1,
    'Build': '64bit',
    'ProjectPath': None,        # Grabbed from the project
    'StartupScript': None,
    'ImageWidth': None,             # Provided by Shotgun
    'ImageHeight': None,            # Provided by Shotgun
    'SkipExistingFrames': 0,
    'OutputFilePath': None,         # Output paths for images
    'OutputFilePrefix': None,       # Output name for images. Can use maya tokens in name (%l - layer name)
    'Camera': None,
    'Camera0': None,
    'SceneFile': None,              # Project file
    'IgnoreError211': 0,
    'UseLocalAssetCaching': 0
}

script_form = {
    'Executable': 'C:/Python27/python.exe',     # Program to run, Python by default
    'Script': os.path.join(os.path.dirname(__file__), 'default_printer.py'),  # Script to run
    'Arguments': None       # Arguments to pass to the script
}

__all__ = ['nuke_form',
           'mayabatch_form',
           'script_form'
           ]
