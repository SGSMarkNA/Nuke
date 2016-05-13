import Node

class Group(Node.Node):

	def __init__(self,node):
		Node.Node.__init__(self,node)

	@property
	def begin(self):
		"""self.begin() -> Group. All python code that follows will be executed in the context of node. All names are evaluated relative to this object. Must be paired with end. @return: Group."""
		return self_node.begin()

	@property
	def numNodes(self):
		"""self.numNodes() -> Number of nodes Number of nodes in group. @return: Number of nodes"""
		return self_node.numNodes()

	@property
	def selectedNode(self):
		"""self.selectedNode() -> Node or None. Returns the node the user is most likely thinking about. This is the last node the user clicked on, if it is selected.  Otherwise it is an 'output' (one with no selected outputs) of the set of selected nodes. If no nodes are selected then None is returned. @return: Node or None."""
		return self_node.selectedNode()

	@property
	def selectedNodes(self):
		"""self.selectedNodes() -> Node or None. Selected nodes. @return: Node or None."""
		return self_node.selectedNodes()

	@property
	def output(self):
		"""self.output() -> Node or None. Return output node of group. @return: Node or None."""
		return self_node.output()

	@property
	def expand(self):
		"""self.expand() -> None. Moves all nodes from the group node into its parent group, maintaining node input and output connections, and deletes the group. Returns the nodes that were moved, which will also be selected. @return: None."""
		return self_node.expand()

	@property
	def end(self):
		"""self.end() -> None. All python code that follows will no longer be executed in the context of node. Must be paired with begin. @return: None."""
		return self_node.end()

	@property
	def nodes(self):
		"""self.nodes() -> List of nodes List of nodes in group. @return: List of nodes"""
		return self_node.nodes()

	#def node(self,s):
	#    """self.node(s) -> Node with name s or None. Locate a node by name. @param s: A string. @return: Node with name s or None."""
	#    return self_node.node(s)
	#
	#def connectSelectedNodes(self):
	#    """self.connectSelectedNodes(backward, inputA) -> None. Connect the selected nodes. @param backward. @param inputA. @return: None."""
	#    return self_node.connectSelectedNodes()
	#
	#def splaySelectedNodes(self):
	#    """self.splaySelectedNodes(backward, inputA) -> None. Splay the selected nodes. @param backward. @param inputA. @return: None."""
	#    return self_node.splaySelectedNodes()