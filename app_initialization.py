print("Running Nuke Init")
import os
import nuke
import nukescripts
if 'USE_WING_DEBUG' in os.environ:
	try:
		import wingdbstub
	except:
		os.sys.path.append(r"C:\Program Files (x86)\Wing Pro 8")
		try:
			import wingdbstub
		except:
			print("Could Not Import Wing Debuger")

try:
	import wingdbstub
except:
	os.sys.path.append(r"C:\Program Files (x86)\Wing Pro 8")
	try:
		import wingdbstub
	except:
		print("Could Not Import Wing Debuger")

__this_dir = os.path.dirname(__file__)
# from Environment_Access import System_Paths, System_Settings, utilities
if "AW_GLOBAL_SYSTEMS" in os.environ:
	if not os.environ["AW_GLOBAL_SYSTEMS"] in os.sys.path:
		os.sys.path.append(os.environ["AW_GLOBAL_SYSTEMS"])
else:
	global_systems_directory = os.path.realpath(__this_dir+"/../../Global_Systems")
	if os.path.exists(global_systems_directory) and not global_systems_directory in os.sys.path:
		os.sys.path.append(global_systems_directory)
		os.sys.path.append(os.path.join(global_systems_directory,"DML_Tools"))
		os.sys.path.append(os.path.join(global_systems_directory,"DML_Tools","DML_PYQT"))
		os.sys.path.append(os.path.join(global_systems_directory,"DML_Tools","DML_Nuke"))

from Environment_Access import System_Paths, System_Settings, utilities

utilities.add_To_System_Path(System_Paths.AW_SITE_PACKAGES)

#try:
	#from Environment_Access import System_Paths, System_Settings, utilities
#except:
	#os.sys.path.append("//isln-smb.ad.sgsco.int/aw_config/Git_Live_Code/Global_Systems")
	#from Environment_Access import System_Paths, System_Settings, utilities

OCIO_CONFIG_FILE = System_Settings.OCIO_CONFIG_FILE


if os.name == 'nt':
	is_NT = True
else:
	is_NT = False
os.environ["QT_PACKAGE"] = "PySide"


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
	r,names,files = next(os.walk(folder))
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
if not System_Settings.NO_USER_TOOLS:
	if os.path.exists(AW_NUKE_USER_TOOLS_DIR):
		Add_User_Tools_Packages_To_Path(AW_NUKE_USER_TOOLS_DIR)
	else:
		print("AW_NUKE_USER_TOOLS_DIR %r Did not exist" % AW_NUKE_USER_TOOLS_DIR)
	
if nuke != None:
	# Get the current version of nuke
	Major = nuke.NUKE_VERSION_MAJOR
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
			print("Did Not Import Geometry Plugins")

	# Determine whether to add the J_Ops plugins, based on the Nuke version.
	# Anything later than ver. 10.5 will not add because no version is avalible.
	if Major <= 10:
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
				print("Did Not Import J_Ops Plugins")
	if Major >= 12:
		## Cryptomatte plugins...
		if os.path.exists(System_Paths._CODE_NUKE_PLUGINS+"/Cryptomatte"):
			nuke.pluginAppendPath(System_Paths._CODE_NUKE_PLUGINS+"/Cryptomatte/nuke")
			nuke.pluginAddPath(System_Paths._CODE_NUKE_PLUGINS+"/Cryptomatte/nuke")
			os.sys.path.append(System_Paths._CODE_NUKE_PLUGINS+"/Cryptomatte/nuke")
			try:
				import cryptomatte_utilities
				cryptomatte_utilities.setup_cryptomatte()
			except ImportError:
				print("Did Not Import Cryptomatte Plugins")
			
	## VRayDenoiser plugins...
	if Major == 10:
		if os.path.exists(System_Paths._CODE_NUKE_PLUGINS+"/VRayDenoiser/v10"):
			nuke.pluginAppendPath(System_Paths._CODE_NUKE_PLUGINS+"/VRayDenoiser/v10")
	if Major == 12:
		if os.path.exists(System_Paths._CODE_NUKE_PLUGINS+"/VRayDenoiser/v12"):
			nuke.pluginAppendPath(System_Paths._CODE_NUKE_PLUGINS+"/VRayDenoiser/v12")
			
	## Lens Distortion Plugin Kit...
	if Major == 12:
		if os.path.exists(System_Paths._CODE_NUKE_PLUGINS+"/3DE_Lens_Distortion_Plugin_Kit_v2_6/v12_2"):
			nuke.pluginAppendPath(System_Paths._CODE_NUKE_PLUGINS+"/3DE_Lens_Distortion_Plugin_Kit_v2_6/v12_2")
			
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
Minor = nuke.NUKE_VERSION_MINOR
Release = nuke.NUKE_VERSION_RELEASE 
if Major == 9 and Minor == 0 and Release == 7:
	nuke.addOnScriptLoad(Set_ViewsButton_On, (), {}, "Root")
	nuke.addOnScriptSave(Set_ViewsButton_On, (), {}, "Root")	
else:
	pass


##-------------------------------------------------------------------------
## MISC. KNOB DEFAULTS:
##-------------------------------------------------------------------------
# Add default value to show what channels are actually being shuffled...
nuke.knobDefault( 'Shuffle.label', '[value in1]' )


##-------------------------------------------------------------------------
## Add Write Node knobDefault for automatically creating missing directories...
## Also, turns on the button for any older scripts (pre-10.5v4)...
##-------------------------------------------------------------------------
Major = nuke.NUKE_VERSION_MAJOR
if Major >= 10:
	import sys
	modulename = 'Callback_WriteNode_create_directories_ON'
	try:
		os.sys.path.append(os.environ['NUKE_USER_TOOLS_DIR'])
		import Callback_WriteNode_create_directories_ON
		print('Successfully imported the {} module.'.format(modulename))
	except:
		if modulename not in sys.modules:
			print('ERROR: Unable to load the {} module.'.format(modulename))	
if Major >= 13:
	os.environ["QT_PACKAGE"] = "PySide2"
else:
	os.environ["QT_PACKAGE"] = "PySide"
##-------------------------------------------------------------------------
##  WriteNodeMetadata --->> Adds Metadata Tab to all Write nodes!
##  Callbacks on tab for adding an ICC Profile to an image, adding XMP/IPTC creator
##  and contact info for Armstrong White. Required by Innocean/Hyundai client.
##-------------------------------------------------------------------------
import sys
modulename = 'WriteNodeMetadata'
try:
	os.sys.path.append(os.environ['NUKE_USER_TOOLS_DIR'])
	import Callbacks_WriteNodeMetadata
	print('Successfully imported the {} module.'.format(modulename))
except:
	if modulename not in sys.modules:
		print('ERROR: Unable to load the {} module.'.format(modulename))
##-------------------------------------------------------------------


##-------------------------------------------------------------------
##  OCIO / ACES Config knobDefaults for colorManagement
##-------------------------------------------------------------------
# Set which OCIO config file is to be used as the default for colorManagement...
# NOTE: OCIO_CONFIG_FILE is set in System_Paths.py and System_Settings.py
try:
	# Determine whether to load an AW custom OCIO config file, based on the nuke version.
	# Anything earlier than ver. 10.5 will load nuke-default.	
	Major = nuke.NUKE_VERSION_MAJOR
	if Major >= 10:
		if 'aw_Comp_config' in OCIO_CONFIG_FILE:
			print("Using custom OCIO config 'aw_Comp_config' for colorManagement.")
			defaultConfig = OCIO_CONFIG_FILE.replace('\\', '/')
			##-------------------------------------------------------------------
			## Default Color Workflow --> "Delta_sRGB"
			## Note: The default viewerProcess selection in the GUI is set via the "aw_Comp_config.ocio" file, in the "active_views:" entries.
			##       The config file is located in \\isln-smb\library\OCIO_Configs\aw_Comp_aces_1.0.3\
			#nuke.knobDefault('Root.colorManagement', 'OCIO')
			#nuke.knobDefault('Root.customOCIOConfigPath', defaultConfig)
			#nuke.knobDefault('Root.OCIO_config', 'custom')
			#nuke.knobDefault('Root.workingSpaceLUT', 'ACES - ACES2065-1')
			#nuke.knobDefault('Root.monitorLut', 'AW/Delta_Gamma_sRGB')
			#nuke.knobDefault('Root.int8Lut', 'Delta_Gamma')
			#nuke.knobDefault('Root.int16Lut', 'Delta_Gamma')
			#nuke.knobDefault('Root.logLut', 'ACES - ACES2065-1')
			#nuke.knobDefault('Root.floatLut', 'ACES - ACES2065-1')
			##---------------------------------------------------------------------
			## Default Color Workflow --> "Legacy_sRGB"
			## Note: The default viewerProcess selection in the GUI is set via the "aw_Comp_config.ocio" file, in the "active_views:" entries.
			##       The config file is located in \\isln-smb\library\OCIO_Configs\aw_Comp_aces_1.0.3\			
			nuke.knobDefault('Root.colorManagement', 'OCIO')
			# nuke.knobDefault('Root.customOCIOConfigPath', defaultConfig)
			# nuke.knobDefault('Root.OCIO_config', 'custom')
			# nuke.knobDefault('Root.workingSpaceLUT', 'ACES - ACES2065-1')
			# nuke.knobDefault('Root.monitorLut', 'AW/sRGB_ICC(sRGB)')
			# nuke.knobDefault('Root.int8Lut', 'sRGB')
			# nuke.knobDefault('Root.int16Lut', 'sRGB')
			# nuke.knobDefault('Root.logLut', 'ACES - ACES2065-1')
			# nuke.knobDefault('Root.floatLut', 'ACES - ACES2065-1')
			##-------------------------------------------------------------------			
		elif OCIO_CONFIG_FILE == 'nuke-default':
			print("Using nuke-default OCIO config for colorManagement.")
	else:
		# Just let the Nuke default color settings load for earlier releases...
		print("Using nuke-default OCIO config for colorManagement.")
except Exception:
	print("ERROR: Unable to load the OCIO config file!")
	nuke.critical("Unable to load the OCIO config file!")
##-------------------------------------------------------------------
import DML_Tools	
#try:
	#import DML_Tools
#except:
	#print("Could Not import Dml_Tools")
	#pass
##-------------------------------------------------------------------
