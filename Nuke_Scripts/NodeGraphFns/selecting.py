
try :
	import nuke
except ImportError:
	nuke = None
	
from . import hierarchy
def get_everything_selected(*args,**kargs):
	nodeList = kargs.get("nodelist",[])
	group    = kargs.get("group",nuke.root())
	
	for n in group.selectedNodes():
		nodeList.append(n)
	
	groups = [i for i in group.nodes() if i.Class() == 'Group']
	
	for i in groups:
		get_everything_selected(group=i,nodelist=nodeList)
	return nodeList

def deselect_selected():
	try:
		for n in nuke.thisGroup().selectedNodes():
			n.setSelected(False)
	except:
		pass

def select_nodes(nodeList):
	for n in nodeList:
		n.setSelected(True)

def deselect_nodes(nodeList):
	for n in nodeList:
		n.setSelected(False)

def select_replace_nodes(nodeList):
	deselect_everything()
	select_nodes(nodeList)

def deselect_everything(group=None):
	if group == None:
		group=nuke.root()
	for n in group.nodes():
		n.setSelected(False)
		
	if isinstance(group,nuke.Node):
		try:
			for grp in nuke.allNodes("Group",group):
				deselect_everything(grp)
		except:
			pass

def select_trunks():
	deselect_selected()
	[n.setSelected(True) for n in hierarchy.trunk_nodes()]

def select_orphans():
	deselect_selected()
	[n.setSelected(True) for n in hierarchy.orphan_nodes()]

def select_leafs():
	deselect_selected()
	[n.setSelected(True) for n in hierarchy.leaf_nodes()]

