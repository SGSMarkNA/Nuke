import nuke
import nukescripts
import os

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


# Handy Web Links, including the AW Wiki...
import webbrowser

urls = []
urls.append(("AW Weblinks/AW Wiki", "http://wiki.armstrong-white.com/"))

for title, url in urls:
	nuke.menu('Nuke').addCommand(title, "webbrowser.open('{url}')".format(url=url))


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
	#os.sys.path.append(os.environ["USER_TOOLS_DIR"])
	os.sys.path.append(os.environ["NUKE_USER_TOOLS_DIR"])
	import UserTools
	nukescripts.executeDeferred(UserTools.pythonScripts)
except:
	pass

try:
	os.sys.path.append(os.environ["NUKE_USER_TOOLS_DIR"])
	import sRGB_Preview_Tools.Photoshop_sRGB_Preview_Tools
	# Add button to Nuke Toolbar
	if os.name == 'nt':
		toolbar = nuke.toolbar("Nodes")
		toolbar.addCommand("sRGB Workflow", "sRGB_Preview_Tools.Photoshop_sRGB_Preview_Tools.start()", icon = os.path.join(os.environ['NUKE_USER_TOOLS_DIR'], "Rich", "sRGB_Preview_Tools", "sRGB_Icon.png").replace('\\', '/'))
	elif os.name =='posix':
		toolbar = nuke.toolbar("Nodes")
		toolbar.addCommand("sRGB Workflow", "sRGB_Preview_Tools.Photoshop_sRGB_Preview_Tools.start()", icon = os.path.join(os.environ['NUKE_USER_TOOLS_DIR'], "Rich", "sRGB_Preview_Tools", "sRGB_Icon.png"))  
except:
	pass
