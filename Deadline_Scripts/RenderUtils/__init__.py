"""
Entry Point to all of RenderUtils
"""

# Standard Imports
import os
import sys
import logging

# # Custom Imports
# # TODO: Add this environment variable via IT department:
# THR3D_CGI_CONFIG = os.environ.get('THR3D_CGI_CONFIG',
#                                   r'\\isln-smb\thr3dcgi_config')
#
# if not os.path.exists(THR3D_CGI_CONFIG):
#     logging.error("Can't access to config path: {}".format(THR3D_CGI_CONFIG))
#     raise ValueError
#
# if THR3D_CGI_CONFIG not in sys.path:
#     sys.path.append(THR3D_CGI_CONFIG)
#
# try:
#     # Imports Agnostic variable paths (THR3D_MAYA)
#     from Agnostic import *  # Will only import what's defined in __all__, even though Agnostic imports common *
# except ImportError:
#     logging.error("THR3D was not able to load the Agnostic")
#     raise ImportError

from .render_job import RenderJob
from .templates import *
