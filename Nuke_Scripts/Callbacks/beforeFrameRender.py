try:
	import nuke
except ImportError:
	nuke = None
	
from Nuke_Scripts.SystemFns.files_and_folders import createWriteDir
if not nuke == None:
	nuke.addBeforeFrameRender(createWriteDir, (), {}, "Write")