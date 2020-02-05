import nuke
import nukescripts
import os

# Closes all property boxes at once (especially useful if you like to use floating windows).
def CloseAllProperties():
	
	# for each node, even the ones in groups
	for n in nuke.allNodes(recurseGroups=True):

		# hide the control panel
		n.hideControlPanel()

	nuke.root().hideControlPanel()


def aw_rename():
	n = nuke.selectedNode()
	new_name = nuke.getInput('Rename {0} to:'.format(n.name()))
	if new_name:
		n.setName(new_name)

def aw_toggleViewerPipes():
	for n in nuke.allNodes('Viewer'):
		curValue=n['hide_input'].value()
		n['hide_input'].setValue(not curValue)

#Render Menu
RENDER_MENU = nuke.menu("Nuke").menu("Render")
RENDER_MENU.addCommand("Submit To Deadline", "from Nuke_Scripts.CommandLine import DeadlineNukeClient\nDeadlineNukeClient.main()", "Shift+Ctrl+Alt+D")

#Nuke Menu
AW_TOOLS_MENU = nuke.menu("Nuke").addMenu("AW Tools")
# AW_TOOLS_MENU.addCommand("Load User Tools"              ,"import UserTools\nUserTools.pythonScripts()" )
AW_TOOLS_MENU.addCommand("Generate Gizmo Menu"                  ,"import Nuke_Scripts.SystemFns.paths\nNuke_Scripts.SystemFns.paths.generate_Gizmo_Menu()")
AW_TOOLS_MENU.addSeparator()
AW_TOOLS_MENU.addCommand('Close All Properties', "CloseAllProperties()", "\\") # two backslashes necessary to write one, as it is an escape character

AW_TOOLS_MENU.addCommand("Create Side Dots"                   ,"import Nuke_Scripts.NodeFns.dots\nNuke_Scripts.NodeFns.dots.create_Side_Dots()")
AW_TOOLS_MENU.addCommand("One View To Join Connect"           ,"import Nuke_Scripts.ViewFns.joinview_connecter\nNuke_Scripts.ViewFns.joinview_connecter.connect_oneviews_to_joinview()")
AW_TOOLS_MENU.addCommand("Select Orphan Nodes"                ,"import Nuke_Scripts.NodeGraphFns.selecting\nNuke_Scripts.NodeGraphFns.selecting.select_orphans()")
AW_TOOLS_MENU.addCommand("Open File In Explorer"           ,"import Nuke_Scripts.NodeFns.footage\nNuke_Scripts.NodeFns.footage.go_to_file()" , 'ctrl+f')
AW_TOOLS_MENU.addSeparator()
AW_TOOLS_MENU.addCommand("Node Graph/Rename Selected"                   ,"aw_rename()", "n")
AW_TOOLS_MENU.addCommand("Node Graph/Toggle Viewer Pipes"               ,"aw_toggleViewerPipes()", "alt+t")
AW_TOOLS_MENU.addCommand("Node Graph/Placement/Align Horizontal"        ,"import Nuke_Scripts.NodeGraphFns.transforms\nNuke_Scripts.NodeGraphFns.transforms.aline_Avarage(direction='h')"  , "alt+x")		#### Note: This hotkey overrides the shortcut cut for "File/TCL File..."
AW_TOOLS_MENU.addCommand("Node Graph/Placement/Align Vertical"          ,"import Nuke_Scripts.NodeGraphFns.transforms\nNuke_Scripts.NodeGraphFns.transforms.aline_Avarage(direction='v')"  , "alt+y")

#Node Graph Menu
NODE_GRAPH =nuke.menu('Node Graph')
TOOLS      = NODE_GRAPH.addMenu("AW Tools")

NODE_TOOLS = TOOLS.addMenu("Nodes")
NODE_TOOLS.addCommand("Align Horizontal"              ,"import Nuke_Scripts.NodeGraphFns.transforms\nNuke_Scripts.NodeGraphFns.transforms.aline_Avarage(direction='h')" )
NODE_TOOLS.addCommand("Align Vertical"                ,"import Nuke_Scripts.NodeGraphFns.transforms\nNuke_Scripts.NodeGraphFns.transforms.aline_Avarage(direction='v')" )
NODE_TOOLS.addCommand("Multi Node Declone"            ,"import Nuke_Scripts.NodeFns.declone\nNuke_Scripts.NodeFns.declone.multi_declone()" )
NODE_TOOLS.addCommand("Multi Input Connect"           ,"import Nuke_Scripts.NodeFns.connections\nNuke_Scripts.NodeFns.connections.multi_input_connect()" )
NODE_TOOLS.addCommand("Multi Output Connect"          ,"import Nuke_Scripts.NodeFns.connections\nNuke_Scripts.NodeFns.connections.multi_output_connect()" )
NODE_TOOLS.addCommand("Exr Layer Extractor"           ,"import Nuke_Scripts.NodeFns.split_layers\nNuke_Scripts.NodeFns.split_layers.split_layers()" )
NODE_TOOLS.addCommand("Open File In Explorer"           ,"import Nuke_Scripts.NodeFns.footage\nNuke_Scripts.NodeFns.footage.go_to_file()" , 'ctrl+f')

KNOB_TOOLS = TOOLS.addMenu("Knobs")
KNOB_TOOLS.addCommand("Set Selected Font Size"        ,"import Nuke_Scripts.KnobFns.values\nNuke_Scripts.KnobFns.values.set_selected_font_size()" )
KNOB_TOOLS.addCommand("Set Knob Values"               ,"import Nuke_Scripts.KnobFns.values\nNuke_Scripts.KnobFns.values.set_selected_values()" )

SCRIPTING_TOOLS = TOOLS.addMenu("Scripting")
SCRIPTING_TOOLS.addCommand("Set Selected Node to G_node Var","G_node = nuke.selectedNode()")
SCRIPTING_TOOLS.addCommand("Set Selected Node to G_node2 Var","import Nuke_Scripts.NukeNodes\nG_node2 = Nuke_Scripts.NukeNodes.Node(nuke.selectedNode())")
SCRIPTING_TOOLS.addCommand("Set Selected Nodes to G_nodes Var","G_nodes = nuke.selectedNodes()")

##-------------------------------------------------------------------
## AW_COLOR_TOOLS Menus for OCIO / ACES colorManagement
##-------------------------------------------------------------------
# NOTE: OCIO_CONFIG_FILE is set in System_Paths.py and System_Settings.py
from Environment_Access import System_Paths, System_Settings, utilities
OCIO_CONFIG_FILE = System_Settings.OCIO_CONFIG_FILE

# Determine whether to add the AW_COLOR_TOOLS menus, based on the Nuke version.
# Anything earlier than ver. 10.5 will not add the buttons.
Major = nuke.NUKE_VERSION_MAJOR
try:
	if Major >= 10:
		
		# Nuke uses forward slashes...
		ConfigFile = OCIO_CONFIG_FILE.replace('\\', '/')
		
		# Set Delta color workflow OCIO configuration settings with sRGB preview...
		def set_AW_COLOR_colorManagement_Delta_sRGB():
			nuke.Root().knob('colorManagement').setValue('OCIO')
			nuke.Root().knob('customOCIOConfigPath').setValue(ConfigFile)
			nuke.Root().knob('OCIO_config').setValue('custom')
			nuke.Root().knob('workingSpaceLUT').setValue('ACES/ACES - ACES2065-1')
			nuke.Root().knob('monitorLut').setValue('AW/Delta_Gamma_sRGB')
			nuke.Root().knob('int8Lut').setValue('AW/Delta_Gamma')
			nuke.Root().knob('int16Lut').setValue('AW/Delta_Gamma')
			nuke.Root().knob('logLut').setValue('ACES/ACES - ACES2065-1')
			nuke.Root().knob('floatLut').setValue('ACES/ACES - ACES2065-1')
			# Set the active Viewer to the monitorLUT value...
			nuke.activeViewer().node().knob('viewerProcess').setValue('Delta_Gamma_sRGB')
			
		# Set Delta color workflow OCIO configuration settings with AdobeRGB(1998) preview...
		def set_AW_COLOR_colorManagement_Delta_Adobe98():
			nuke.Root().knob('colorManagement').setValue('OCIO')
			nuke.Root().knob('customOCIOConfigPath').setValue(ConfigFile)
			nuke.Root().knob('OCIO_config').setValue('custom')
			nuke.Root().knob('workingSpaceLUT').setValue('ACES/ACES - ACES2065-1')
			nuke.Root().knob('monitorLut').setValue('AW/Delta_Gamma_Adobe98')
			nuke.Root().knob('int8Lut').setValue('AW/Delta_Gamma')
			nuke.Root().knob('int16Lut').setValue('AW/Delta_Gamma')
			nuke.Root().knob('logLut').setValue('ACES/ACES - ACES2065-1')
			nuke.Root().knob('floatLut').setValue('ACES/ACES - ACES2065-1')
			# Set the active Viewer to the monitorLUT value...
			nuke.activeViewer().node().knob('viewerProcess').setValue('Delta_Gamma_Adobe98')
		
		# Set Legacy/Linear color workflow OCIO configuration settings with sRGB preview...
		def set_AW_COLOR_colorManagement_Legacy_sRGB():
			nuke.Root().knob('colorManagement').setValue('OCIO')
			nuke.Root().knob('customOCIOConfigPath').setValue(ConfigFile)
			nuke.Root().knob('OCIO_config').setValue('custom')
			nuke.Root().knob('workingSpaceLUT').setValue('ACES/ACES - ACES2065-1')
			nuke.Root().knob('monitorLut').setValue('AW/sRGB_ICC(sRGB)')
			nuke.Root().knob('int8Lut').setValue('AW/sRGB')
			nuke.Root().knob('int16Lut').setValue('AW/sRGB')
			nuke.Root().knob('logLut').setValue('ACES/ACES - ACES2065-1')
			nuke.Root().knob('floatLut').setValue('ACES/ACES - ACES2065-1')
			# Set the active Viewer to the monitorLUT value...
			nuke.activeViewer().node().knob('viewerProcess').setValue('sRGB_ICC(sRGB)')
			
		# Set Legacy/Linear color workflow OCIO configuration settings with AdobeRGB(1998) preview...
		def set_AW_COLOR_colorManagement_Legacy_Adobe98():
			nuke.Root().knob('colorManagement').setValue('OCIO')
			nuke.Root().knob('customOCIOConfigPath').setValue(ConfigFile)
			nuke.Root().knob('OCIO_config').setValue('custom')
			nuke.Root().knob('workingSpaceLUT').setValue('ACES/ACES - ACES2065-1')
			nuke.Root().knob('monitorLut').setValue('AW/sRGB_ICC(Adobe98)')
			nuke.Root().knob('int8Lut').setValue('AW/sRGB')
			nuke.Root().knob('int16Lut').setValue('AW/sRGB')
			nuke.Root().knob('logLut').setValue('ACES/ACES - ACES2065-1')
			nuke.Root().knob('floatLut').setValue('ACES/ACES - ACES2065-1')
			# Set the active Viewer to the monitorLUT value...
			nuke.activeViewer().node().knob('viewerProcess').setValue('sRGB_ICC(Adobe98)')
		
		# Set Original Nuke Default color workflow settings with sRGB Gamma...
		def set_AW_COLOR_colorManagement_nukeDefault():
			nuke.Root().knob('colorManagement').setValue('Nuke')
			nuke.Root().knob('OCIO_config').setValue('nuke-default')
			nuke.Root().knob('monitorLut').setValue('sRGB')
			nuke.Root().knob('int8Lut').setValue('sRGB')
			nuke.Root().knob('int16Lut').setValue('sRGB')
			nuke.Root().knob('logLut').setValue('Cineon')
			nuke.Root().knob('floatLut').setValue('linear')
			# Set the active Viewer to the monitorLUT value...
			nuke.activeViewer().node().knob('viewerProcess').setValue('sRGB')
			
		# Add Node Graph right-click menus...
		AW_COLOR_TOOLS = NODE_GRAPH.addMenu("AW Color")
		#AW_COLOR_TOOLS.addCommand("Delta_sRGB", "set_AW_COLOR_colorManagement_Delta_sRGB()")
		#AW_COLOR_TOOLS.addCommand("Delta_Adobe98", "set_AW_COLOR_colorManagement_Delta_Adobe98()")
		AW_COLOR_TOOLS.addCommand("Legacy_sRGB", "set_AW_COLOR_colorManagement_Legacy_sRGB()")
		AW_COLOR_TOOLS.addCommand("Legacy_Adobe98", "set_AW_COLOR_colorManagement_Legacy_Adobe98()")
		AW_COLOR_TOOLS.addCommand("Nuke-default", "set_AW_COLOR_colorManagement_nukeDefault()")
		
		# Add Title Bar menus...
		aw_color_menu_items = []
		#aw_color_menu_items.append(("AW Color/Delta_sRGB", "set_AW_COLOR_colorManagement_Delta_sRGB()"))
		#aw_color_menu_items.append(("AW Color/Delta_Adobe98", "set_AW_COLOR_colorManagement_Delta_Adobe98()"))
		aw_color_menu_items.append(("AW Color/Legacy_sRGB", "set_AW_COLOR_colorManagement_Legacy_sRGB()"))
		aw_color_menu_items.append(("AW Color/Legacy_Adobe98", "set_AW_COLOR_colorManagement_Legacy_Adobe98()"))
		aw_color_menu_items.append(("AW Color/Nuke-default", "set_AW_COLOR_colorManagement_nukeDefault()"))
		for name, choice in aw_color_menu_items:
			nuke.menu('Nuke').addCommand(name, choice)
except Exception:
	print "ERROR: Unable to add the AW_COLOR_TOOLS menus!"
	nuke.critical("Unable to add the AW_COLOR_TOOLS menus!")

	
##-------------------------------------------------------------------
## Handy Web Links, including the AW Wiki...
##-------------------------------------------------------------------
import webbrowser
urls = []
urls.append(("Weblinks/AW Wiki", "http://wiki.armstrong-white.com/mediawiki/index.php/Main_Page"))
urls.append(("Weblinks/Guidelines: Monitor Calibration", "http://wiki.armstrong-white.com/mediawiki/index.php/Guidelines:Monitor_Calibration"))
urls.append(("Weblinks/Guidelines: Working With Views", "http://wiki.armstrong-white.com/mediawiki/index.php/Dept:Compositing_Nuke_Working_With_Views"))
urls.append(("Weblinks/Nukepedia", "http://nukepedia.com/"))
for title, url in urls:
	nuke.menu('Nuke').addCommand(title, "webbrowser.open('{url}')".format(url=url))
##-------------------------------------------------------------------

#Animation Graph Menu
nuke.menu('Animation').addCommand('Bookend', "import Nuke_Scripts.KnobFns.bookend\nNuke_Scripts.KnobFns.bookend.bookend()")

try:
	import geometry.commands
	geometry.commands.setupNodes(nuke.menu('Nodes').addMenu('Geometry'))
except:
	print "Did Not Import Geometry Tools Menu"

try:
	import J_Ops.menu
except:
	print "Did Not Import J_Ops Menu"

try:
	import cryptomatte_utilities
	cryptomatte_utilities.setup_cryptomatte_ui()
except:
	print "Did Not Import cryptomatte Menu"

try:
	menu = nuke.menu('Nodes')
	subMenu = menu.addMenu("V-Ray Tools", icon = "VRayTools.png")
	subMenu.addCommand('VRayDenoiser', 'nuke.createNode("VRayDenoiser")', icon = "VRayDenoiser.png")
except:
	print "Did Not create V-Ray Menu"
	
try:
	#os.sys.path.append(os.environ["USER_TOOLS_DIR"])
	os.sys.path.append(os.environ["NUKE_USER_TOOLS_DIR"])
	import UserTools
	nukescripts.executeDeferred(UserTools.pythonScripts)
except:
	pass

##-------------------------------------------------------------------
#### NOTE:
#### All of the sRGB ICC Profile previewing tools are built into the new system
#### and accessed via the main menu, 'AW Color'...  RKB 10/11/17

#### UPDATE:
#### New Reinhard Viewer Process node - RKB 06/01/18 
try:
	os.sys.path.append(os.environ["NUKE_USER_TOOLS_DIR"])
	import Reinhard_Preview_Tools.Photoshop_Reinhard_Preview_Tools
	# Add button to Nuke Toolbar
	if os.name == 'nt':
		toolbar = nuke.toolbar("Nodes")
		toolbar.addCommand("Reinhard Workflow", "Reinhard_Preview_Tools.Photoshop_Reinhard_Preview_Tools.start()", icon = os.path.join(os.environ['NUKE_USER_TOOLS_DIR'], "Rich", "Reinhard_Preview_Tools", "Reinhard_ICON_24px.png").replace('\\', '/'))
	elif os.name =='posix':
		toolbar = nuke.toolbar("Nodes")
		toolbar.addCommand("Reinhard Workflow", "Reinhard_Preview_Tools.Photoshop_Reinhard_Preview_Tools.start()", icon = os.path.join(os.environ['NUKE_USER_TOOLS_DIR'], "Rich", "Reinhard_Preview_Tools", "Reinhard_ICON_24px.png"))  
except:
	pass

##-------------------------------------------------------------------
#### NOTE:
#### Added Back In Nuke Will Now Generate The Gizmos Menu At Startup
try:
	import Nuke_Scripts.SystemFns.paths
	Nuke_Scripts.SystemFns.paths.generate_Gizmo_Menu()
except:
	pass
AW_ASSET_ASSEMBLY_SYSTEM_MENU = nuke.menu("Nuke").addMenu("Asset Assembly System")
AW_ASSET_ASSEMBLY_SYSTEM_MENU.addCommand("Initialize System","if not os.path.join(System_Paths.AW_COMMON_UTILITIES,'Other') in os.sys.path:\n\tos.sys.path.append(os.path.join(System_Paths.AW_COMMON_UTILITIES,'Other'))\nimport AW_Asset_Assembly_System.Simple_Main_Window\nprop_pan = nuke.getPaneFor('Properties.1')\nAW_Asset_Assembly_System.Simple_Main_Window.Global_Nuke_Pan.addToPane(prop_pan)")


##-------------------------------------------------------------------
#### Add Hotkey to create a new Shuffle node in the Node Graph...
nuke.menu('Nodes').addCommand('@;Shuffle', 'nuke.createNode(\'Shuffle\')', 'h', shortcutContext=2)
nuke.menu('Nodes').addCommand('@;ShuffleBranch', 'nuke.createNode(\'Shuffle\')', '+h', shortcutContext=2)


try:
	import Nuke_Scripts.ChannelFns.channel_hotbox
	nuke.menu("Nuke").findItem("Edit").addCommand("HotBox", 'Nuke_Scripts.ChannelFns.channel_hotbox.start()', "alt+q")
except:
	pass

try:
	from DML_Tools.menu import *
except:
	print "Could Not Import DML_Tools menu"

#Gimp_menu = AW_TOOLS_MENU.addMenu("Gimped To PSD Nodes")
#Gimp_menu.addCommand("Master Layer Order",'nuke.createNode("DML_Master_Layer_Order")')
#Gimp_menu.addCommand("Layers To PSD",'nuke.createNode("DML_Layers_To_Gimped_PSD")')
#Gimp_menu.addCommand("Layer Order Builder",'nuke.createNode("DML_Layer_Order_Builder")')