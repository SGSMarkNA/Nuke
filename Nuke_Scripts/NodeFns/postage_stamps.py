try:
	import nuke
except ImportError:
	nuke = None

def postage_stamps_setter(*args,**kwargs):
	nodeList = list()
	group    = nuke.thisGroup().begin()

	nodeType = kwargs.get("type", kwargs.get("typ",None))
	switch   = kwargs.get("switch", kwargs.get("sw",False))
	selected = kwargs.get("selected", kwargs.get("sel",False))

	if selected:
		#Get selection of users working nodes
		for n in nuke.selectedNodes():
			if nodeType:
				if n.Class() == nodeType:
					nodeList.append(n)
			else:
				nodeList.append(n)
	else:
		#Get All nodes in Group
		for n in nuke.allNodes(group=group):
			if nodeType:
				if n.Class() == nodeType:
					nodeList.append(n)
			else:
				nodeList.append(n)
	for n in nodeList:
		if "postage_stamp" in n.knobs().keys():
			if switch:
				n.knob("postage_stamp").setValue(True)
			else:
				n.knob("postage_stamp").setValue(False)
	group.end()