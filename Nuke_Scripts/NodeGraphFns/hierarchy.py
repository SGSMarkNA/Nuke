try :
	import nuke
except ImportError:
	nuke = None

from . import node_filters

def recursiveFindNodes(nodeClass, startNode):
	if startNode.Class() == nodeClass:
		yield startNode
	elif isinstance(startNode, nuke.Group):
		for child in startNode.nodes():
			for foundNode in recursiveFindNodes(nodeClass, child):
				yield foundNode

def orphan_nodes():
	nodes = []
	allNodes = nuke.allNodes()
	for nod in allNodes:
		if not len(nod.dependent()) and not len(nod.dependencies()):
			nodes.append(nod)
	nodes = node_filters.filter_remove_node_class(nodes,("BackdropNode","StickyNote"))
	return nodes


def trunk_nodes():
	nodes = []
	orphans  = orphan_nodes()
	allNodes = nuke.allNodes()
	[allNodes.remove(n) for n in orphans]
	for nod in allNodes:
		if len(nod.dependent()) and not len(nod.dependencies()):
			nodes.append(nod)

	return nodes
#===============================================================================
def leaf_nodes(*args,**kwargs):
	"""Find And Return A List Of Nodes At The End Of A Chain Of Nodes
	*args = list of nodes
	**kwargs
		group    = thisGoup 'exacute this function within a spacific Group'
		selected = False 'exacute this function only one the Selected Nodes'
		all      = True 'exacute this function on all Nodes' default
	"""
	nodelist = []
	if len(args):
		nodelist = list(args)
	else:
		grp = kwargs.get("group", nuke.thisGroup() ).begin()
		if kwargs.get("selected",False):
			nodelist = nuke.selectedNodes()
		else:
			nodelist = nuke.allNodes()

	for node in orphan_nodes():
		if node in nodelist:
			nodelist.remove(node)

	for i,n in enumerate(nodelist):
		if n.inputs() and len(n.dependencies()):
			nodelist.append(n)

	return nodelist

#===============================================================================
def find_downstream_node_by_class( matchclass=None, startnode=None ):
	if matchclass == None:
		return None
	elif startnode == None:
		return None
	elif  startnode.Class() == matchclass:
		return startnode
	else:
		for node in startnode.dependent():
			return find_downstream_node_by_class( matchclass=matchclass, startnode=node )

def down_stream_nodes(nodes=None,nlist=None,stop_on_class=False):
	if nlist == None:
		nlist = []
	if nodes == None:
		nodes = nuke.selectedNodes()
	elif isinstance(nodes,nuke.Node):
		nlist.append(nodes)
		down_stream_nodes(nodes.dependent(),nlist,stop_on_class)
	if isinstance(nodes,list):
		for n in nodes:
			nlist.append(n)
			if stop_on_class:
				if n.Class() == stop_on_class:
					return nlist
			others = n.dependent()
			if len(others):
				down_stream_nodes(others,nlist,stop_on_class)
	return nlist
#===============================================================================
def find_upstream_node( matchclass=None, startnode=None ):
	"""
	In the simplest way possible, this function will go upstream and find
	the first node matching the specified class.
	"""

	if matchclass == None:
		return None
	elif startnode == None:
		return None
	elif  startnode.Class() == matchclass:
		return startnode
	else:
		return find_upstream_node( matchclass=matchclass, startnode=startnode.input( 0 ) )
#===============================================================================
def up_stream_nodes(nodes=None,nlist=None):
	if nlist == None:
		nlist = []
	if nodes == None:
		nodes = nuke.selectedNodes()
	elif isinstance(nodes,nuke.Node):
		up_stream_nodes(nodes.dependencies(),nlist)
	if isinstance(nodes,list):
		for n in nodes:
			nlist.append(n)
			if n.inputs():
				up_stream_nodes(n.dependencies(),nlist)
	return nlist

class NodeDagPaths:
	def __init__(self):
		self.tabs = 0
		self.start()
	def PrintNode(self,node):
		print("\t"*self.tabs+node.fullName())

	def start(self):
		trunkNodes = trunk_nodes()

		for node in trunkNodes:
			self.PrintNode(node)
			self.tabs += 1
			self.traversNodes(node)
	def traversNodes(self,node):
		for child in node.dependent():

			self.tabs += 1

			self.PrintNode(child)

			self.traversNodes(child)

			self.tabs -= 1


