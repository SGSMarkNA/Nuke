try :
	import nuke
except ImportError:
	nuke = None
	
from Nuke_Scripts.NodeGraphFns import selecting
from Nuke_Scripts.KnobFns import copying
#===============================================================================
def declone(node):
	if node.clones() == 0:
		return
	opts = nuke.WRITE_ALL | nuke.WRITE_USER_KNOB_DEFS | nuke.TO_SCRIPT
	args = node.writeKnobs(opts)
	newnode = nuke.createNode(node.Class(), knobs = args,inpanel=False)
	nuke.inputs(newnode, nuke.inputs(node))
	num_inputs = nuke.inputs(node)
	for i in range(num_inputs):
		newnode.setInput(i, node.input(i))
	node.setInput(0, newnode)
	nuke.delete(node)
	return newnode
#===============================================================================
def multi_declone():
	grp = nuke.thisGroup()
	if isinstance(grp,str):
		grp = nuke.toNode(grp)

	if not grp.Class() in ["Root","Group"]:
		nuke.message("While Runing DML_declone "+
				     "the string value for the "+
				     "group node was not a Group")
		raise TypeError

	selnodes = grp.selectedNodes()

	selecting.deselect_everything()

	locationNode = nuke.createNode("NoOp","",False)
	locationNode.setSelected(False)
	for i in range(len(selnodes)):
		if selnodes[i].clones():
			copying.copy_xy_pos(selnodes[i],locationNode)

			selnodes[i].setSelected(True)
			selnodes[i] = declone(selnodes[i])
			selnodes[i].setSelected(False)

			copying.copy_xy_pos(locationNode,selnodes[i])

	nuke.delete(locationNode)

	selecting.select_nodes(selnodes)