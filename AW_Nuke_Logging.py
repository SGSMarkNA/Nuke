import logging
import os

LOG_FILENAME = 'example.log'

# create logger
logger = logging.getLogger("AW_Nuke")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
#fh = logging.FileHandler(os.path.dirname(__file__)+"/Nuke_Startup.log",mode='w')
#fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(name)s :: %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)
#fh.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)