try:
	import nuke
except ImportError:
	nuke = None

from Nuke_Scripts.NodeGraphFns import placement, selecting, transforms
def create_Side_Dots(nodelist=None):
	if nodelist is None:
		nodelist = nuke.selectedNodes()
	alldots = []
	nodelist = placement.reorder_from_top_to_bottom(nodelist)
	topDot = None
	returnDot = None
	selecting.deselect_everything()
	for n in nodelist:
		dot = nuke.nodes.Dot()
		dot.setXpos(n.xpos()-300)
		dot.setYpos(n.ypos())
		n.setInput(0,dot)
		if not topDot == None:
			dot.setInput(0,topDot)
		else:
			returnDot = dot
		topDot = dot
		alldots.append(dot)
	transforms.aline_horizontal_avarage(nodes=alldots)
	return returnDot