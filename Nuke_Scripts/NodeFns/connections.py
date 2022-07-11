try:
	import nuke
except ImportError:
	nuke = None
	
def remove_inputs():
	nodes = nuke.selectedNodes()
	for i in nodes:
		for j in range(i.inputs()):
			i.setInput(j, None)
#===============================================================================
def multi_output_connect():
	nodeList = nuke.selectedNodes()
	for i in range(1, len(nodeList), 1):
		nodeList[i].connectInput(i, nodeList[0])
#===============================================================================
def multi_input_connect():
	nodeList = nuke.selectedNodes()
	for i in reversed(list(range(1, len(nodeList), 1))):
		nodeList[0].setInput(i-1, nodeList[i])