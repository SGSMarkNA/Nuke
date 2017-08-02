import os
import nuke
import nukescripts
from Environment_Access import System_Paths, System_Settings, utilities



if os.name == 'nt':
	is_NT = True
else:
	is_NT = False
os.environ["QT_PACKAGE"] = "PySide"
if System_Settings.USE_WING_DEBUG:
	try:
		import wingdbstub
	except:
		pass


def drag_drop_shotgun_shot(mimeType, text):
	if mimeType == "text/plain":
		if text.startswith("https://armstrong-white.shotgunstudio.com/detail/Shot/"):
			try:
				import Nuke_Scripts.CommandLine.CPG_Shot_Contact_Sheet
			except ImportError:
				return False
			shot_id = int(text.split("/")[-1])
			Nuke_Scripts.CommandLine.CPG_Shot_Contact_Sheet.make_CPG_Contact_Sheet(shot_id)
			return True

def get_Path_To_Frames(mimeType, text):
	if mimeType == "text/plain":
		if text.startswith("https://armstrong-white.shotgunstudio.com/detail/Version/"):
			try:
				import AW_Shotgun_Access
			except ImportError:
				os.sys.path.append(os.environ.get("AW_BASE") + "/Shotgun")
				import AW_Shotgun_Access
			version_id = int(text.split("/")[-1])
			version    = AW_Shotgun_Access.get_Shotgun_Version([version_id], None, ["sg_path_to_frames", "code", "sg_last_frame", "sg_first_frame"])
			read_node  = nuke.createNode("Read","file %s name %s first %i last %i" % (version["sg_path_to_frames"].replace("\\","/"),version["code"],version["sg_first_frame"],version["sg_last_frame"]))
			return True
#----------------------------------------------------------------------
def _path_fixer(path):
	"""File Path Standerizer"""
	path = os.path.expandvars(path)
	return path.replace("\\", "/")

#----------------------------------------------------------------------
def get_and_set_environ_key_path(key, default, add_to_path=False, fource_default=False, fource_check=None):
	""""""
	res = _path_fixer(os.environ.get(key, default))
	if fource_default and callable(fource_check):
		if fource_check(res):
			res = _path_fixer(default)
	elif fource_default:
		res = _path_fixer(default)
	
	if add_to_path:
		if os.path.exists(res) and not res in os.sys.path:
			os.sys.path.append(res)
	os.environ[key] = res
	return res
#----------------------------------------------------------------------
def Add_User_Tools_Packages_To_Path(folder):
	folder = os.path.expandvars(folder)
	nuke.pluginAppendPath(folder)
	r,names,files = os.walk(folder).next()
	for n in names:
		path = os.path.join(r, n)
		os.sys.path.append(path)
		
#----------------------------------------------------------------------
# AW_BASE                = get_and_set_environ_key_path("AW_BASE", os.path.realpath(os.path.dirname(__file__)+"/.."), False, True)
#----------------------------------------------------------------------
#----------------------------------------------------------------------
AW_GIZMOS_PATH         = utilities.add_To_Multi_Path_Environment_Key("NUKE_GIZMOS", System_Paths._CODE_NUKE_GIZMOS)
#----------------------------------------------------------------------
AW_NUKE_PLUGINS_PATH   = utilities.add_To_Multi_Path_Environment_Key("NUKE_PLUGINS", [System_Paths._CODE_NUKE_PLUGINS])
#----------------------------------------------------------------------
AW_NUKE_USER_TOOLS_DIR = utilities.get_and_set_environ_key("NUKE_USER_TOOLS_DIR", System_Paths._CODE_NUKE_USER_TOOLS)
#----------------------------------------------------------------------

if os.path.exists(AW_NUKE_USER_TOOLS_DIR):
	Add_User_Tools_Packages_To_Path(AW_NUKE_USER_TOOLS_DIR)

if nuke != None:
	import Nuke_Scripts.SystemFns.paths
	import Nuke_Scripts.Callbacks
	Nuke_Scripts.SystemFns.paths.AddGizmo_Paths(System_Paths._CODE_NUKE_GIZMOS)
	nuke.pluginAppendPath(System_Paths._CODE_NUKE_PLUGINS)
	
	## Geometry_Tools plugins...
	if os.path.exists(System_Paths._CODE_NUKE_PLUGINS+"/geometry-1.1.544"):
		if is_NT:
			nuke.pluginAppendPath(System_Paths._CODE_NUKE_PLUGINS+"/geometry-1.1.544/Win")
		else:
			nuke.pluginAppendPath(System_Paths._CODE_NUKE_PLUGINS+"/geometry-1.1.544/Mac")
		try:
			import geometry
		except:
			print "Did Not Import Geometry Plugins"
			
	## J_Ops plugins...
	if os.path.exists(System_Paths._CODE_NUKE_PLUGINS+"/J_Ops_2.3v1_for_Nuke9.0"):
		if is_NT:
			nuke.pluginAppendPath(System_Paths._CODE_NUKE_PLUGINS+"/J_Ops_2.3v1_for_Nuke9.0/Win/J_Ops/py")
			nuke.pluginAddPath(System_Paths._CODE_NUKE_PLUGINS+"/J_Ops_2.3v1_for_Nuke9.0/Win/J_Ops/ndk")
			nuke.pluginAddPath(System_Paths._CODE_NUKE_PLUGINS+"/J_Ops_2.3v1_for_Nuke9.0/Win/J_Ops/icons")
		else:
			nuke.pluginAppendPath(System_Paths._CODE_NUKE_PLUGINS+"/J_Ops_2.3v1_for_Nuke9.0/Mac/J_Ops/py")
			nuke.pluginAddPath(System_Paths._CODE_NUKE_PLUGINS+"/J_Ops_2.3v1_for_Nuke9.0/Mac/J_Ops/ndk")
			nuke.pluginAddPath(System_Paths._CODE_NUKE_PLUGINS+"/J_Ops_2.3v1_for_Nuke9.0/Mac/J_Ops/icons")
		try:
			import J_Ops
		except ImportError:
			print "Did Not Import J_Ops Plugins"

	if nuke.GUI:
		## Revamped threaded localise function from Frank Rueter...
		## Replaces the nuke.localise method...
		import Nuke_Scripts.SystemFns.LocaliseThreaded
		Nuke_Scripts.SystemFns.LocaliseThreaded.register()
		nukescripts.addDropDataCallback(get_Path_To_Frames)
		nukescripts.addDropDataCallback(drag_drop_shotgun_shot)


		
'''
Temporary fix for views_button bug in Nuke 9.0v7 -- 09/11/15 - RKB.
BUG DESCRIPTION:
If the "views_button" checkbox knob in Project Settings is unchecked
when the script is saved, Nuke will crash on opening the script!
These callbacks will make sure that the checkbox is always on when
loading a script or saving a script. Note that you can still uncheck
the box while working on the script...
'''
import nuke

def Set_ViewsButton_On():
	nuke.root().knob('views_button').setValue(True)

# Check for Nuke 9.0v7 release...
Major = nuke.NUKE_VERSION_MAJOR 
Release = nuke.NUKE_VERSION_RELEASE 
if Major == 9 and Release == 7:
	nuke.addOnScriptLoad(Set_ViewsButton_On, (), {}, "Root")
	nuke.addOnScriptSave(Set_ViewsButton_On, (), {}, "Root")	
else:
	pass


## KNOB DEFAULTS: -----------------------------------------------------------

# Add default value to show what channels are actually being shuffled...

nuke.knobDefault( 'Shuffle.label', '[value in]' )

##  -------------------------------------------------------------------------




##  -------------------------------------------------------------------------
##  WriteNodeMetadata --->> Adds Metadata Tab to all Write nodes!
##  Callbacks on tab for adding an ICC Profile to an image, adding XMP/IPTC creator
##  and contact info for Armstrong White. Required by Innocean/Hyundai client.
##  -------------------------------------------------------------------------

import sys
modulename = 'WriteNodeMetadata'
try:
	os.sys.path.append('\\isln-smb\Git_Live_Code\Global_Systems\User_Tools\Nuke_User_Tools\Rich')
	import Callbacks_WriteNodeMetadata
	print 'Successfully imported the {} module.'.format(modulename)
except:
	if modulename not in sys.modules:
		print 'You have not imported the {} module.'.format(modulename)
		
##  -------------------------------------------------------------------------
