try:
	import nuke
except ImportError:
	nuke = None
	
from Nuke_Scripts.SystemFns.files_and_folders import createWriteDir
if not nuke == None:
	# Nuke 10.5 now has a create_directories knob that will automatically create any non-existant directories.
	# There is a knobDefault in app_initialization to turn on the knob's checkbox for any new Write nodes.
	Major = nuke.NUKE_VERSION_MAJOR
	Minor = nuke.NUKE_VERSION_MINOR
	if Major <10:	
		nuke.addBeforeFrameRender(createWriteDir, (), {}, "Write")