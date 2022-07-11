#!/usr/bin/env python
import nuke
#----------------------------------------------------------------------
def flatten(x):
	result = []
	for el in x:
		if hasattr(el, "__iter__") and not isinstance(el, str):
			result.extend(flatten(el))
		else:
			result.append(el)
	return result
#----------------------------------------------------------------------
def get_nukeNode(node):
	"""if the node is a wrapper class the the real node otherwise returns the input node"""
	if hasattr(node,"_nukeNode"):
		return node._nukeNode
	return node
#----------------------------------------------------------------------
def get_nukeNode_list(*args):
	"""returns the A Node list Containing no wrappers"""
	return [get_nukeNode(node) for node in flatten(*args)]
#----------------------------------------------------------------------
def get_Node(node):
	res =  Node(node)
	return res
#----------------------------------------------------------------------
def get_Nodes(*args):
	return [Node(node) for node in flatten(*args)]

################################################################################
class Knob_Assessor(object):
	def __init__(self, data):
		for key, value in data.items():
			key = "".join([k for k in list(key) if not k in invalid_chars])
			key = str("n_" + key) if key[0] in string_digits else key
			if isinstance(value, dict):
				self.__dict__[key] = Knob_Assessor(value)
			elif isinstance(value, list):
				new_val = []
				for val in value:
					if isinstance(val, dict):
						val = Knob_Assessor(val)
					new_val.append(val)
				self.__dict__[key] = new_val
			else:
				self.__dict__[key] = value
################################################################################
class NukeNode(object):
	"""Wrapper class for a nuke Node type"""
	#----------------------------------------------------------------------
	def __init__(self,*args,**kwargs):
		fn = getattr(nuke.nodes,self.__class__.__name__)
		self._nukeNode = None
		if len(args):
			if isinstance(args[0],str):
				fn = getattr(nuke.nodes,args[0])

			elif isinstance(args[0],nuke.Node):
				self._nukeNode = args[0]

			elif isinstance(args[0],NukeNode):
				self._nukeNode = args[0]._nukeNode

		if self._nukeNode == None:
			node_name = kwargs.get("name","")
			node = nuke.toNode(node_name)
			if node != None:
				self._nukeNode = node

		if self._nukeNode == None:
			if "inputs" in kwargs:
				kwargs["inputs"]=get_nukeNode_list(kwargs["inputs"])
			self._nukeNode = fn(**kwargs)
	#----------------------------------------------------------------------
	def __getattribute__(self,name):
		try:
			return super(NukeNode,self).__getattribute__(name)
		except:
			obj = super(NukeNode,self).__getattribute__("_nukeNode")
			if hasattr(obj,name):
				return getattr(obj,name)
			else:
				return object.__getattribute__(self,name)

	def __repr__(self):
		return "Nuke_Scripts.NukeNode(%s,%r)" % (self._nukeNode.Class,self._nukeNode.knobs())
	#@property
	#def nodeKnobs(self):
		#return Knob_Assessor(super(NukeNode,self).__getattribute__("_nukeNode"))
################################################################################
################################################################################ Nodes Class's
################################################################################
class Node(NukeNode):
	#----------------------------------------------------------------------
	def Disconnect_All_Dependencies(self):
		""""""
		while len(self._nukeNode.dependencies()):
			for i in range(self.inputs):
				self.setInput(i, None)
	def Disconnect_All_Dependent(self):
		for n in self.dependent():
			for i in range(n.inputs()):
				if n.input(i) == n:
					n.setInput(i,None)
	#----------------------------------------------------------------------
	def getNumKnobs(self):
		"""self.numKnobs() -> The number of knobs. @return: The number of knobs."""
		return self._nukeNode.getNumKnobs()
	#----------------------------------------------------------------------
	def writeKnobs(self,i):
		"""self.writeKnobs(i) -> String in .nk form. Return a tcl list. If TO_SCRIPT | TO_VALUE is not on, this is a simple list of knob names. If it is on, it is an alternating list of knob names and the output of to_script().  Flags can be any of these or'd together: - nuke.TO_SCRIPT produces to_script(0) values - nuke.TO_VALUE produces to_script(context) values - nuke.WRITE_NON_DEFAULT_ONLY skips knobs with not_default() false - nuke.WRITE_USER_KNOB_DEFS writes addUserKnob commands for user knobs - nuke.WRITE_ALL writes normally invisible knobs like name, xpos, ypos  @param i: The set of flags or'd together. Default is TO_SCRIPT | TO_VALUE. @return: String in .nk form."""
		return self._nukeNode.writeKnobs(i)
	#----------------------------------------------------------------------
	def autoplace(self):
		"""self.autoplace() -> None. Automatically place nodes, so they do not overlap. @return: None."""
		return self._nukeNode.autoplace()
	#----------------------------------------------------------------------
	def forceValidate(self):
		"""self.forceValidate() -> None  Force the node to validate itself, updating its hash."""
		return self._nukeNode.forceValidate()
	#----------------------------------------------------------------------
	def help(self):
		"""self.help() -> str @return: Help for the node."""
		return self._nukeNode.help()
	#----------------------------------------------------------------------
	def lastFrame(self):
		"""self.lastFrame() -> int. Last frame in frame range for this node. @return: int."""
		return self._nukeNode.lastFrame()
	#----------------------------------------------------------------------
	def setSelected(self,selected):
		"""self.setSelected(selected) -> None. Set the selection state of the node.  This is the same as changing the 'selected' knob. @param selected: New selection state - True or False. @return: None."""
		return self._nukeNode.setSelected(selected)
	#----------------------------------------------------------------------
	def treeHasError(self):
		"""treeHasError() -> bool True if the node or any in its input tree have an error, or False otherwise.  Error state of the node and its input tree. Note that this will always return false for viewers, which cannot generate their input trees.  Instead, choose an input of the viewer (e.g. the active one), and call treeHasError() on that."""
		return self._nukeNode.treeHasError()
	#----------------------------------------------------------------------
	@property
	def maximumInputs(self):
		"""self.maximumInputs() -> Maximum number of inputs this node can have. @return: Maximum number of inputs this node can have."""
		return self._nukeNode.maximumInputs()
	#----------------------------------------------------------------------
	def hasError(self):
		"""hasError() -> bool True if the node itself has an error, regardless of the state of the ops in its input tree, or False otherwise.  Error state of the node itself, regardless of the state of the ops in its input tree. Note that an error on a node may not appear if there is an error somewhere in its input tree, because it may not be possible to validate the node itself correctly in that case."""
		return self._nukeNode.hasError()
	#----------------------------------------------------------------------
	def deepSample(self):
		"""self.deepSample(c, x, y, n) -> Floating point value. Return pixel values from a deep image. This requires the image to be calculated, so performance may be very bad if this is placed into an expression in a control panel. @param c: Channel name. @param x: Position to sample (X coordinate). @param y: Position to sample (Y coordinate). @param n: Sample index (between 0 and the number returned by deepSampleCount() for this pixel, or -1 for the frontmost). @return: Floating point value."""
		return self._nukeNode.deepSample()
	#----------------------------------------------------------------------
	@property
	def height(self):
		"""self.height() -> int. Height of the node. @return: int."""
		return self._nukeNode.height()
	#----------------------------------------------------------------------
	def sample(self,*args,**kwargs):
		"""self.sample(c, x, y, dx, dy) -> Floating point value.

			Return pixel values from an image.
			This requires the image to be calculated.
			Performance may be very bad if this is placed into an expression in a control panel.
			Produces a cubic filtered result.
			Any sizes less than 1, including 0, produce the same filtered result,
			this is correct based on sampling theory.
			Note that integers are at the corners of pixels,
			to center on a pixel add .5 to both coordinates.
			If the optional dx,dy are not given
			then the exact value of the square pixel that x,y lands in is returned.
			This is also called 'impulse filtering'.

			@param c: Channel name.
			@param x: Centre of the area to sample (X coordinate).
			@param y: Centre of the area to sample (Y coordinate).
			@param dx: Optional size of the area to sample (X coordinate).
			@param dy: Optional size of the area to sample (Y coordinate).
			@param frame: Optional frame to sample the node at.
			@return: Floating point value.
		"""
		return self._nukeNode.sample(*args,**kwargs)

	#----------------------------------------------------------------------
	def setInput(self, i, node):
		"""self.setInput(i, node) -> bool

		Connect input i to node if canSetInput() returns true.

		@param i: Input number.
		@param node: The node to connect to input i.
		@return: True if canSetInput() or if the input is already correct.
		"""
		return self._nukeNode.setInput(i,get_nukeNode(node))
	#----------------------------------------------------------------------
	def dependencies(self,*args):
		"""self.dependencies(what) -> List of nodes.

		List all nodes referred to by this node.
		'what' is an optional integer (see below).
		You can use the following constants
		to select what types of dependencies are looked for:

		nuke.EXPRESSIONS = expressions
		nuke.INPUTS = visible input pipes
		nuke.HIDDEN_INPUTS = hidden input pipes.
		The default is to look for all types of connections.
		Example: nuke.toNode('Blur1').dependencies( nuke.INPUTS | nuke.EXPRESSIONS )
		@param what: Or'ed constant of nuke.EXPRESSIONS, nuke.INPUTS and nuke.HIDDEN_INPUTS
		to select the types of dependencies.
		The default is to look for all types of connections.
		@return: List of nodes.
		"""
		return self._nukeNode.dependencies(*args)
	#----------------------------------------------------------------------
	def canSetInput(self, i, node):
		"""self.canSetInput(i, node) -> bool

		Check whether the output of 'node'
		can be connected to input i.
		@param i: Input number.
		@param node: The node to be connected to input i.
		@return: True if node can be connected, False otherwise.
		"""
		return self._nukeNode.canSetInput(i, get_nukeNode(node))
	#----------------------------------------------------------------------
	def maximumOutputs(self):
		"""self.maximumOutputs() -> Maximum number of outputs this node can have. @return: Maximum number of outputs this node can have."""
		return self._nukeNode.maximumOutputs()
	#----------------------------------------------------------------------
	def screenWidth(self):
		"""self.screenWidth() -> int. Width of the node when displayed on screen in the DAG, at 1:1 zoom, in pixels. @return: int."""
		return self._nukeNode.screenWidth()
	#----------------------------------------------------------------------
	def linkableKnobs(self,knobType):
		"""self.linkableKnobs(knobType) -> List  Returns a list of any knobs that may be linked to from the node as well as some meta information about the knob. This may include whether the knob is enabled and whether it should be used for absolute or relative values. Not all of these variables may make sense for all knobs.. @param knobType A KnobType describing the type of knobs you want.@return: A list of LinkableKnobInfo that may be empty ."""
		return self._nukeNode.linkableKnobs(knobType)
	#----------------------------------------------------------------------
	@property
	def minimumInputs(self):
		"""self.minimumInputs() -> Minimum number of inputs this node can have. @return: Minimum number of inputs this node can have."""
		return self._nukeNode.minimumInputs()
	#----------------------------------------------------------------------
	def firstFrame(self):
		"""self.firstFrame() -> int. First frame in frame range for this node. @return: int."""
		return self._nukeNode.firstFrame()
	#----------------------------------------------------------------------
	def setXpos(self,x):
		"""self.setXpos(x) -> None. Set the x position of node in node graph. @param x: The x position of node in node graph. @return: None."""
		return self._nukeNode.setXpos(x)
	#----------------------------------------------------------------------
	def shown(self):
		"""self.shown() -> true if the properties panel is open. This can be used to skip updates that are not visible to the user. @return: true if the properties panel is open. This can be used to skip updates that are not visible to the user."""
		return self._nukeNode.shown()
	#----------------------------------------------------------------------
	@property
	def numKnobs(self):
		"""self.numKnobs() -> The number of knobs. @return: The number of knobs."""
		return self._nukeNode.numKnobs()
	#----------------------------------------------------------------------
	@property
	def maxInputs(self):
		"""self.maximumInputs() -> Maximum number of inputs this node can have. @return: Maximum number of inputs this node can have."""
		return self._nukeNode.maxInputs()
	#----------------------------------------------------------------------
	@property
	def isSelected(self):
		"""self.isSelected() -> bool  Returns the current selection state of the node.  This is the same as checking the 'selected' knob. @return: True if selected, or False if not."""
		return self._nukeNode.isSelected()
	#----------------------------------------------------------------------
	def setYpos(self,y):
		"""self.setYpos(y) -> None. Set the y position of node in node graph. @param y: The y position of node in node graph. @return: None."""
		return self._nukeNode.setYpos(y)
	#----------------------------------------------------------------------
	def showControlPanel(self,forceFloat = False):
		"""self.showControlPanel(forceFloat = false) -> None @param forceFloat: Optional python object. If it evaluates to True the control panel will always open as a floating panel. Default is False. @return: None"""
		return self._nukeNode.showControlPanel(forceFloat = forceFloat)
	#----------------------------------------------------------------------
	@property
	def width(self):
		"""self.width() -> int. Width of the node. @return: int."""
		return self._nukeNode.width()
	#----------------------------------------------------------------------
	def connectInput(self,i, node):
		"""self.connectInput(i, node) -> bool

		Connect the output of 'node' to the i'th input or the next available unconnected input.
		The requested input is tried first,
		but if it is already set then subsequent inputs are tried until an unconnected one is found,
		as when you drop a connection arrow onto a node in the GUI.
		@param i: Input number to try first.
		@param node: The node to connect to input i.
		@return: True if a connection is made, False otherwise."""
		return self._nukeNode.connectInput(i, get_nukeNode(node))
	#----------------------------------------------------------------------
	def allKnobs(self):
		"""self.allKnobs() -> dict

		Get a list of all knobs in this node,
		including nameless knobs.
		@return: List of all knobs.
		Note that this doesn't follow the links for Link_Knobs"""
		return self._nukeNode.allKnobs()
	##----------------------------------------------------------------------
	#def deepSampleCount(self):
		#"""self.deepSampleCount(x, y) -> Integer value. Return number of samples for a pixel on a deep image. This requires the image to be calculated, so performance may be very bad if this is placed into an expression in a control panel. @param x: Position to sample (X coordinate). @param y: Position to sample (Y coordinate). @return: Integer value."""
		#return self._nukeNode.deepSampleCount()
	#----------------------------------------------------------------------
	def removeKnob(self,k):
		"""self.removeKnob(k) -> None. Remove knob k from this node or panel. Throws a ValueError exception if k is not found on the node. @param k: Knob. @return: None."""
		return self._nukeNode.removeKnob(k)
	#----------------------------------------------------------------------
	def input(self,i):
		"""self.input(i) -> The i'th input. @param i: Input number. @return: The i'th input."""
		return self._nukeNode.input(i)
	#----------------------------------------------------------------------
	def knobs(self):
		"""self.knobs() -> dict  Get a dictionary of (name, knob) pairs for all knobs in this node.  For example:     >>> b = nuke.nodes.Blur()    >>> b.knobs()  @return: Dictionary of all knobs.  Note that this doesn't follow the links for Link_Knobs"""
		res = self._nukeNode.knobs()
		isinstance(res, dict)
		return res
	#----------------------------------------------------------------------
	@property
	def Class(self):
		"""self.Class() -> Class of node. @return: Class of node."""
		return self._nukeNode.Class()
	#----------------------------------------------------------------------
	def maxOutputs(self):
		"""self.maximumOutputs() -> Maximum number of outputs this node can have. @return: Maximum number of outputs this node can have."""
		return self._nukeNode.maxOutputs()
	#----------------------------------------------------------------------
	def metadata(self):
		"""self.metadata(key, time, view) -> value or dict Return the metadata item for key on this node at current output context, or at optional time and view. If key is not specified a dictionary containing all key/value pairs is returned. None is returned if key does not exist on this node. @param key: Optional name of the metadata key to retrieve. @param time: Optional time to evaluate at (default is taken from node's current output context). @param view: Optional view to evaluate at (default is taken from node's current output context). @return: The requested metadata value, a dictionary containing all keys if a key name is not provided, or None if the specified key is not matched."""
		return self._nukeNode.metadata()
	#----------------------------------------------------------------------
	def knob(self,p):
		"""self.knob(p) -> The knob named p or the pth knob. @param p: A string or an integer. @return: The knob named p or the pth knob.  Note that this follows the links for Link_Knobs"""
		return self._nukeNode.knob(p)
	#----------------------------------------------------------------------
	@property
	def inputs(self):
		"""self.inputs() -> Gets the maximum number of connected inputs. @return: Number of the highest connected input + 1. If inputs 0, 1, and 3 are connected, this will return 4."""
		return self._nukeNode.inputs()
	#----------------------------------------------------------------------
	def xpos(self):
		"""self.xpos() -> X position of node in node graph. @return: X position of node in node graph."""
		return self._nukeNode.xpos()
	#----------------------------------------------------------------------
	def setName(self, name):
		"""self.setName(name, uncollide=True, updateExpressions=False) -> None Set name of the node and resolve name collisions if optional named argument 'uncollide' is True. @param name: A string. @param uncollide: Optional boolean to resolve name collisions. Defaults to True. @param updateExpressions: Optional boolean to update expressions in other nodes to point at the new name. Defaults to False. @return: None"""
		return self._nukeNode.setName(name)
	#----------------------------------------------------------------------
	@property
	def format(self):
		"""self.format() -> Format. Format of the node. @return: Format."""
		return self._nukeNode.format()
	#----------------------------------------------------------------------
	def dependent(self,*args,**kwargs):
		"""self.dependent(what, forceEvaluate) -> List of nodes.
		List all nodes that read information from this node.
		'what' is an optional integer:
		You can use any combination of the following constants together
		to select what types of dependent nodes to look for:
		nuke.EXPRESSIONS = expressions
		nuke.INPUTS = visible input pipes
		nuke.HIDDEN_INPUTS = hidden input pipes.
		The default is to look for all types of connections.
		forceEvaluate is an optional boolean defaulting to True.
		When this parameter is true, it forces a re-evaluation of the entire tree.
		This can be expensive, but otherwise could give incorrect results if nodes are expression-linked.
		Example: nuke.toNode('Blur1').dependent( nuke.INPUTS | nuke.EXPRESSIONS )
		@param what: Or'ed constant of nuke.EXPRESSIONS, nuke.INPUTS and nuke.HIDDEN_INPUTS to select the types of dependent nodes. The default is to look for all types of connections. @param forceEvaluate: Specifies whether a full tree evaluation will take place. Defaults to True. @return: List of nodes."""
		return self._nukeNode.dependent(*args,**kwargs)
	#----------------------------------------------------------------------
	def setXYpos(self, x, y):
		"""self.setXYpos(x, y) -> None. Set the (x, y) position of node in node graph. @param x: The x position of node in node graph. @param y: The y position of node in node graph. @return: None."""
		return self._nukeNode.setXYpos(x, y)
	#----------------------------------------------------------------------
	def ypos(self):
		"""self.ypos() -> Y position of node in node graph. @return: Y position of node in node graph."""
		return self._nukeNode.ypos()
	#----------------------------------------------------------------------
	def running(self):
		"""self.running() -> Node rendering when paralled threads are running or None. Class method. @return: Node rendering when paralled threads are running or None."""
		return self._nukeNode.running()
	#----------------------------------------------------------------------
	def pixelAspect(self):
		"""self.pixelAspect() -> int. Pixel Aspect ratio of the node. @return: float."""
		return self._nukeNode.pixelAspect()
	#----------------------------------------------------------------------
	def proxy(self):
		"""self.proxy() -> bool @return: True if proxy is enabled, False otherwise."""
		return self._nukeNode.proxy()
	#----------------------------------------------------------------------
	@property
	def clones(self):
		"""self.clones() -> Number of clones. @return: Number of clones."""
		return self._nukeNode.clones()
	#----------------------------------------------------------------------
	@property
	def fullName(self):
		"""self.fullName() -> str Get the name of this node and any groups enclosing it in 'group.group.name' form. @return: The fully-qualified name of this node, as a string."""
		return self._nukeNode.fullName()
	#----------------------------------------------------------------------
	def resetKnobsToDefault(self):
		"""self.resetKnobsToDefault() -> None  Reset all the knobs to their default values."""
		return self._nukeNode.resetKnobsToDefault()
	#----------------------------------------------------------------------
	def channels(self):
		"""self.channels() -> String list. List channels output by this node. @return: String list."""
		return self._nukeNode.channels()
	#----------------------------------------------------------------------
	def showInfo(self,s):
		"""self.showInfo(s) -> None. Creates a dialog box showing the result of script s. @param s: A string. @return: None."""
		return self._nukeNode.showInfo(s)
	#----------------------------------------------------------------------
	def selectOnly(self):
		"""self.selectOnly() -> None. Set this node to be the only selection, as if it had been clicked in the DAG. @return: None."""
		return self._nukeNode.selectOnly()
	#----------------------------------------------------------------------
	def name(self):
		"""self.name() -> str @return: Name of node."""
		return self._nukeNode.name()
	#----------------------------------------------------------------------
	def minInputs(self):
		"""self.minimumInputs() -> Minimum number of inputs this node can have. @return: Minimum number of inputs this node can have."""
		return self._nukeNode.minInputs()
	#----------------------------------------------------------------------
	def hideControlPanel(self):
		"""self.hideControlPanel() -> None @return: None"""
		return self._nukeNode.hideControlPanel()
	#----------------------------------------------------------------------
	def optionalInput(self):
		"""self.optionalInput() -> Number of first optional input. @return: Number of first optional input."""
		return self._nukeNode.optionalInput()
	#----------------------------------------------------------------------
	def screenHeight(self):
		"""self.screenHeight() -> int. Height of the node when displayed on screen in the DAG, at 1:1 zoom, in pixels. @return: int."""
		return self._nukeNode.screenHeight()
	#----------------------------------------------------------------------
	def addKnob(self,k):
		"""self.addKnob(k) -> None. Add knob k to this node or panel. @param k: Knob. @return: None."""
		return self._nukeNode.addKnob(k)
	#----------------------------------------------------------------------
	def __len__(self):
		"""x.__len__() <==> len(x)"""
		return self._nukeNode.__len__()
	#----------------------------------------------------------------------
	def frameRange(self):
		"""self.frameRange() -> FrameRange. Frame range for this node. @return: FrameRange."""
		return self._nukeNode.frameRange()
	#----------------------------------------------------------------------
	def __repr__(self):
		"""x.__repr__() <==> repr(x)"""
		return self._nukeNode.__repr__()
	#----------------------------------------------------------------------
	def error(self):
		"""error() -> bool True if the node or any in its input tree have an error, or False otherwise.  Error state of the node and its input tree.  Deprecated; use hasError or treeHasError instead. Note that this will always return false for viewers, which cannot generate their input trees.  Instead, choose an input of the viewer (e.g. the active one), and call treeHasError() on that."""
		return self._nukeNode.error()
	#----------------------------------------------------------------------
	def redraw(self):
		"""self.redraw() -> None. Force a redraw of the node. @return: None."""
		return self._nukeNode.redraw()
	#----------------------------------------------------------------------
	def readKnobs(self,s):
		"""self.readKnobs(s) -> None. Read the knobs from a string (TCL syntax). @param s: A string. @return: None."""
		return self._nukeNode.readKnobs(s)
	#----------------------------------------------------------------------
	def bbox(self):
		"""self.bbox() -> List of x, y, w, h. Bounding box of the node. @return: List of x, y, w, h."""
		return self._nukeNode.bbox()
	def test(self):
		return "this is a test"
	x = property(xpos,setXpos)
	y = property(ypos,setYpos)
	node_name = property(name,setName)
################################################################################
class BackdropNode(Node):
	#----------------------------------------------------------------------
	def __getitem__(self,y):
		"""x.__getitem__(y) <==> x[y]"""
		return self._nukeNode.__getitem__(y)
	#----------------------------------------------------------------------
	def __str__(self):
		"""x.__str__() <==> str(x)"""
		return self._nukeNode.__str__()
	#----------------------------------------------------------------------
	def selectNodes(self):
		"""self.selectNodes(selectNodes) -> None Select or deselect all nodes in backdrop node Example: backdrop = nuke.toNode("BackdropNode1") backdrop.selectNodes(True)  @return: None."""
		return self._nukeNode.selectNodes()
	#----------------------------------------------------------------------
	def __repr__(self):
		"""x.__repr__() <==> repr(x)"""
		return self._nukeNode.__repr__()
	#----------------------------------------------------------------------
	def __len__(self):
		"""x.__len__() <==> len(x)"""
		return self._nukeNode.__len__()

################################################################################
class Group(Node):
	#----------------------------------------------------------------------
	def node(self,s):
		"""self.node(s) -> Node with name s or None. Locate a node by name. @param s: A string. @return: Node with name s or None."""
		return self._nukeNode.node(s)
	#----------------------------------------------------------------------
	def __exit__(self):
		""""""
		return self._nukeNode.__exit__()
	#----------------------------------------------------------------------
	@property
	def begin(self):
		"""self.begin() -> Group. All python code that follows will be executed in the context of node. All names are evaluated relative to this object. Must be paired with end. @return: Group."""
		return self._nukeNode.begin()
	#----------------------------------------------------------------------
	def run(self,callable):
		"""self.run(callable) -> Result of callable. Execute in the context of node. All names are evaluated relative to this object. @param callable: callable to execute. @return: Result of callable."""
		return self._nukeNode.run(callable)
	#----------------------------------------------------------------------
	def numNodes(self):
		"""self.numNodes() -> Number of nodes Number of nodes in group. @return: Number of nodes"""
		return self._nukeNode.numNodes()
	#----------------------------------------------------------------------
	def connectSelectedNodes(self):
		"""self.connectSelectedNodes(backward, inputA) -> None. Connect the selected nodes. @param backward. @param inputA. @return: None."""
		return self._nukeNode.connectSelectedNodes()
	#----------------------------------------------------------------------
	@property
	def selectedNode(self):
		"""self.selectedNode() -> Node or None. Returns the node the user is most likely thinking about. This is the last node the user clicked on, if it is selected.  Otherwise it is an 'output' (one with no selected outputs) of the set of selected nodes. If no nodes are selected then None is returned. @return: Node or None."""
		return self._nukeNode.selectedNode()
	#----------------------------------------------------------------------
	@property
	def selectedNodes(self):
		"""self.selectedNodes() -> Node or None. Selected nodes. @return: Node or None."""
		return self._nukeNode.selectedNodes()
	#----------------------------------------------------------------------
	def output(self):
		"""self.output() -> Node or None. Return output node of group. @return: Node or None."""
		return self._nukeNode.output()
	#----------------------------------------------------------------------
	def expand(self):
		"""self.expand() -> None. Moves all nodes from the group node into its parent group, maintaining node input and output connections, and deletes the group. Returns the nodes that were moved, which will also be selected. @return: None."""
		return self._nukeNode.expand()
	#----------------------------------------------------------------------
	@property
	def end(self):
		"""self.end() -> None. All python code that follows will no longer be executed in the context of node. Must be paired with begin. @return: None."""
		return self._nukeNode.end()
	#----------------------------------------------------------------------
	@property
	def nodes(self):
		"""self.nodes() -> List of nodes List of nodes in group. @return: List of nodes"""
		return self._nukeNode.nodes()
	#----------------------------------------------------------------------
	def splaySelectedNodes(self):
		"""self.splaySelectedNodes(backward, inputA) -> None. Splay the selected nodes. @param backward. @param inputA. @return: None."""
		return self._nukeNode.splaySelectedNodes()
	#----------------------------------------------------------------------
	def __len__(self):
		"""x.__len__() <==> len(x)"""
		return self._nukeNode.__len__()

################################################################################
class Gizmo(Group):
	def filename(self):
		"""self.filename() -> String. Gizmo filename. @return: String."""
		return self._nukeNode.filename()
	#----------------------------------------------------------------------
	def command(self):
		"""self.command() -> String. Gizmo command. @return: String."""
		return self._nukeNode.command()
	#----------------------------------------------------------------------
	def makeGroup(self):
		"""self.makeGroup() -> Group Creates a Group node copy of the Gizmo node. @return: Group."""
		return self._nukeNode.makeGroup()

################################################################################
class Precomp(Group):
	#----------------------------------------------------------------------
	def __getitem__(self,y):
		"""x.__getitem__(y) <==> x[y]"""
		return self._nukeNode.__getitem__(y)
	#----------------------------------------------------------------------
	def __str__(self):
		"""x.__str__() <==> str(x)"""
		return self._nukeNode.__str__()
	#----------------------------------------------------------------------
	def reload(self):
		"""self.reload() -> None Precomp Node reload() @return: None"""
		return self._nukeNode.reload()
	#----------------------------------------------------------------------
	def __repr__(self):
		"""x.__repr__() <==> repr(x)"""
		return self._nukeNode.__repr__()
	#----------------------------------------------------------------------
	def __len__(self):
		"""x.__len__() <==> len(x)"""
		return self._nukeNode.__len__()

################################################################################
class Root(Group):
	#----------------------------------------------------------------------
	def lastFrame(self):
		"""self.lastFrame() -> Integer. Last frame. @return: Integer."""
		return self._nukeNode.lastFrame()
	#----------------------------------------------------------------------
	def __str__(self):
		"""x.__str__() <==> str(x)"""
		return self._nukeNode.__str__()
	#----------------------------------------------------------------------
	def maximumInputs(self):
		""""""
		return self._nukeNode.maximumInputs()
	#----------------------------------------------------------------------
	def modified(self):
		"""self.modified() -> True if modified, False otherwise. Get or set the 'modified' flag in a script @return: True if modified, False otherwise."""
		return self._nukeNode.modified()
	#----------------------------------------------------------------------
	def channels(self):
		"""nuke.Root.channels() -> Channel list. Class method. @return: Channel list."""
		return self._nukeNode.channels()
	#----------------------------------------------------------------------
	def setInput(self):
		""""""
		return self._nukeNode.setInput()
	#----------------------------------------------------------------------
	def canSetInput(self):
		""""""
		return self._nukeNode.canSetInput()
	#----------------------------------------------------------------------
	def maximumOutputs(self):
		""""""
		return self._nukeNode.maximumOutputs()
	#----------------------------------------------------------------------
	def minimumInputs(self):
		""""""
		return self._nukeNode.minimumInputs()
	#----------------------------------------------------------------------
	def firstFrame(self):
		"""self.firstFrame() -> Integer. First frame. @return: Integer."""
		return self._nukeNode.firstFrame()
	#----------------------------------------------------------------------
	def layers(self):
		"""nuke.Root.layers() -> Layer list. Class method. @return: Layer list."""
		return self._nukeNode.layers()
	#----------------------------------------------------------------------
	def realFps(self):
		"""self.realFps() -> float The global frames per second setting."""
		return self._nukeNode.realFps()
	#----------------------------------------------------------------------
	def connectInput(self):
		""""""
		return self._nukeNode.connectInput()
	#----------------------------------------------------------------------
	def fps(self):
		"""self.fps() -> integer Return the FPS rounded to an int. This is deprecated. Please use real_fps()."""
		return self._nukeNode.fps()
	#----------------------------------------------------------------------
	def setProxy(self,b):
		"""self.setProxy(b) -> None. Set proxy. @param b: Boolean convertible object. @return: None."""
		return self._nukeNode.setProxy(b)
	#----------------------------------------------------------------------
	def input(self):
		""""""
		return self._nukeNode.input()
	#----------------------------------------------------------------------
	def __len__(self):
		"""x.__len__() <==> len(x)"""
		return self._nukeNode.__len__()
	#----------------------------------------------------------------------
	def addView(self,s):
		"""self.addView(s) -> None. Add view. @param s: Name of view. @return: None."""
		return self._nukeNode.addView(s)
	#----------------------------------------------------------------------
	def deleteView(self,s):
		"""self.deleteView(s) -> None. Delete view. @param s: Name of view. @return: None."""
		return self._nukeNode.deleteView(s)
	#----------------------------------------------------------------------
	def inputs(self):
		""""""
		return self._nukeNode.inputs()
	#----------------------------------------------------------------------
	def __getitem__(self,y):
		"""x.__getitem__(y) <==> x[y]"""
		return self._nukeNode.__getitem__(y)
	#----------------------------------------------------------------------
	def mergeFrameRange(self):
		"""self.mergeFrameRange(a, b) -> None. Merge frame range. @param a: Low-end of interval range. @param b: High-end of interval range. @return: None."""
		return self._nukeNode.mergeFrameRange()
	#----------------------------------------------------------------------
	def setModified(self,b):
		"""self.setModified(b) -> None. Set the 'modified' flag in a script. Setting the value will turn the indicator in the title bar on/off and will start or stop the autosave timeout. @param b: Boolean convertible object. @return: None."""
		return self._nukeNode.setModified(b)
	#----------------------------------------------------------------------
	def proxy(self):
		"""self.proxy() -> True if proxy is set, False otherwise. @return: True if proxy is set, False otherwise."""
		return self._nukeNode.proxy()
	#----------------------------------------------------------------------
	def clones(self):
		""""""
		return self._nukeNode.clones()
	#----------------------------------------------------------------------
	def setView(self,s):
		"""self.setView(s) -> None. Set view. @param s: Name of view. @return: None."""
		return self._nukeNode.setView(s)
	#----------------------------------------------------------------------
	def setFrame(self,n):
		"""self.setFrame(n) -> None. Set frame. @param n: Frame number. @return: None."""
		return self._nukeNode.setFrame(n)
	#----------------------------------------------------------------------
	def optionalInput(self):
		""""""
		return self._nukeNode.optionalInput()
	#----------------------------------------------------------------------
	def __repr__(self):
		"""x.__repr__() <==> repr(x)"""
		return self._nukeNode.__repr__()

################################################################################
class Viewer(Node):
	#----------------------------------------------------------------------
	def roi(self):
		"""self.roi() -> dict Region of interest set in the viewer in pixel space coordinates. Returns None if the Viewer has no window yet. @return: Dict with keys x, y, r and t or None."""
		return self._nukeNode.roi()
	#----------------------------------------------------------------------
	def frameCached(self,f):
		"""frameCached(f) -> Bool  Determine whether frame /f/ is known to be in the memory cache."""
		return self._nukeNode.frameCached(f)
	#----------------------------------------------------------------------
	def sendMouseEvent(self,f):
		"""frameCached(f) -> Bool  Determine whether frame /f/ is known to be in the memory cache."""
		return self._nukeNode.sendMouseEvent(f)
	#----------------------------------------------------------------------
	def setRoi(self,box):
		"""self.setRoi(box) -> None. Set the region of interest in pixel space. @param box: A dictionary with the x, y, r and t keys.@return: None."""
		return self._nukeNode.setRoi(box)
	#----------------------------------------------------------------------
	def __getitem__(self,y):
		"""x.__getitem__(y) <==> x[y]"""
		return self._nukeNode.__getitem__(y)
	#----------------------------------------------------------------------
	def playbackRange(self):
		"""self.playbackRange() -> FrameRange. Return the frame range that's currently set to be played back in the viewer.@return: FrameRange."""
		return self._nukeNode.playbackRange()
	#----------------------------------------------------------------------
	def __str__(self):
		"""x.__str__() <==> str(x)"""
		return self._nukeNode.__str__()
	#----------------------------------------------------------------------
	def recordMouse(self,f):
		"""frameCached(f) -> Bool  Determine whether frame /f/ is known to be in the memory cache."""
		return self._nukeNode.recordMouse(f)
	#----------------------------------------------------------------------
	def recordMouseStop(self,f):
		"""recordMouseStop(f)  Stops mouse recording."""
		return self._nukeNode.recordMouseStop(f)
	#----------------------------------------------------------------------
	def toggleMouseTrails(self,f):
		"""frameCached(f) -> Bool  Determine whether frame /f/ is known to be in the memory cache."""
		return self._nukeNode.toggleMouseTrails(f)
	#----------------------------------------------------------------------
	def __repr__(self):
		"""x.__repr__() <==> repr(x)"""
		return self._nukeNode.__repr__()
	#----------------------------------------------------------------------
	def roiEnabled(self):
		"""self.roiEnabled() -> bool Whether the viewing of just a region of interest is enabled. Returns None if the Viewer has no window yet. @return: Boolean or None."""
		return self._nukeNode.roiEnabled()
	#----------------------------------------------------------------------
	def __len__(self):
		"""x.__len__() <==> len(x)"""
		return self._nukeNode.__len__()
	#----------------------------------------------------------------------
	def replayMouse(self,f):
		"""replayMouse(f) -> Bool  Determine whether frame /f/ is known to be in the memory cache."""
		return self._nukeNode.replayMouse(f)



################################################################################
class Assert(Node):
	pass

################################################################################
class DiskCache(Node):
	pass

################################################################################
class Dot(Node):
	pass
################################################################################
class Input(Node):
	pass
################################################################################
class Output(Node):
	pass

################################################################################
class NoOp(Node):
	pass

################################################################################
class PostageStamp(Node):
	pass

################################################################################
class StickyNote(Node):
	pass

################################################################################
class ViewMetaData(Node):
	pass

################################################################################
class CompareMetaData(Node):
	pass

################################################################################
class ModifyMetaData(Node):
	pass

################################################################################
class CopyMetaData(Node):
	pass

################################################################################
class AddTimeCode(Node):
	pass

################################################################################
class Anaglyph(Node):
	pass

################################################################################
class MixViews(Node):
	pass

################################################################################
class SideBySide(Node):
	pass

################################################################################
class ReConverge(Node):
	pass

################################################################################
class JoinViews(Node):
	pass

################################################################################
class OneView(Node):
	pass
#Image
################################################################################
class Read(Node):
	pass
################################################################################
class Write(Node):
	pass
################################################################################
class Constant(Node):
	pass
################################################################################
class CheckerBoard(Node):
	pass
################################################################################
class ColorBars(Node):
	pass
################################################################################
class ColorWheel(Node):
	pass
################################################################################
class CurveTool(Node):
	pass
#Merge
################################################################################
class CopyBBox(Node):
	pass
################################################################################
class CopyRectangle(Node):
	pass
################################################################################
class Merge2(Node):
	pass
################################################################################
class ShuffleViews(Node):
	pass

################################################################################
class Shuffle(Node):
	pass
################################################################################
class Copy(Node):
	pass
################################################################################
class AddChannels(Node):
	pass


################################################################################
class AnimationCurve(object):
	#----------------------------------------------------------------------
	def fixSlopes(self):
		"""self.fixSlopes() -> None. @return: None."""
		return self._nukeNode.fixSlopes()
	#----------------------------------------------------------------------
	def constant(self):
		"""self.constant() -> bool @return: True if the animation appears to be a horizontal line, is a simple number, or it is the default and all the points are at the same y value and have 0 slopes. False otherwise."""
		return self._nukeNode.constant()
	#----------------------------------------------------------------------
	def removeKey(self,keys):
		"""self.removeKey(keys) -> None. Remove some keys from the curve. @param keys: The sequence of keys to be removed. @return: None."""
		return self._nukeNode.removeKey(keys)
	#----------------------------------------------------------------------
	def size(self):
		"""self.size() -> Number of keys. @return: Number of keys."""
		return self._nukeNode.size()
	#----------------------------------------------------------------------
	def knobIndex(self):
		"""self.knobIndex() -> Int. Return the knob index this animation belongs to.@return: Int."""
		return self._nukeNode.knobIndex()
	#----------------------------------------------------------------------
	def inverse(self,y):
		"""self.inverse(y) -> Float. The inverse function at value y. This is the value of x such that evaluate(x) returns y. This is designed to invert color lookup tables. It only works if the derivative is zero or positive everywhere. @param y: The value of the function to get the inverse for. @return: Float."""
		return self._nukeNode.inverse(y)
	#----------------------------------------------------------------------
	def selected(self):
		"""self.selected() -> bool @return: True if selected, False otherwise."""
		return self._nukeNode.selected()
	#----------------------------------------------------------------------
	def setKey(self):
		"""self.setKey(t, y) -> Key. Set a key at time t and value y. If there is no key there one is created. If there is a key there it is moved vertically to be at y.  If a new key is inserted the interpolation and extrapolation are copied from a neighboring key, if there were no keys then it is set to nuke.SMOOTH interpolation and nuke.CONSTANT extrapolation. @param t: The time to set the key at. @param y: The value for the key. @return: The new key."""
		return self._nukeNode.setKey()
	#----------------------------------------------------------------------
	def addKey(self,keys):
		"""self.addKey(keys) -> None. Insert a sequence of keys. @param keys: Sequence of AnimationKey. @return: None."""
		return self._nukeNode.addKey(keys)
	#----------------------------------------------------------------------
	def changeInterpolation(self):
		"""self.changeInterpolation(keys, type) -> None. Change interpolation (and extrapolation) type for the keys. @param keys: Sequence of keys. @param type: Interpolation type. One of nuke.HORIZONTAL, nuke.BREAK, nuke.BEFORE_CONST, nuke.BEFORE_LINEAR, nuke.AFTER_CONST or nuke.AFTER_LINEAR. @return: None."""
		return self._nukeNode.changeInterpolation()
	#----------------------------------------------------------------------
	def toScript(self,selected):
		"""self.toScript(selected) -> str @param selected: Optional parameter. If this is given and is True, then only process the selected curves; otherwise convert all. @return: A string containing the curves."""
		return self._nukeNode.toScript(selected)
	#----------------------------------------------------------------------
	def knob(self):
		"""self.knob() -> Knob. Return knob this animation belongs to.@return: Knob."""
		return self._nukeNode.knob()
	#----------------------------------------------------------------------
	def keys(self):
		"""self.keys() -> List of keys. @return: List of keys."""
		return list(self._nukeNode.keys())
	#----------------------------------------------------------------------
	def evaluate(self,t):
		"""self.evaluate(t) -> float Value at time 't'. @param t: Time. @return: The value of the animation at time 't'."""
		return self._nukeNode.evaluate(t)
	#----------------------------------------------------------------------
	def integrate(self):
		"""self.integrate(t1, t2) -> Float. Calculate the area underneath the curve from t1 to t2. @param t1 The start of the integration range. @param t2 The end of the integration range. @return: The result of the integration."""
		return self._nukeNode.integrate()
	#----------------------------------------------------------------------
	def derivative(self):
		"""self.derivative(t, n) -> Float. The n'th derivative at time 't'. If n is less than 1 it returns evaluate(t). @param t: Time. @param n: Optional. Default is 1. @return: The value of the derivative."""
		return self._nukeNode.derivative()
	#----------------------------------------------------------------------
	def setExpression(self,s):
		"""self.setExpression(s) -> None. Set expression. @param s: A string containing the expression. @return: None."""
		return self._nukeNode.setExpression(s)
	#----------------------------------------------------------------------
	def identity(self):
		"""self.identity() -> bool @return: True if the animation appears to be such that y == x everywhere. This is True only for an expression of 'x' or the default expression and all points having y == x and slope == 1. Extrapolation is ignored."""
		return self._nukeNode.identity()
	#----------------------------------------------------------------------
	def clear(self):
		"""self.clear() -> None. Delete all keys. @return: None."""
		return self._nukeNode.clear()
	#----------------------------------------------------------------------
	def fromScript(self,s):
		"""self.fromScript(s) -> None. @param s: String. @return: None."""
		return self._nukeNode.fromScript(s)
	#----------------------------------------------------------------------
	def knobAndFieldName(self):
		"""self.knobAndFieldName() -> string. Knob and field name combined (e.g. 'translate.x'). @return: string."""
		return self._nukeNode.knobAndFieldName()
	#----------------------------------------------------------------------
	def noExpression(self):
		"""self.noExpression() -> bool @return: True if the expression is the default expression (i.e. the keys control the curve), False otherwise."""
		return self._nukeNode.noExpression()
	#----------------------------------------------------------------------
	def expression(self):
		"""self.expression() -> String. Get the expression.@return: String."""
		return self._nukeNode.expression()
	#----------------------------------------------------------------------
	def view(self):
		"""self.view() -> String. The view this AnimationCurve object is associated with. @return: String."""
		return self._nukeNode.view()
################################################################################
class AnimationKey(object):
	pass
################################################################################
class Box(object):

	def __init__(self,x=0,y=0,r=0,t=0):
		self._nuke_node = nuke.Box(int(x), int(y), int(r), int(t))

	def set(self, x, y, r, t):
		"""set all values at once."""
		self._nuke_node.set(x, y, r, t)

	def move(self, dx, dy):
		"""Move all the sides and thus the entire box by the given deltas."""
		self._nuke_node.move(dx, dy)

	@property
	def isConstant(self):
		"""if box is 1x1 in both directions, False otherwise."""
		return self._nuke_node.isConstant()

	def clampY(self,y):
		"""Return y restricted to pointing at a pixel in the box."""
		return self._nuke_node.clampY(y)

	def clampX(self,x):
		"""Return x restricted to pointing at a pixel in the box."""
		return self._nuke_node.clampX(x)

	def pad(self, dx, dy, dr, dt):
		"""pad(dx, dy, dr, dt) -> None. Move all the sides and thus the entire box by the given deltas."""
		self._nuke_node.pad(dx, dy, dr, dt)

	def intersect(self, x, y, r, t):
		"""Intersect with the given edges."""
		set_check=False

		if len(*args)==4:
			x,y,r,t = args[0], args[1], args[2], args[3]
			set_check=True

		elif len(*args)==1 and isinstance(args[0], Box):
			x,y,r,t = args[0].x, args[0].y, args[0].r, args[0].t
			set_check=True

		elif len(*args)==1 and isinstance(args[0], BackdropNode):
			x,y,r,t = args[0]._box.x, args[0]._box.y, args[0]._box.r, args[0]._box.t
			set_check=True

		elif len(*args)==1 and isinstance(args[0], nuke.Box):
			x,y,r,t = args[0].x(), args[0].y(), args[0].r(), args[0].t()
			set_check=True

		if set_check:
			self._nuke_node.intersect(x, y, r, t)

	def clear(self):
		"""clear() -> None.Set to is_constant()."""
		self._nuke_node.clear()

	def merge(self,*args):
		"""merge(x, y, r, t) -> None.Merge with the given edges."""
		set_check=False

		if len(*args)==4:
			x,y,r,t = args[0], args[1], args[2], args[3]
			set_check=True

		elif len(*args)==1 and isinstance(args[0], Box):
			x,y,r,t = args[0].x, args[0].y, args[0].r, args[0].t
			set_check=True

		elif len(*args)==1 and isinstance(args[0], BackdropNode):
			x,y,r,t = args[0]._box.x, args[0]._box.y, args[0]._box.r, args[0]._box.t
			set_check=True

		elif len(*args)==1 and isinstance(args[0], nuke.Box):
			x,y,r,t = args[0].x(), args[0].y(), args[0].r(), args[0].t()
			set_check=True

		if set_check:
			self._nuke_node.merge(x,y,r,t)

	def getR(self):
		"""r() -> intReturn right edge."""
		return self._nuke_node.r()

	def setR(self,value):
		return self._nuke_node.setR(value)
	r = property(getR,setR)

	def getT(self):
		"""t() -> intReturn top edge."""
		return self._nuke_node.t()

	def setT(self,value):
		return self._nuke_node.setT(value)
	t = property(getT,setT)

	def getW(self):
		"""w() -> intReturn width."""
		return self._nuke_node.w()

	def setW(self,value):
		return self._nuke_node.setW(value)
	w = property(getW,setW)

	def getY(self):
		"""y() -> intReturn bottom edge."""
		return self._nuke_node.y()

	def setY(self,value):
		return self._nuke_node.setY(value)
	y = property(getY,setY)

	def getX(self):
		"""x() -> intReturn left edge."""
		return self._nuke_node.x()

	def setX(self,value):
		return self._nuke_node.setX(value)
	x = property(getX,setX)

	def getH(self):
		"""h() -> intReturn height."""
		return self._nuke_node.h()

	def setH(self,value):
		return self._nuke_node.setH(value)
	h = property(getH,setH)

	@property
	def centerY(self):
		return self._nuke_node.centerY()
	@property
	def centerX(self):
		return self._nuke_node.centerX()

################################################################################
class Format(object):
	#----------------------------------------------------------------------
	def setPixelAspect(self,aspectRatio):
		"""self.setPixelAspect(aspectRatio) -> None  Set a new pixel aspect ratio for this format. The aspectRatio parameter is the new ratio, found by dividing the desired pixel width by the desired pixel height."""
		return self._nukeNode.setPixelAspect(aspectRatio)
	#----------------------------------------------------------------------
	def height(self):
		"""self.height() -> int  Return the height of image file in pixels."""
		return self._nukeNode.height()
	#----------------------------------------------------------------------
	def scaled(self):
		"""scaled(sx, sy, tx, ty) -> Format  Scale and translate this format by sx, sy, tx and ty.  @param sx: Scale factor in X.@param sy: Scale factor in Y.@param tx: Offset factor in X.@param ty: Offset factor in Y.@return: Format."""
		return self._nukeNode.scaled()
	#----------------------------------------------------------------------
	def setWidth(self,newWidth):
		"""self.setWidth(newWidth) -> None  Set the width of image file in pixels.newWidth is the new width for the image; it should be a positive integer."""
		return self._nukeNode.setWidth(newWidth)
	#----------------------------------------------------------------------
	def width(self):
		"""self.width() -> int  Return the width of image file in pixels."""
		return self._nukeNode.width()
	#----------------------------------------------------------------------
	def add(self,name):
		"""self.add(name) -> None  Add this instance to a list of "named" formats. The name parameter is the name of the list to add the format to."""
		return self._nukeNode.add(name)
	#----------------------------------------------------------------------
	def setName(self,name):
		"""self.setName(name) -> None  Set name of this format. The name parameter is the new name for the format."""
		return self._nukeNode.setName(name)
	#----------------------------------------------------------------------
	def setT(self,newT):
		"""self.setT(newT) -> None  Set the top edge of image file in pixels. newY is the new top edge for the image; it should be a positive integer."""
		return self._nukeNode.setT(newT)
	#----------------------------------------------------------------------
	def setR(self,newR):
		"""self.setR(newR) -> None  Set the right edge of image file in pixels. newR is the new right edge for the image; it should be a positive integer."""
		return self._nukeNode.setR(newR)
	#----------------------------------------------------------------------
	def fromUV(self):
		"""self.fromUV(u, v) -> [x, y]  Transform a UV coordinate in the range 0-1 into the format's XY range. Returns a list containing the x and y coordinates.  @param u: The U coordinate. @param v: The V coordinate. @return: [x, y]"""
		return self._nukeNode.fromUV()
	#----------------------------------------------------------------------
	def setX(self,newX):
		"""self.setX(newX) -> None  Set the left edge of image file in pixels. newX is the new left edge for the  image; it should be a positive integer."""
		return self._nukeNode.setX(newX)
	#----------------------------------------------------------------------
	def setY(self,newY):
		"""self.setY(newY) -> None  Set the bottom edge of image file in pixels. newY is the new bottom edge for the image; it should be a positive integer."""
		return self._nukeNode.setY(newY)
	#----------------------------------------------------------------------
	def setHeight(self,newHeight):
		"""self.setHeight(newHeight) -> None  Set the height of image file in pixels. newHeight is the new height for the image; it should be a positive integer."""
		return self._nukeNode.setHeight(newHeight)
	#----------------------------------------------------------------------
	def pixelAspect(self):
		"""self.pixelAspect() -> float  Returns the pixel aspect ratio (pixel width divided by pixel height) for this format."""
		return self._nukeNode.pixelAspect()
	#----------------------------------------------------------------------
	def name(self):
		"""self.name() -> string  Returns the user-visible name of the format."""
		return self._nukeNode.name()
	#----------------------------------------------------------------------
	def r(self):
		"""self.r() -> int  Return the right edge of image file in pixels."""
		return self._nukeNode.r()
	#----------------------------------------------------------------------
	def t(self):
		"""self.t() -> int  Return the top edge of image file in pixels."""
		return self._nukeNode.t()
	#----------------------------------------------------------------------
	def toUV(self):
		"""self.toUV(x, y) -> (u, v)  Back-transform an XY coordinate in the format's space into UV space.  @param x: The X coordinate. @param y: The Y coordinate. @return: [u, v]."""
		return self._nukeNode.toUV()
	#----------------------------------------------------------------------
	def y(self):
		"""self.y() -> int  Return the bottom edge of image file in pixels."""
		return self._nukeNode.y()
	#----------------------------------------------------------------------
	def x(self):
		"""self.x() -> int  Return the left edge of image file in pixels."""
		return self._nukeNode.x()
################################################################################
class FrameRange(object):
	#----------------------------------------------------------------------
	def minFrame(self):
		"""self.minFrame() -> int   return the minimun frame define in the range."""
		return self._nukeNode.minFrame()
	#----------------------------------------------------------------------
	def last(self):
		"""self.last() -> int   return the last frame of the range."""
		return self._nukeNode.last()
	#----------------------------------------------------------------------
	def setLast(self,n):
		"""self.setLast(n) -> None   set the last frame of the range."""
		return self._nukeNode.setLast(n)
	#----------------------------------------------------------------------
	def __str__(self):
		"""x.__str__() <==> str(x)"""
		return self._nukeNode.__str__()
	#----------------------------------------------------------------------
	def getFrame(self,n):
		"""self.getFrame(n) -> int   return the frame according to the index, parameter n must be between 0 and frames()."""
		return self._nukeNode.getFrame(n)
	#----------------------------------------------------------------------
	def stepFrame(self):
		"""self.stepFrame() -> int   return the absolute increment between two frames."""
		return self._nukeNode.stepFrame()
	#----------------------------------------------------------------------
	def setFirst(self,n):
		"""self.setFirst(n) -> None   set the first frame of the range."""
		return self._nukeNode.setFirst(n)
	#----------------------------------------------------------------------
	def __next__(self):
		"""x.next() -> the next value, or raise StopIteration"""
		return next(self._nukeNode)
	#----------------------------------------------------------------------
	def isInRange(self,n):
		"""self.isInRange(n) -> int   return if the frame is inside the range."""
		return self._nukeNode.isInRange(n)
	#----------------------------------------------------------------------
	def maxFrame(self):
		"""self.maxFrame() -> int   return the maximun frame define in the range."""
		return self._nukeNode.maxFrame()
	#----------------------------------------------------------------------
	def __iter__(self):
		"""x.__iter__() <==> iter(x)"""
		return self._nukeNode.__iter__()
	#----------------------------------------------------------------------
	def setIncrement(self,n):
		"""self.setIncrement(n) -> None   set the increment between two frames."""
		return self._nukeNode.setIncrement(n)
	#----------------------------------------------------------------------
	def increment(self):
		"""self.increment() -> int   return the increment between two frames."""
		return self._nukeNode.increment()
	#----------------------------------------------------------------------
	def frames(self):
		"""self.frames() -> int   return the numbers of frames defined in the range."""
		return self._nukeNode.frames()
	#----------------------------------------------------------------------
	def first(self):
		"""self.first() -> int   return the first frame of the range."""
		return self._nukeNode.first()
################################################################################
class FrameRanges(object):
	#----------------------------------------------------------------------
	def compact(self):
		"""compact() -> None   compact all the frame ranges."""
		return self._nukeNode.compact()
	#----------------------------------------------------------------------
	def getRange(self):
		"""getRange()-> FrameRange   return a range from the list"""
		return self._nukeNode.getRange()
	#----------------------------------------------------------------------
	def toFrameList(self):
		"""toFrameList() -> [int]   return a list of frames in a vector"""
		return self._nukeNode.toFrameList()
	#----------------------------------------------------------------------
	def __str__(self):
		"""x.__str__() <==> str(x)"""
		return self._nukeNode.__str__()
	#----------------------------------------------------------------------
	def minFrame(self):
		"""minFrame() -> int   get minimun frame of all ranges."""
		return self._nukeNode.minFrame()
	#----------------------------------------------------------------------
	def add(self,r):
		"""add(r) -> None   add a new frame range."""
		return self._nukeNode.add(r)
	#----------------------------------------------------------------------
	def __next__(self):
		"""x.next() -> the next value, or raise StopIteration"""
		return next(self._nukeNode)
	#----------------------------------------------------------------------
	def maxFrame(self):
		"""maxFrame() -> int   get maximun frame of all ranges."""
		return self._nukeNode.maxFrame()
	#----------------------------------------------------------------------
	def __iter__(self):
		"""x.__iter__() <==> iter(x)"""
		return self._nukeNode.__iter__()
	#----------------------------------------------------------------------
	def clear(self):
		"""clear() -> None   reset all store frame ranges."""
		return self._nukeNode.clear()
	#----------------------------------------------------------------------
	def size(self):
		"""size() -> int   return the ranges number."""
		return self._nukeNode.size()
################################################################################
class GlobalsEnvironment(object):
	#----------------------------------------------------------------------
	def __delitem__(self,y):
		"""x.__delitem__(y) <==> del x[y]"""
		return self._nukeNode.__delitem__(y)
	#----------------------------------------------------------------------
	def __getitem__(self,y):
		"""x.__getitem__(y) <==> x[y]"""
		return self._nukeNode.__getitem__(y)
	#----------------------------------------------------------------------
	def __contains__(self):
		""""""
		return self._nukeNode.__contains__()
	#----------------------------------------------------------------------
	def keys(self):
		""""""
		return list(self._nukeNode.keys())
	#----------------------------------------------------------------------
	def items(self):
		""""""
		return list(self._nukeNode.items())
	#----------------------------------------------------------------------
	def get(self):
		""""""
		return self._nukeNode.get()
	#----------------------------------------------------------------------
	def __setitem__(self):
		"""x.__setitem__(i, y) <==> x[i]=y"""
		return self._nukeNode.__setitem__()
	#----------------------------------------------------------------------
	def has_key(self):
		""""""
		return self._nukeNode.has_key()
	#----------------------------------------------------------------------
	def values(self):
		""""""
		return list(self._nukeNode.values())
	#----------------------------------------------------------------------
	def __repr__(self):
		"""x.__repr__() <==> repr(x)"""
		return self._nukeNode.__repr__()
	#----------------------------------------------------------------------
	def __len__(self):
		"""x.__len__() <==> len(x)"""
		return self._nukeNode.__len__()
################################################################################
class Hash(object):
	#----------------------------------------------------------------------
	def reset(self):
		"""Reset the hash."""
		return self._nukeNode.reset()
	#----------------------------------------------------------------------
	def __ne__(self,y):
		"""x.__ne__(y) <==> x!=y"""
		return self._nukeNode.__ne__(y)
	#----------------------------------------------------------------------
	def setHash(self):
		"""Set the current value of the hash."""
		return self._nukeNode.setHash()
	#----------------------------------------------------------------------
	def append(self):
		"""Add another value to the hash."""
		return self._nukeNode.append()
	#----------------------------------------------------------------------
	def __hash__(self):
		"""x.__hash__() <==> hash(x)"""
		return self._nukeNode.__hash__()
	#----------------------------------------------------------------------
	def getHash(self):
		"""Get the current value of the hash."""
		return self._nukeNode.getHash()
	#----------------------------------------------------------------------
	def __lt__(self,y):
		"""x.__lt__(y) <==> x<y"""
		return self._nukeNode.__lt__(y)
	#----------------------------------------------------------------------
	def __eq__(self,y):
		"""x.__eq__(y) <==> x==y"""
		return self._nukeNode.__eq__(y)
	#----------------------------------------------------------------------
	def __ge__(self,y):
		"""x.__ge__(y) <==> x>=y"""
		return self._nukeNode.__ge__(y)
################################################################################
class Info(object):
	#----------------------------------------------------------------------
	def h(self):
		"""self.h() -> float  Return height."""
		return self._nukeNode.h()
	#----------------------------------------------------------------------
	def w(self):
		"""self.w() -> float  Return width."""
		return self._nukeNode.w()
	#----------------------------------------------------------------------
	def y(self):
		"""self.y() -> float  Return the bottom edge."""
		return self._nukeNode.y()
	#----------------------------------------------------------------------
	def x(self):
		"""x() -> float  Return left edge."""
		return self._nukeNode.x()
################################################################################
class Layer(object):
	#----------------------------------------------------------------------
	def setName(self,newName):
		"""self.setName(newName) -> None Set the name of this layer.  @param newName: The new name for this layer."""
		return self._nukeNode.setName(newName)
	#----------------------------------------------------------------------
	def channels(self):
		"""self.channels() -> [string, ...] Get a list of the channels in this layer.  @return: A list of strings, where each string is the name of a channel in this layer."""
		return self._nukeNode.channels()
	#----------------------------------------------------------------------
	def visible(self):
		"""self.visible() -> bool Check whether the layer is visible.  @return: True if visible, False if not."""
		return self._nukeNode.visible()
	#----------------------------------------------------------------------
	def name(self):
		"""self.name() -> str Get the layer name.  @return: The layer name, as a string."""
		return self._nukeNode.name()
################################################################################
class LinkableKnobInfo(object):
	#----------------------------------------------------------------------
	def knob(self):
		"""self.knob() -> Knob Returns the knob that may be linked to."""
		return self._nukeNode.knob()
	#----------------------------------------------------------------------
	def displayName(self):
		"""self.displayName() -> String Returns the custom display name that will appear in Link-to menus."""
		return self._nukeNode.displayName()
	#----------------------------------------------------------------------
	def enabled(self):
		"""self.enabled() -> Boolean Returns whether the knob is currently enabled or not."""
		return self._nukeNode.enabled()
	#----------------------------------------------------------------------
	def indices(self):
		"""self.indices() -> List Returns a list of the knob channels that should be used with this linkable knob."""
		return self._nukeNode.indices()
	#----------------------------------------------------------------------
	def absolute(self):
		"""self.absolute() -> Boolean Returns whether the values of this knob should be treated as absolute or relative. This may be useful for positions."""
		return self._nukeNode.absolute()
################################################################################
class Lut(object):
	#----------------------------------------------------------------------
	def toByte(self,float):
		"""self.toByte(float) -> float.  Converts floating point values to byte values in the range 0-255."""
		return self._nukeNode.toByte(float)
	#----------------------------------------------------------------------
	def fromByteSingle(self,float):
		"""self.fromByte(float) -> float.  Converts byte values in the range 0-255 to floating point."""
		return self._nukeNode.fromByteSingle(float)
	#----------------------------------------------------------------------
	def fromFloat(self):
		"""fromFloat(src, alpha) -> float list.  Convert a sequence of floating-point values to from_byte(x*255). Alpha is an optional argument and if present unpremultiply by alpha, convert, and then multiply back."""
		return self._nukeNode.fromFloat()
	#----------------------------------------------------------------------
	def toFloat(self):
		"""toFloat(src, alpha) -> float list.  Convert a sequence of floating-point values to to_byte(x)/255. Alpha is an optional argument and if present unpremultiply by alpha, convert, and then multiply back."""
		return self._nukeNode.toFloat()
	#----------------------------------------------------------------------
	def isLinear(self):
		"""self.isLinear() -> True if toByte(x) appears to return x*255, False otherwise."""
		return self._nukeNode.isLinear()
	#----------------------------------------------------------------------
	def toByteSingle(self,float):
		"""self.toByte(float) -> float.  Converts floating point values to byte values in the range 0-255."""
		return self._nukeNode.toByteSingle(float)
	#----------------------------------------------------------------------
	def fromByte(self,float):
		"""self.fromByte(float) -> float.  Converts byte values in the range 0-255 to floating point."""
		return self._nukeNode.fromByte(float)
	#----------------------------------------------------------------------
	def isZero(self):
		"""self.isZero() -> True if toByte(0) returns a value <= 0, False otherwise."""
		return self._nukeNode.isZero()
################################################################################
class MenuItem(object):
	#----------------------------------------------------------------------
	def setEnabled(self,enabled):
		"""self.setEnabled(enabled) -> None Enable or disable the item. @param enabled: True to enable the object; False to disable it."""
		return self._nukeNode.setEnabled(enabled)
	#----------------------------------------------------------------------
	def name(self):
		"""self.name() -> String Returns the name of the menu item."""
		return self._nukeNode.name()
	#----------------------------------------------------------------------
	def invoke(self):
		"""self.invoke() -> None Perform the action associated with this menu item."""
		return self._nukeNode.invoke()
	#----------------------------------------------------------------------
	def script(self):
		"""self.script() -> String Returns the script that gets executed for this menu item."""
		return self._nukeNode.script()
	#----------------------------------------------------------------------
	def setScript(self,script):
		"""self.setScript(script) -> None Set the script to be executed for this menu item. Note: To call a python script file, you can use the execfile() function. i.e: menu.setScript("execfile('script.py')")"""
		return self._nukeNode.setScript(script)
	#----------------------------------------------------------------------
	def setShortcut(self,keySequence):
		"""self.setShortcut(keySequence) -> None Set the keyboard shortcut on this menu item. @param keySequence: the new shortcut in PortableText format, e.g. "Ctrl+Shift+P"""
		return self._nukeNode.setShortcut(keySequence)
	#----------------------------------------------------------------------
	def shortcut(self):
		"""self.shortcut() -> String Returns the keyboard shortcut on this menu item. The format of this is the PortableText format. It will return a string such as "Ctrl+Shift+P". Note that on Mac OS X the Command key is equivalent to Ctrl."""
		return self._nukeNode.shortcut()
	#----------------------------------------------------------------------
	def setIcon(self,icon):
		"""self.setIcon(icon) -> None Set the icon on this menu item. @param icon: the new icon as a path"""
		return self._nukeNode.setIcon(icon)
	#----------------------------------------------------------------------
	def icon(self):
		"""self.icon() -> String Returns the name of the icon on this menu item as path of the icon."""
		return self._nukeNode.icon()
################################################################################
class Menu(MenuItem):
	#----------------------------------------------------------------------
	def name(self):
		"""self.name() -> String Returns the name of the menu item."""
		return self._nukeNode.name()
	#----------------------------------------------------------------------
	def addSeparator(self,**kwargs):
		"""self.addSeparator(**kwargs) -> The separator that was created. Add a separator to this menu/toolbar. @param **kwargs The following keyword arguments are accepted: index     The position to insert the new separator in, in the menu/toolbar. @return: The separator that was created."""
		return self._nukeNode.addSeparator(**kwargs)
	#----------------------------------------------------------------------
	def menu(self,name):
		"""self.menu(name) -> Menu or None Finds a submenu or command with a particular name. @param name: The name to search for. @return: The submenu or command we found, or None if we could not find anything."""
		return self._nukeNode.menu(name)
	#----------------------------------------------------------------------
	def addCommand(self):
		"""self.addCommand(name, command, shortcut, icon, tooltip, index, readonly) -> The menu/toolbar item that was added to hold the command. Add a new command to this menu/toolbar. Note that when invoked, the command is automatically enclosed in an undo group, so that undo/redo functionality works. Optional arguments can be specified by name. Note that if the command argument is not specified, then the command will be auto-created as a "nuke.createNode()" using the name argument as the node to create.  Example: menubar = nuke.menu('Nuke') fileMenu = menubar.findItem('File') fileMenu.addCommand('NewCommand', 'print 10', shortcut='t')  @param name: The name for the menu/toolbar item. The name may contain submenu names delimited by '/' or '', and submenus are created as needed. @param command: Optional. The command to add to the menu/toolbar. This can be a string to evaluate or a Python Callable (function, method, etc) to run. @param shortcut: Optional. The keyboard shortcut for the command, such as 'R', 'F5' or 'Ctrl-H'. Note that this overrides pre-existing other uses for the shortcut. @param icon: Optional. An icon for the command. This should be a path to an icon in the nuke.pluginPath() directory. If the icon is not specified, Nuke will automatically try to find an icon with the name argument and .png appended to it. @param tooltip: Optional. The tooltip text, displayed on mouseover for toolbar buttons. @param index: Optional. The position to insert the new item in, in the menu/toolbar. This defaults to last in the menu/toolbar. @param readonly: Optional. True/False for whether the item should be available when the menu is invoked in a read-only context. @return: The menu/toolbar item that was added to hold the command."""
		return self._nukeNode.addCommand()
	#----------------------------------------------------------------------
	def addMenu(self,**kwargs):
		"""self.addMenu(**kwargs) -> The submenu that was added. Add a new submenu. @param **kwargs The following keyword arguments are accepted:                 name      The name for the menu/toolbar item                 icon      An icon for the menu. Loaded from the nuke search path.                 tooltip   The tooltip text.                 index     The position to insert the menu in. Use -1 to add to the end of the menu. @return: The submenu that was added."""
		return self._nukeNode.addMenu(**kwargs)
	#----------------------------------------------------------------------
	def removeItem(self,name):
		"""self.removeItem(name) -> None Removes a submenu or command with a particular name. If the containing menu becomes empty, it will be removed too. @param name: The name to remove for. @return: true if removed, false if menu not found """
		return self._nukeNode.removeItem(name)
	#----------------------------------------------------------------------
	def items(self):
		"""self.items() -> None Returns a list of sub menu items."""
		return list(self._nukeNode.items())
	#----------------------------------------------------------------------
	def findItem(self,name):
		"""self.findItem(name) -> Menu or None Finds a submenu or command with a particular name. @param name: The name to search for. @return: The submenu or command we found, or None if we could not find anything."""
		return self._nukeNode.findItem(name)
	#----------------------------------------------------------------------
	def clearMenu(self):
		"""self.clearMenu()  Clears a menu. @param **kwargs The following keyword arguments are accepted:                 name      The name for the menu/toolbar item @return: true if cleared, false if menu not found """
		return self._nukeNode.clearMenu()
################################################################################
class MenuBar(object):
	#----------------------------------------------------------------------
	def name(self):
		"""self.name() -> String Returns the name of the menu item."""
		return self._nukeNode.name()
	#----------------------------------------------------------------------
	def addSeparator(self,**kwargs):
		"""self.addSeparator(**kwargs) -> The separator that was created. Add a separator to this menu/toolbar. @param **kwargs The following keyword arguments are accepted: index     The position to insert the new separator in, in the menu/toolbar. @return: The separator that was created."""
		return self._nukeNode.addSeparator(**kwargs)
	#----------------------------------------------------------------------
	def menu(self,name):
		"""self.menu(name) -> Menu or None Finds a submenu or command with a particular name. @param name: The name to search for. @return: The submenu or command we found, or None if we could not find anything."""
		return self._nukeNode.menu(name)
	#----------------------------------------------------------------------
	def addCommand(self):
		"""self.addCommand(name, command, shortcut, icon, tooltip, index, readonly) -> The menu/toolbar item that was added to hold the command. Add a new command to this menu/toolbar. Note that when invoked, the command is automatically enclosed in an undo group, so that undo/redo functionality works. Optional arguments can be specified by name. Note that if the command argument is not specified, then the command will be auto-created as a "nuke.createNode()" using the name argument as the node to create.  Example: menubar = nuke.menu('Nuke') fileMenu = menubar.findItem('File') fileMenu.addCommand('NewCommand', 'print 10', shortcut='t')  @param name: The name for the menu/toolbar item. The name may contain submenu names delimited by '/' or '', and submenus are created as needed. @param command: Optional. The command to add to the menu/toolbar. This can be a string to evaluate or a Python Callable (function, method, etc) to run. @param shortcut: Optional. The keyboard shortcut for the command, such as 'R', 'F5' or 'Ctrl-H'. Note that this overrides pre-existing other uses for the shortcut. @param icon: Optional. An icon for the command. This should be a path to an icon in the nuke.pluginPath() directory. If the icon is not specified, Nuke will automatically try to find an icon with the name argument and .png appended to it. @param tooltip: Optional. The tooltip text, displayed on mouseover for toolbar buttons. @param index: Optional. The position to insert the new item in, in the menu/toolbar. This defaults to last in the menu/toolbar. @param readonly: Optional. True/False for whether the item should be available when the menu is invoked in a read-only context. @return: The menu/toolbar item that was added to hold the command."""
		return self._nukeNode.addCommand()
	#----------------------------------------------------------------------
	def addMenu(self,**kwargs):
		"""self.addMenu(**kwargs) -> The submenu that was added. Add a new submenu. @param **kwargs The following keyword arguments are accepted:                 name      The name for the menu/toolbar item                 icon      An icon for the menu. Loaded from the nuke search path.                 tooltip   The tooltip text.                 index     The position to insert the menu in. Use -1 to add to the end of the menu. @return: The submenu that was added."""
		return self._nukeNode.addMenu(**kwargs)
	#----------------------------------------------------------------------
	def removeItem(self,name):
		"""self.removeItem(name) -> None Removes a submenu or command with a particular name. If the containing menu becomes empty, it will be removed too. @param name: The name to remove for. @return: true if removed, false if menu not found """
		return self._nukeNode.removeItem(name)
	#----------------------------------------------------------------------
	def items(self):
		"""self.items() -> None Returns a list of sub menu items."""
		return list(self._nukeNode.items())
	#----------------------------------------------------------------------
	def findItem(self,name):
		"""self.findItem(name) -> Menu or None Finds a submenu or command with a particular name. @param name: The name to search for. @return: The submenu or command we found, or None if we could not find anything."""
		return self._nukeNode.findItem(name)
	#----------------------------------------------------------------------
	def clearMenu(self):
		"""self.clearMenu()  Clears a menu. @param **kwargs The following keyword arguments are accepted:                 name      The name for the menu/toolbar item @return: true if cleared, false if menu not found """
		return self._nukeNode.clearMenu()
################################################################################
class NodeConstructor(object):
	#----------------------------------------------------------------------
	def __call__(self):
		"""x.__call__(...) <==> x(...)"""
		return self._nukeNode.__call__()
################################################################################
class OutputContext(object):
	#----------------------------------------------------------------------
	def viewcount(self):
		"""viewcount() -> int  Return number of views."""
		return self._nukeNode.viewcount()
	#----------------------------------------------------------------------
	def viewname(self,n):
		"""viewname(n) -> string  Return name of the view. The n argument is an integer in the range of 0 to number of views."""
		return self._nukeNode.viewname(n)
	#----------------------------------------------------------------------
	def setFrame(self,f):
		"""setFrame(f) -> True  Set frame value. The f argument is a float."""
		return self._nukeNode.setFrame(f)
	#----------------------------------------------------------------------
	def frame(self):
		"""frame() -> float  Return frame value."""
		return self._nukeNode.frame()
	#----------------------------------------------------------------------
	def setView(self,n):
		"""setView(n) -> True  Set view number. The n argument is an integer in the range of 0 to number of views."""
		return self._nukeNode.setView(n)
	#----------------------------------------------------------------------
	def viewshort(self,n):
		"""viewshort(n) -> string  Return short name of the view. The n argument is an integer in the range of 0 to number of views."""
		return self._nukeNode.viewshort(n)
	#----------------------------------------------------------------------
	def view(self):
		"""view() -> int  Return view number."""
		return self._nukeNode.view()
################################################################################
class Panel(object):
	#----------------------------------------------------------------------
	def addEnumerationPulldown(self):
		"""self.addEnumerationPulldown(name, value) -> True if successful. Add a pulldown menu to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addEnumerationPulldown()
	#----------------------------------------------------------------------
	def show(self):
		"""self.show() -> An int value indicating how the dialog was closed (normally, or cancelled). Display the panel. @return: An int value indicating how the dialog was closed (normally, or cancelled)."""
		return self._nukeNode.show()
	#----------------------------------------------------------------------
	def setTitle(self,val):
		"""self.setTitle(val) -> True if successful. Set the current title for the panel. @param val: The title as a string. @return: True if successful."""
		return self._nukeNode.setTitle(val)
	#----------------------------------------------------------------------
	def addButton(self):
		"""self.addButton(name, value) -> True if successful. Add a button to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addButton()
	#----------------------------------------------------------------------
	def addPasswordInput(self):
		"""self.addPasswordInput(name, value) -> True if successful. Add a password input knob to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addPasswordInput()
	#----------------------------------------------------------------------
	def value(self,name):
		"""self.value(name) -> The value for the field if any, otherwise None. Get the value of a particular control in the panel. @param name: The name of the knob to get a value from. @return: The value for the field if any, otherwise None."""
		return self._nukeNode.value(name)
	#----------------------------------------------------------------------
	def setWidth(self,val):
		"""self.setWidth(val) -> True if successful. Set the width of the panel. @param val: The width as an int. @return: True if successful."""
		return self._nukeNode.setWidth(val)
	#----------------------------------------------------------------------
	def title(self):
		"""self.title() -> The title as a string. Get the current title for the panel. @return: The title as a string."""
		return self._nukeNode.title()
	#----------------------------------------------------------------------
	def addMultilineTextInput(self):
		"""self.addMultilineTextInput(name, value) -> True if successful. Add a multi-line text knob to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addMultilineTextInput()
	#----------------------------------------------------------------------
	def width(self):
		"""self.width() -> The width as an int. Get the width of the panel. @return: The width as an int."""
		return self._nukeNode.width()
	#----------------------------------------------------------------------
	def addRGBColorChip(self):
		"""self.addRGBColorChip(name, value) -> True if successful. Add a color chooser to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addRGBColorChip()
	#----------------------------------------------------------------------
	def addClipnameSearch(self):
		"""self.addClipnameSearch(name, value) -> True if successful. Add a clipname search knob to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addClipnameSearch()
	#----------------------------------------------------------------------
	def addNotepad(self):
		"""self.addNotepad(name, value) -> True if successful. Add a text edit widget to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addNotepad()
	#----------------------------------------------------------------------
	def addScriptCommand(self):
		"""self.addScriptCommand(name, value) -> True if successful. Add a script command evaluator to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addScriptCommand()
	#----------------------------------------------------------------------
	def addSingleLineInput(self):
		"""self.addSingleLineInput(name, value) -> True if successful. Add a single-line input knob to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addSingleLineInput()
	#----------------------------------------------------------------------
	def addTextFontPulldown(self):
		"""self.addTextFontPulldown(name, value) -> True if successful. Add a font chooser to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addTextFontPulldown()
	#----------------------------------------------------------------------
	def execute(self,name):
		"""self.execute(name) -> The result of the script as a string, or None if it fails. Execute the script command associated with a particular label and return the result as a string. @param name: The name of the script field to execute. @return: The result of the script as a string, or None if it fails."""
		return self._nukeNode.execute(name)
	#----------------------------------------------------------------------
	def clear(self):
		"""self.clear() -> None Clear all panel attributes."""
		return self._nukeNode.clear()
	#----------------------------------------------------------------------
	def addFilenameSearch(self):
		"""self.addFilenameSearch(name, value) -> True if successful. Add a filename search knob to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addFilenameSearch()
	#----------------------------------------------------------------------
	def addBooleanCheckBox(self):
		"""self.addBooleanCheckBox(name, value) -> True if successful. Add a boolean check box knob to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addBooleanCheckBox()
	#----------------------------------------------------------------------
	def addExpressionInput(self):
		"""self.addExpressionInput(name, value) -> True if successful. Add an expression evaluator to the panel. @param name: The name for the new knob. @param value: The initial value for the new knob. @return: True if successful."""
		return self._nukeNode.addExpressionInput()
################################################################################
class PanelNode(object):
	#----------------------------------------------------------------------
	def writeKnobs(self,i):
		"""self.writeKnobs(i) -> String in .nk form. Return a tcl list. If TO_SCRIPT | TO_VALUE is not on, this is a simple list of knob names. If it is on, it is an alternating list of knob names and the output of to_script().  Flags can be any of these or'd together: - nuke.TO_SCRIPT produces to_script(0) values - nuke.TO_VALUE produces to_script(context) values - nuke.WRITE_NON_DEFAULT_ONLY skips knobs with not_default() false - nuke.WRITE_USER_KNOB_DEFS writes addUserKnob commands for user knobs - nuke.WRITE_ALL writes normally invisible knobs like name, xpos, ypos  @param i: The set of flags or'd together. Default is TO_SCRIPT | TO_VALUE. @return: String in .nk form."""
		return self._nukeNode.writeKnobs(i)
	#----------------------------------------------------------------------
	def createWidget(self):
		"""Create the widget for the panel"""
		return self._nukeNode.createWidget()
	#----------------------------------------------------------------------
	def __str__(self):
		"""x.__str__() <==> str(x)"""
		return self._nukeNode.__str__()
	#----------------------------------------------------------------------
	def addKnob(self,k):
		"""self.addKnob(k) -> None. Add knob k to this node or panel. @param k: Knob. @return: None."""
		return self._nukeNode.addKnob(k)
	#----------------------------------------------------------------------
	def removeKnob(self,k):
		"""self.removeKnob(k) -> None. Remove knob k from this node or panel. Throws a ValueError exception if k is not found on the node. @param k: Knob. @return: None."""
		return self._nukeNode.removeKnob(k)
	#----------------------------------------------------------------------
	def knobs(self):
		"""self.knobs() -> dict  Get a dictionary of (name, knob) pairs for all knobs in this node.  For example:     >>> b = nuke.nodes.Blur()    >>> b.knobs()  @return: Dictionary of all knobs.  Note that this doesn't follow the links for Link_Knobs"""
		return self._nukeNode.knobs()
	#----------------------------------------------------------------------
	def readKnobs(self,s):
		"""self.readKnobs(s) -> None. Read the knobs from a string (TCL syntax). @param s: A string. @return: None."""
		return self._nukeNode.readKnobs(s)
################################################################################
class ProgressTask(object):
	#----------------------------------------------------------------------
	def setProgress(self,i):
		"""self.setProgress(i) -> None.  i is an integer representing the current progress"""
		return self._nukeNode.setProgress(i)
	#----------------------------------------------------------------------
	def isCancelled(self):
		"""self.isCancelled() -> True if the user has requested the task to be cancelled. """
		return self._nukeNode.isCancelled()
	#----------------------------------------------------------------------
	def setMessage(self,s):
		"""self.setMessage(s) -> None.  set the message for the progress task"""
		return self._nukeNode.setMessage(s)
################################################################################
class RunInMainThread(object):
	#----------------------------------------------------------------------
	def request(self):
		""""""
		return self._nukeNode.request()
	#----------------------------------------------------------------------
	def result(self):
		""""""
		return self._nukeNode.result()
################################################################################
class ToolBar(object):
	#----------------------------------------------------------------------
	def addSeparator(self,**kwargs):
		"""self.addSeparator(**kwargs) -> The separator that was created. Add a separator to this menu/toolbar. @param **kwargs The following keyword arguments are accepted: index     The position to insert the new separator in, in the menu/toolbar. @return: The separator that was created."""
		return self._nukeNode.addSeparator(**kwargs)
	#----------------------------------------------------------------------
	def menu(self,name):
		"""self.menu(name) -> Menu or None Finds a submenu or command with a particular name. @param name: The name to search for. @return: The submenu or command we found, or None if we could not find anything."""
		return self._nukeNode.menu(name)
	#----------------------------------------------------------------------
	def addCommand(self):
		"""self.addCommand(name, command, shortcut, icon, tooltip, index, readonly) -> The menu/toolbar item that was added to hold the command. Add a new command to this menu/toolbar. Note that when invoked, the command is automatically enclosed in an undo group, so that undo/redo functionality works. Optional arguments can be specified by name. Note that if the command argument is not specified, then the command will be auto-created as a "nuke.createNode()" using the name argument as the node to create.  Example: menubar = nuke.menu('Nuke') fileMenu = menubar.findItem('File') fileMenu.addCommand('NewCommand', 'print 10', shortcut='t')  @param name: The name for the menu/toolbar item. The name may contain submenu names delimited by '/' or '', and submenus are created as needed. @param command: Optional. The command to add to the menu/toolbar. This can be a string to evaluate or a Python Callable (function, method, etc) to run. @param shortcut: Optional. The keyboard shortcut for the command, such as 'R', 'F5' or 'Ctrl-H'. Note that this overrides pre-existing other uses for the shortcut. @param icon: Optional. An icon for the command. This should be a path to an icon in the nuke.pluginPath() directory. If the icon is not specified, Nuke will automatically try to find an icon with the name argument and .png appended to it. @param tooltip: Optional. The tooltip text, displayed on mouseover for toolbar buttons. @param index: Optional. The position to insert the new item in, in the menu/toolbar. This defaults to last in the menu/toolbar. @param readonly: Optional. True/False for whether the item should be available when the menu is invoked in a read-only context. @return: The menu/toolbar item that was added to hold the command."""
		return self._nukeNode.addCommand()
	#----------------------------------------------------------------------
	def addMenu(self,**kwargs):
		"""self.addMenu(**kwargs) -> The submenu that was added. Add a new submenu. @param **kwargs The following keyword arguments are accepted:                 name      The name for the menu/toolbar item                 icon      An icon for the menu. Loaded from the nuke search path.                 tooltip   The tooltip text.                 index     The position to insert the menu in. Use -1 to add to the end of the menu. @return: The submenu that was added."""
		return self._nukeNode.addMenu(**kwargs)
	#----------------------------------------------------------------------
	def name(self):
		"""self.name() -> String Returns the name of the menu item."""
		return self._nukeNode.name()
	#----------------------------------------------------------------------
	def removeItem(self,name):
		"""self.removeItem(name) -> None Removes a submenu or command with a particular name. If the containing menu becomes empty, it will be removed too. @param name: The name to remove for. @return: true if removed, false if menu not found """
		return self._nukeNode.removeItem(name)
	#----------------------------------------------------------------------
	def items(self):
		"""self.items() -> None Returns a list of sub menu items."""
		return list(self._nukeNode.items())
	#----------------------------------------------------------------------
	def findItem(self,name):
		"""self.findItem(name) -> Menu or None Finds a submenu or command with a particular name. @param name: The name to search for. @return: The submenu or command we found, or None if we could not find anything."""
		return self._nukeNode.findItem(name)
	#----------------------------------------------------------------------
	def clearMenu(self):
		"""self.clearMenu()  Clears a menu. @param **kwargs The following keyword arguments are accepted:                 name      The name for the menu/toolbar item @return: true if cleared, false if menu not found """
		return self._nukeNode.clearMenu()
################################################################################
class Undo(object):
	#----------------------------------------------------------------------
	def disabled(self):
		"""True if disable() has been called"""
		return self._nukeNode.disabled()
	#----------------------------------------------------------------------
	def undoDescribe(self):
		"""Return short description of undo n."""
		return self._nukeNode.undoDescribe()
	#----------------------------------------------------------------------
	def cancel(self):
		"""Undoes any actions recorded in the current set and throws it away."""
		return self._nukeNode.cancel()
	#----------------------------------------------------------------------
	def redo(self):
		"""Redoes 0'th redo."""
		return self._nukeNode.redo()
	#----------------------------------------------------------------------
	def undoSize(self):
		"""Number of undo's that can be done."""
		return self._nukeNode.undoSize()
	#----------------------------------------------------------------------
	def end(self):
		"""Complete current undo set and add it to the undo list."""
		return self._nukeNode.end()
	#----------------------------------------------------------------------
	def redoDescribe(self):
		"""Return short description of redo n."""
		return self._nukeNode.redoDescribe()
	#----------------------------------------------------------------------
	def __enter__(self):
		""""""
		return self._nukeNode.__enter__()
	#----------------------------------------------------------------------
	def redoDescribeFully(self):
		"""Return long description of redo n."""
		return self._nukeNode.redoDescribeFully()
	#----------------------------------------------------------------------
	def new(self):
		"""Same as end();begin()."""
		return self._nukeNode.new()
	#----------------------------------------------------------------------
	def redoTruncate(self):
		"""Destroy any redo's greater or equal to n."""
		return self._nukeNode.redoTruncate()
	#----------------------------------------------------------------------
	def undoTruncate(self):
		"""Destroy any undo's greater or equal to n."""
		return self._nukeNode.undoTruncate()
	#----------------------------------------------------------------------
	def begin(self):
		"""Begin a new user-visible group of undo actions."""
		return self._nukeNode.begin()
	#----------------------------------------------------------------------
	def enable(self):
		"""Undoes the previous disable()"""
		return self._nukeNode.enable()
	#----------------------------------------------------------------------
	def __exit__(self):
		""""""
		return self._nukeNode.__exit__()
	#----------------------------------------------------------------------
	def undo(self):
		"""Undoes 0'th undo."""
		return self._nukeNode.undo()
	#----------------------------------------------------------------------
	def disable(self):
		"""Prevent recording undos until matching enable()"""
		return self._nukeNode.disable()
	#----------------------------------------------------------------------
	def redoSize(self):
		"""Number of redo's that can be done."""
		return self._nukeNode.redoSize()
	#----------------------------------------------------------------------
	def name(self):
		"""Name current undo set."""
		return self._nukeNode.name()
	#----------------------------------------------------------------------
	def undoDescribeFully(self):
		"""Return long description of undo n."""
		return self._nukeNode.undoDescribeFully()
################################################################################
class View(object):
	#----------------------------------------------------------------------
	def __str__(self):
		"""x.__str__() <==> str(x)"""
		return self._nukeNode.__str__()
	#----------------------------------------------------------------------
	def value(self):
		"""self.value() -> Value of view. @return: Value of view."""
		return self._nukeNode.value()

	#----------------------------------------------------------------------
	def string(self):
		"""self.string() -> Name of view. @return: Name of view."""
		return self._nukeNode.string()

################################################################################
class ViewerProcess(object):
	#----------------------------------------------------------------------
	def unregister(self,name):
		"""nuke.ViewerProcess.unregister(name) -> None. Unregister a ViewerProcess. This is a class method. @param name: Menu name. @return: None."""
		return self._nukeNode.unregister(name)
	#----------------------------------------------------------------------
	def node(self):
		"""nuke.ViewerProcess.node(name, viewer) -> Node. Returns a ViewerProcess node. Default is to return the current selected one. This is a class method. @param name: Optional ViewerProcess name. @param viewer: Optional viewer name. @return: Node."""
		return self._nukeNode.node()
	#----------------------------------------------------------------------
	def register(self):
		"""nuke.ViewerProcess.register(name, call, args, kwargs) -> None. Register a ViewerProcess. This is a class method. @param name: Menu name. @param call: Python callable. Must return a Node. @param args: Arguments to call. @param kwargs: Optional named arguments. @return: None."""
		return self._nukeNode.register()
	#----------------------------------------------------------------------
	def registeredNames(self):
		"""nuke.ViewerProcess.registeredNames() -> List. Returns a list containing the names of all currently regisered ViewerProcesses. @return: List."""
		return self._nukeNode.registeredNames()

################################################################################
class ViewerWindow(object):
	#----------------------------------------------------------------------
	def node(self):
		"""self.node() -> Node. Returns the Viewer node currently associated with this window. @return: Node."""
		return self._nukeNode.node()
	#----------------------------------------------------------------------
	def activeInput(self,secondary=False):
		"""self.activeInput(secondary=False) -> int Returns the currently active input of the viewer - i. e. the one with its image in the output window. @param secondary: True to return the index of the active secondary (wipe) input, or False (the default) to return the primary input. @return: int: The currently active input of the viewer, starting with 0 for the first, or None if no input is active."""
		return self._nukeNode.activeInput(secondary=False)
	#----------------------------------------------------------------------
	def play(self):
		"""Play forward (1) or reverse (0)."""
		return self._nukeNode.play()
	#----------------------------------------------------------------------
	def previousView(self):
		"""self.previousView() -> switch to previous view in settings Views list. """
		return self._nukeNode.previousView()
	#----------------------------------------------------------------------
	def nextView(self):
		"""self.nextView() -> switch to next view in settings Views list. """
		return self._nukeNode.nextView()
	#----------------------------------------------------------------------
	def getGLCameraMatrix(self):
		"""self.getGLCameraMatrix() -> Matrix4 Return the world transformations of the current GL viewer camera. @return: Matrix4: GL camera world transformation."""
		return self._nukeNode.getGLCameraMatrix()
	#----------------------------------------------------------------------
	def getGeometryNodes(self):
		"""self.getGeometry() -> None Returns the a list of geometry nodes attached with this viewer @return: Nodes: a list of the geometry nodes."""
		return self._nukeNode.getGeometryNodes()
	#----------------------------------------------------------------------
	def stop(self):
		"""Stop playing."""
		return self._nukeNode.stop()
	#----------------------------------------------------------------------
	def activateInput(self):
		"""self.activateInput(input, secondary=False) -> None Set the given viewer input to be active - i. e. show its image in the output window. @param input: The viewer input number, starting with 0 for the first.  If the input is not connected, a ValueError exception is raised. @param secondary: True if the input should be connected as the secondary (wipe) input, or False to connect it as the primary input (the default). @return: None"""
		return self._nukeNode.activateInput()
	#----------------------------------------------------------------------
	def setView(self,s):
		"""self.setView(s) -> set 'current' multi-view view to 's'. """
		return self._nukeNode.setView(s)
	#----------------------------------------------------------------------
	def frameControl(self,i):
		"""self.frameControl(i) -> True.  i is an integer indicating viewer frame control 'button' to execute:     -6 go to start    -5 play reverse    -4 go to previous keyframe    -3 step back by increment    -2 go back previous keyframe or increment, whichever is closer    -1 step back one frame      0 stop     +1 step forward one frame    +2 go to next keyframe or increment, whichever is closer    +3 step forward by increment    +4 go to next keyframe    +5 play forward    +6 go to end"""
		return self._nukeNode.frameControl(i)
	#----------------------------------------------------------------------
	def view(self):
		"""self.view() -> string name of 'current' multi-view view. """
		return self._nukeNode.view()


################################################################################
################################################################################ Knob Class's
################################################################################



################################################################################
class Knob(object):
	"""Wrapper class for a nuke Node type"""
	##----------------------------------------------------------------------
	#def __init__(self,*args,**kwargs):
		#fn = getattr(nuke,self.__class__.__name__)
		#self._nukeNode = None
		#if len(args):
			#if isinstance(args[0],nuke.Knob):
				#self._nukeNode = args[0]

			#elif isinstance(args[0], Knob):
				#self._nukeNode = args[0]._nukeNode

		#if self._nukeNode == None:
			#if kwargs.has_key("inputs"):
				#kwargs["inputs"]=get_nukeNode_list(kwargs["inputs"])
			#self._nukeNode = fn(**kwargs)
	##----------------------------------------------------------------------
	#def __getattribute__(self,name):
		#try:
			#return super(NukeNode,self).__getattribute__(name)
		#except:
			#obj = super(NukeNode,self).__getattribute__("_nukeNode")
			#if hasattr(obj,name):
				#return getattr(obj,name)
			#else:
				#return object.__getattribute__(self,name)

	#----------------------------------------------------------------------
	def clearAnimated(self):
		"""Clear animation for channel 'c'. Return True if successful."""
		return self._nukeNode.clearAnimated()
	#----------------------------------------------------------------------
	def setLabel(self,s):
		"""self.setLabel(s) -> None. @param s: New label. @return: None."""
		return self._nukeNode.setLabel(s)
	#----------------------------------------------------------------------
	def setTooltip(self,s):
		"""self.setTooltip(s) -> None. @param s: New tooltip. @return: None."""
		return self._nukeNode.setTooltip(s)
	#----------------------------------------------------------------------
	def removeKey(self):
		"""Remove key for channel 'c'. Return True if successful."""
		return self._nukeNode.removeKey()
	#----------------------------------------------------------------------
	def getFlag(self,f):
		"""self.getFlag(f) -> Bool. Returns whether the input flag is set. @param f: Flag. @return: True if set, False otherwise."""
		return self._nukeNode.getFlag(f)
	#----------------------------------------------------------------------
	def setEnabled(self,enabled):
		"""self.setEnabled(enabled) -> None.  Enable or disable the knob. @param enabled: True to enable the knob, False to disable it."""
		return self._nukeNode.setEnabled(enabled)
	#----------------------------------------------------------------------
	def removeKeyAt(self):
		"""Remove key at time 't' for channel 'c'. Return True if successful."""
		return self._nukeNode.removeKeyAt()
	#----------------------------------------------------------------------
	def visible(self):
		"""self.visible() -> Boolean.  @return: True if the knob is visible, False if it's hidden."""
		return self._nukeNode.visible()
	#----------------------------------------------------------------------
	def warning(self,message):
		"""self.warning(message) -> None. @param message: message to put a warning on the knob. @return: None."""
		return self._nukeNode.warning(message)
	#----------------------------------------------------------------------
	def getIntegral(self):
		"""Return integral at the interval [t1, t2] for channel 'c'."""
		return self._nukeNode.getIntegral()
	#----------------------------------------------------------------------
	def isKeyAt(self):
		"""Return True if there is a keyframe at time 't' for channel 'c'."""
		return self._nukeNode.isKeyAt()
	#----------------------------------------------------------------------
	def hasExpression(self,index=-1):
		"""self.hasExpression(index=-1) -> bool Return True if animation at index 'index' has an expression. @param index: Optional index parameter. Defaults to -1 if not specified. This can be specified as a keyword parameter if desired. @return: True if has expression, False otherwise."""
		return self._nukeNode.hasExpression(index=-1)
	#----------------------------------------------------------------------
	def getKeyTime(self):
		"""Return index of the keyframe at time 't' for channel 'c'."""
		return self._nukeNode.getKeyTime()
	#----------------------------------------------------------------------
	def tooltip(self):
		"""self.tooltip() -> tooltip. @return: tooltip."""
		return self._nukeNode.tooltip()
	#----------------------------------------------------------------------
	def label(self):
		"""self.label() -> label. @return: label."""
		return self._nukeNode.label()
	#----------------------------------------------------------------------
	def setFlag(self,f):
		"""self.setFlag(f) -> None. Logical OR of the argument and existing knob flags. @param f: Flag. @return: None."""
		return self._nukeNode.setFlag(f)
	#----------------------------------------------------------------------
	def getNumKeys(self):
		"""Return number of keyframes for channel 'c'."""
		return self._nukeNode.getNumKeys()
	#----------------------------------------------------------------------
	def critical(self,message):
		"""self.critical(message) -> None. @param message: message to put the knob in error, and do a popup. @return: None."""
		return self._nukeNode.critical(message)
	#----------------------------------------------------------------------
	def toScript(self):
		"""toScript(quote, context=current) -> string.  Return the value of the knob in script syntax. Pass True for quote to return results quoted in {}. Pass None for context to get results for all views and key times (as stored in a .nk file)."""
		return self._nukeNode.toScript()
	#----------------------------------------------------------------------
	def clearFlag(self,f):
		"""self.clearFlag(f) -> None. Clear flag. @param f: Flag. @return: None."""
		return self._nukeNode.clearFlag(f)
	#----------------------------------------------------------------------
	def Class(self):
		"""self.Class() -> Class name. @return: Class name."""
		return self._nukeNode.Class()
	#----------------------------------------------------------------------
	def node(self):
		"""self.node() -> nuke.Node Return the node that this knob belongs to. If the node has been cloned, we'll always return a reference to the original. @return: The node which owns this knob, or None if the knob has no owner yet."""
		return self._nukeNode.node()
	#----------------------------------------------------------------------
	def fullyQualifiedName(self,channel=-1):
		"""self.fullyQualifiedName(channel=-1) -> string Returns the fully-qualified name of the knob within the node. This can be useful for expression linking.  @param channel: Optional parameter, specifies the channel number of the sub-knob (for example, channels of  0 and 1 would refer to the x and y of a XY_Knob respectively), leave blank or set to -1 to get the  qualified name of the knob only. @return: The string of the qualified knob or sub-knob, which can be used directly in expression links."""
		return self._nukeNode.fullyQualifiedName(channel=-1)
	#----------------------------------------------------------------------
	def setValue(self):
		"""self.setValue(val, chan) -> bool  Sets the value 'val' at channel 'chan'. @return: True if successful, False if not."""
		return self._nukeNode.setValue()
	#----------------------------------------------------------------------
	def setName(self,s):
		"""self.setName(s) -> None. @param s: New name. @return: None."""
		return self._nukeNode.setName(s)
	#----------------------------------------------------------------------
	def isAnimated(self):
		"""Return True if channel 'c' is animated."""
		return self._nukeNode.isAnimated()
	#----------------------------------------------------------------------
	def setAnimated(self, c):
		"""Set channel 'c' to be animated."""
		return self._nukeNode.setAnimated(c)
	#----------------------------------------------------------------------
	def getDerivative(self):
		"""Return derivative at time 't' for channel 'c'."""
		return self._nukeNode.getDerivative()
	#----------------------------------------------------------------------
	def setExpression(self):
		"""self.setExpression(expr, channel=-1, view=None) -> bool Set the expression for a knob. You can optionally specify a channel to set the expression for.  @param expr: The new expression for the knob. This should be a string. @param channel: Optional parameter, specifying the channel to set the expression for. This should be an integer. @param view: Optional view parameter. Without, this command will set the expression for the current view theinterface is displaying. Can be the name of the view or the index. @return: True if successful, False if not."""
		return self._nukeNode.setExpression()
	#----------------------------------------------------------------------
	def setValueAt(self):
		"""self.setValueAt(val, time, chan) -> bool  Sets the value 'val' at channel 'chan' for time 'time'. @return: True if successful, False if not."""
		return self._nukeNode.setValueAt()
	#----------------------------------------------------------------------
	def getNthDerivative(self):
		"""Return nth derivative at time 't' for channel 'c'."""
		return self._nukeNode.getNthDerivative()
	#----------------------------------------------------------------------
	def getValueAt(self):
		"""Return value at time 't' for channel 'c'."""
		return self._nukeNode.getValueAt()
	#----------------------------------------------------------------------
	def name(self):
		"""self.name() -> name. @return: name."""
		return self._nukeNode.name()
	#----------------------------------------------------------------------
	def isKey(self):
		"""Return True if there is a keyframe at the current frame for channel 'c'."""
		return self._nukeNode.isKey()
	#----------------------------------------------------------------------
	def fromScript(self):
		"""Initialise from script."""
		return self._nukeNode.fromScript()
	#----------------------------------------------------------------------
	def enabled(self):
		"""self.enabled() -> Boolean.  @return: True if the knob is enabled, False if it's disabled."""
		return self._nukeNode.enabled()
	#----------------------------------------------------------------------
	def value(self):
		"""Return value at the current frame for channel 'c'."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def getValue(self):
		"""Return value at the current frame for channel 'c'."""
		return self._nukeNode.getValue()
	#----------------------------------------------------------------------
	def getKeyIndex(self):
		"""Return keyframe index at time 't' for channel 'c'."""
		return self._nukeNode.getKeyIndex()
	#----------------------------------------------------------------------
	def error(self,message):
		"""self.error(message) -> None. @param message: message to put the knob in error. @return: None."""
		return self._nukeNode.error(message)
	#----------------------------------------------------------------------
	def debug(self,message):
		"""self.debug(message) -> None. @param message: message to put out to the error console, attached to the knob, if the verbosity level is set high enough. @return: None."""
		return self._nukeNode.debug(message)
	#----------------------------------------------------------------------
	def setVisible(self,visible):
		"""self.setVisible(visible) -> None.  Show or hide the knob. @param visible: True to show the knob, False to hide it."""
		return self._nukeNode.setVisible(visible)
################################################################################
class Array_Knob(Knob):
	#----------------------------------------------------------------------
	def clearAnimated(self):
		"""self.clearAnimated(index, view) -> True if succeeded, False otherwise. Delete animation. @param index: Optional index. @param view: Optional view. @return: True if succeeded, False otherwise."""
		return self._nukeNode.clearAnimated()
	#----------------------------------------------------------------------
	def removeKey(self):
		"""self.removeKey(index, view) -> True if succeeded, False otherwise. Remove key. @param index: Optional index. @param view: Optional view. @return: True if succeeded, False otherwise."""
		return self._nukeNode.removeKey()
	#----------------------------------------------------------------------
	def setValueAt(self):
		"""self.setValueAt(value, time, index, view) -> bool. Set value of element 'index' at time for view. If the knob is animated, it will set a new keyframe or change an existing one. Index and view are optional. Return True if successful. @param value: Floating point value. @param time: Time. @param index: Optional index. @param view: Optional view. @return: True if value changed, False otherwise. Safe to ignore."""
		return self._nukeNode.setValueAt()
	#----------------------------------------------------------------------
	def frame(self):
		"""self.frame() -> Frame number. @return: Frame number."""
		return self._nukeNode.frame()
	#----------------------------------------------------------------------
	def removeKeyAt(self):
		"""self.removeKeyAt(time, index, view) -> True if succeeded, False otherwise. Remove keyframe at specified time, optional index and view. Return True if successful. @param time: Time. @param index: Optional index. @param view: Optional view. @return: True if succeeded, False otherwise."""
		return self._nukeNode.removeKeyAt()
	#----------------------------------------------------------------------
	def height(self):
		"""self.height() -> Height of array of values. @return: Height of array of values."""
		return self._nukeNode.height()
	#----------------------------------------------------------------------
	def minimum(self):
		"""self.min() -> Minimum value. @return: Minimum value."""
		return self._nukeNode.minimum()
	#----------------------------------------------------------------------
	def unsplitView(self,view):
		"""self.unsplitView(view) -> None. Unsplit the view so that it shares a value with other views. @param view: Optional view. Default is current view. @return: None."""
		return self._nukeNode.unsplitView(view)
	#----------------------------------------------------------------------
	def array(self):
		"""self.array() -> List of knob values. @return: List of knob values."""
		return self._nukeNode.array()
	#----------------------------------------------------------------------
	def getIntegral(self):
		"""Return integral at time interval [t1, t2] and index 'i'."""
		return self._nukeNode.getIntegral()
	#----------------------------------------------------------------------
	def singleValue(self,view):
		"""self.singleValue(view) -> True if holds a single value. @param view: Optional view. Default is current view. @return: True if holds a single value."""
		return self._nukeNode.singleValue(view)
	#----------------------------------------------------------------------
	def isKeyAt(self):
		"""self.isKeyAt(time, index, view) -> True if succeeded, False otherwise. Returns True if there is a keyframe at specified time, optional index and view, otherwise returns False. @param time: Time. @param index: Optional index. @param view: Optional view. @return: True if succeeded, False otherwise."""
		return self._nukeNode.isKeyAt()
	#----------------------------------------------------------------------
	def hasExpression(self,index):
		"""self.hasExpression(index) -> True if has expression, False otherwise. @param index: Optional index. @return: True if has expression, False otherwise."""
		return self._nukeNode.hasExpression(index)
	#----------------------------------------------------------------------
	def setKeyAt(self):
		"""self.setKeyAt(time, index, view) -> None. Set a key on element 'index', at time and view. @param time: Time. @param index: Optional index. @param view: Optional view. @return: None."""
		return self._nukeNode.setKeyAt()
	#----------------------------------------------------------------------
	def min(self):
		"""self.min() -> Minimum value. @return: Minimum value."""
		return self._nukeNode.min()
	#----------------------------------------------------------------------
	def defaultValue(self):
		"""self.defaultValue() -> Default value. @return: Default value."""
		return self._nukeNode.defaultValue()
	#----------------------------------------------------------------------
	def getKeyTime(self):
		"""Return time of the keyframe at time 't' and channel 'c'."""
		return self._nukeNode.getKeyTime()
	#----------------------------------------------------------------------
	def deleteAnimation(self,curve):
		"""self.deleteAnimation(curve) -> None. Raises ValueError if not found. Deletes the AnimationCurve. @param curve: An AnimationCurve instance which belongs to this Knob. @return: None. Raises ValueError if not found."""
		return self._nukeNode.deleteAnimation(curve)
	#----------------------------------------------------------------------
	def width(self):
		"""self.width() -> Width of array of values. @return: Width of array of values."""
		return self._nukeNode.width()
	#----------------------------------------------------------------------
	def getNumKeys(self):
		"""Return number of keys at channel 'c'."""
		return self._nukeNode.getNumKeys()
	#----------------------------------------------------------------------
	def valueAt(self):
		"""self.valueAt(time, index, view) -> Floating point or List of floating point values (in case some are different). Return value for this knob at specified time, optional index and view. @param time: Time. @param index: Optional index. Default is 0. @param view: Optional view. @return: Floating point or List of floating point values (in case some are different)."""
		return self._nukeNode.valueAt()
	#----------------------------------------------------------------------
	def arraySize(self):
		"""self.arraySize() -> Number of elements in array. @return: Number of elements in array."""
		return self._nukeNode.arraySize()
	#----------------------------------------------------------------------
	def max(self):
		"""self.max() -> Maximum value. @return: Maximum value."""
		return self._nukeNode.max()
	#----------------------------------------------------------------------
	def setSingleValue(self):
		"""self.setSingleValue(b, view) -> None. Set to just hold a single value or not. @param b: Boolean object. @param view: Optional view. Default is current view. @return: None."""
		return self._nukeNode.setSingleValue()
	#----------------------------------------------------------------------
	def toScript(self):
		"""self.toScript(quote, context) -> String. Return the value of the knob in script syntax. @param quote: Optional, default is False. Specify True to return the knob value quoted in {}. @param context: Optional context, default is current, None will be "contextless" (all views, all keys) as in a .nk file. @return: String."""
		return self._nukeNode.toScript()
	#----------------------------------------------------------------------
	def notDefault(self):
		"""self.notDefault() -> True if any of the values is not set to the default, False otherwise. @return: True if any of the values is not set to the default, False otherwise."""
		return self._nukeNode.notDefault()
	#----------------------------------------------------------------------
	def splitView(self,view):
		"""self.splitView(view) -> None. Split the view away from the current knob value. @param view: Optional view. Default is current view. @return: None."""
		return self._nukeNode.splitView(view)
	#----------------------------------------------------------------------
	def setValue(self):
		"""self.setValue(value, index, time, view) -> True if value changed, False otherwise. Safe to ignore. Set index to value at time and view. @param value: Floating point value. @param index: Optional index. @param time: Optional time. @param view: Optional view. @return: True if value changed, False otherwise. Safe to ignore."""
		return self._nukeNode.setValue()
	#----------------------------------------------------------------------
	def isAnimated(self):
		"""self.isAnimated(index, view) -> True if animated, False otherwise. @param index: Optional index. @param view: Optional view. @return: True if animated, False otherwise."""
		return self._nukeNode.isAnimated()
	#----------------------------------------------------------------------
	def copyAnimations(self):
		"""self.copyAnimations(curves, view) -> None. Copies the AnimationCurves from curves to this object. The view is optional and defaults to the current view. @param curves: AnimationCurve list. @param view: Optional view. Defaults to current. @return: None."""
		return self._nukeNode.copyAnimations()
	#----------------------------------------------------------------------
	def setDefaultValue(self,s):
		"""self.setDefaultValue(s) -> None. @param s: Sequence of floating-point values. @return: None."""
		return self._nukeNode.setDefaultValue(s)
	#----------------------------------------------------------------------
	def dimensions(self):
		"""self.dimensions() -> Dimensions in array. @return: Dimensions in array."""
		return self._nukeNode.dimensions()
	#----------------------------------------------------------------------
	def vect(self):
		"""self.vect() -> List of knob values. @return: List of knob values."""
		return self._nukeNode.vect()
	#----------------------------------------------------------------------
	def animations(self,view):
		"""self.animations(view) -> AnimationCurve list. @param view: Optional view. @return: AnimationCurve list. Example: b = nuke.nodes.Blur() k = b['size'] k.setAnimated(0) a = k.animations() a[0].setKey(0, 11) a[0].setKey(10, 20)"""
		return self._nukeNode.animations(view)
	#----------------------------------------------------------------------
	def setAnimated(self):
		"""self.setAnimated(index, view) -> True if succeeded, False otherwise. Create an Animation object. Return True if successful, in which case caller must initialise it by calling setValue() or setValueAt(). @param index: Optional index. @param view: Optional view. @return: True if succeeded, False otherwise."""
		return self._nukeNode.setAnimated()
	#----------------------------------------------------------------------
	def getDerivative(self):
		"""Return derivative at time 't' and index 'i'."""
		return self._nukeNode.getDerivative()
	#----------------------------------------------------------------------
	def setExpression(self):
		"""self.setExpression(expr, channel=-1, view=None) -> bool Set the expression for a knob. You can optionally specify a channel to set the expression for.  @param expr: The new expression for the knob. This should be a string. @param channel: Optional parameter, specifying the channel to set the expression for. This should be an integer. @param view: Optional view parameter. Without, this command will set the expression for the current view theinterface is displaying. Can be the name of the view or the index. @return: True if successful, False if not."""
		return self._nukeNode.setExpression()
	#----------------------------------------------------------------------
	def animation(self):
		"""self.animation(chan, view) -> AnimationCurve or None. Return the AnimationCurve for the  channel 'chan' and view 'view'. The view argument is optional. @param channel: The channel index. @param view: Optional view. @return: AnimationCurve or None."""
		return self._nukeNode.animation()
	#----------------------------------------------------------------------
	def resize(self):
		"""self.resize(w, h) -> True if successful, False otherwise. Resize the array. @param w: New width @param h: Optional new height @return: True if successful, False otherwise."""
		return self._nukeNode.resize()
	#----------------------------------------------------------------------
	def setRange(self):
		"""self.setRange(f1, f2) -> None. Set range of values. @param f1 Min value. @param f2 Max value. @return: None."""
		return self._nukeNode.setRange()
	#----------------------------------------------------------------------
	def getValueAt(self):
		"""self.valueAt(time, index, view) -> Floating point or List of floating point values (in case some are different). Return value for this knob at specified time, optional index and view. @param time: Time. @param index: Optional index. Default is 0. @param view: Optional view. @return: Floating point or List of floating point values (in case some are different)."""
		return self._nukeNode.getValueAt()
	#----------------------------------------------------------------------
	def getNthDerivative(self):
		"""Return n'th derivative at time 't' and index 'i'."""
		return self._nukeNode.getNthDerivative()
	#----------------------------------------------------------------------
	def isKey(self):
		"""self.isKey(index, view) -> True if succeeded, False otherwise. @param index: Optional index. @param view: Optional view. @return: True if succeeded, False otherwise."""
		return self._nukeNode.isKey()
	#----------------------------------------------------------------------
	def fromScript(self,s):
		"""self.fromScript(s) -> True if successful, False otherwise. Set value of the knob to a user defined script (TCL syntax, as in .nk file). Return True if successful. @param s: Nuke script to be set on knob. @return: True if successful, False otherwise."""
		return self._nukeNode.fromScript(s)
	#----------------------------------------------------------------------
	def maximum(self):
		"""self.max() -> Maximum value. @return: Maximum value."""
		return self._nukeNode.maximum()
	#----------------------------------------------------------------------
	def value(self):
		"""self.value(index, view, time) -> Floating point or List of floating point values (in case some are different). @param index: Optional index. Default is 0. @param view: Optional view. @param time: Optional time. @return: Floating point or List of floating point values (in case some are different)."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def getValue(self):
		"""self.value(index, view, time) -> Floating point or List of floating point values (in case some are different). @param index: Optional index. Default is 0. @param view: Optional view. @param time: Optional time. @return: Floating point or List of floating point values (in case some are different)."""
		return self._nukeNode.getValue()
	#----------------------------------------------------------------------
	def getKeyIndex(self):
		"""Return index of the keyframe at time 't' and channel 'c'."""
		return self._nukeNode.getKeyIndex()
	#----------------------------------------------------------------------
	def copyAnimation(self):
		"""self.copyAnimation(channel, curve, view) -> None. Copies the i'th channel of the AnimationCurve curve to this object. The view is optional and defaults to the current view. @param channel: The channel index. @param curve: AnimationCurve. @param view: Optional view. Defaults to current. @return: None."""
		return self._nukeNode.copyAnimation()
################################################################################
class Unsigned_Knob(Array_Knob):
	#----------------------------------------------------------------------
	def value(self):
		"""self.value() -> int Get the value of this knob as an integer. @return: int"""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def setValue(self,val):
		"""self.setValue(val) -> bool Set the unsigned integer value of this knob. @param val: The new value for the knob. Must be an integer >= 0. @return: True if succeeded, False otherwise."""
		return self._nukeNode.setValue(val)
################################################################################
class Color_Knob(Array_Knob):
	#----------------------------------------------------------------------
	def inputNumber(self):
		"""inputNumber() -> int  Return input number."""
		return self._nukeNode.inputNumber()
	#----------------------------------------------------------------------
	def names(self,n):
		"""names(n) -> string  Return name for dimension n. The argument n is an integer."""
		return self._nukeNode.names(n)
################################################################################
class AColor_Knob(Color_Knob):
	pass
################################################################################
class Axis_Knob(Knob):
	#----------------------------------------------------------------------
	def uniformScale(self):
		"""self.uniformScale() -> Double_Knob  Return uniform scale knob."""
		return self._nukeNode.uniformScale()
	#----------------------------------------------------------------------
	def rotate(self):
		"""self.rotate() -> XYZ_Knob  Return rotation knob."""
		return self._nukeNode.rotate()
	#----------------------------------------------------------------------
	def skew(self):
		"""self.skew() -> XYZ_Knob  Return skew knob."""
		return self._nukeNode.skew()
	#----------------------------------------------------------------------
	def value(self):
		"""self.value() -> _nukemath.Matrix4 Return the transform matrix formed by combining the input knob values for translate, rotate, scale, skew and pivot."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def scale(self):
		"""self.scale() -> Scale_Knob  Return scale knob."""
		return self._nukeNode.scale()
	#----------------------------------------------------------------------
	def pivot(self):
		"""self.pivot() -> XYZ_Knob  Return pivot knob."""
		return self._nukeNode.pivot()
	#----------------------------------------------------------------------
	def translate(self):
		"""self.translate() -> XYZ_Knob  Return translation knob."""
		return self._nukeNode.translate()
################################################################################
class BBox_Knob(Array_Knob):
	#----------------------------------------------------------------------
	def value(self):
		"""Return value for dimension 'i'"""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def setT(self):
		"""Set value for T extent."""
		return self._nukeNode.setT()
	#----------------------------------------------------------------------
	def fromDict(self,box):
		"""self.fromDict(box) -> None  Set the bounding box from the given box. @param box: Dictionary containing the x, y, r and t keys. @return: None"""
		return self._nukeNode.fromDict(box)
	#----------------------------------------------------------------------
	def r(self):
		"""Return value for R extent."""
		return self._nukeNode.r()
	#----------------------------------------------------------------------
	def names(self):
		"""Return name for dimension 'i'"""
		return self._nukeNode.names()
	#----------------------------------------------------------------------
	def setR(self):
		"""Set value for R extent."""
		return self._nukeNode.setR()
	#----------------------------------------------------------------------
	def toDict(self):
		"""self.toDict() -> dict.  Returns the bounding box as a dict with x, y, r, and t keys. @return: dict with x, y, r and t keys"""
		return self._nukeNode.toDict()
	#----------------------------------------------------------------------
	def y(self):
		"""Return value for Y position."""
		return self._nukeNode.y()
	#----------------------------------------------------------------------
	def x(self):
		"""Return value for X position."""
		return self._nukeNode.x()
	#----------------------------------------------------------------------
	def setX(self):
		"""Set value for X position."""
		return self._nukeNode.setX()
	#----------------------------------------------------------------------
	def setY(self):
		"""Set value for Y position."""
		return self._nukeNode.setY()
	#----------------------------------------------------------------------
	def t(self):
		"""Return value for T extent."""
		return self._nukeNode.t()

################################################################################
class Enumeration_Knob(Unsigned_Knob):
	#----------------------------------------------------------------------
	def setValue(self,item):
		"""self.setValue(item) -> None. Set the current value. If item is of an Integer type it will treat it as an index to the enum, otherwise as a value. @param item: String or Integer. @return: None. Example: w = nuke.nodes.Write() k = w['file_type'] k.setValue('exr')"""
		return self._nukeNode.setValue(item)
	#----------------------------------------------------------------------
	def numValues(self):
		"""self.numValues() -> int  Return number of values. Deprecated."""
		return self._nukeNode.numValues()
	#----------------------------------------------------------------------
	def value(self):
		"""self.value() -> String. Current value. @return: String. Example: w = nuke.nodes.Write() k = w['file_type'] k.value()"""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def enumName(self,n):
		"""self.enumName(n) -> string  Return name of enumeration n. The argument n is an integer and in the range of 0 and numValues. Deprecated."""
		return self._nukeNode.enumName(n)
	#----------------------------------------------------------------------
	def values(self):
		"""self.values() -> List of strings. Return list of items. @return: List of strings. Example: w = nuke.nodes.Write() k = w['file_type'] k.values()"""
		return list(self._nukeNode.values())
	#----------------------------------------------------------------------
	def setValues(self,items):
		"""self.setValues(items) -> None. (Re)initialise knob to the supplied list of items. @param items: The new list of values. @return: None. Example: w = nuke.nodes.Write() k = w['file_type'] k.setValues(['exr'])"""
		return self._nukeNode.setValues(items)
################################################################################
class Bitmask_Knob(Enumeration_Knob):
	pass
################################################################################
class Boolean_Knob(Array_Knob):
	#----------------------------------------------------------------------
	def value(self):
		"""self.value() -> bool Get the boolean value for this knob. @return: True or False."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def setValue(self,b):
		"""self.setValue(b) -> bool Set the boolean value of this knob. @param b: Boolean convertible object. @return: True if modified, False otherwise."""
		return self._nukeNode.setValue(b)

################################################################################
class Box3_Knob(Array_Knob):
	#----------------------------------------------------------------------
	def setF(self,far):
		"""Set value for F extent. F (far) is the maximum Z extent of the box."""
		return self._nukeNode.setF(far)
	#----------------------------------------------------------------------
	def f(self,ar):
		"""Return value for F extent. F (far) is the maximum Z extent of the box."""
		return self._nukeNode.f(ar)
	#----------------------------------------------------------------------
	def setN(self,near):
		"""Set value for N position. N (near) is the minimum Z extent of the box."""
		return self._nukeNode.setN(near)
	#----------------------------------------------------------------------
	def value(self):
		"""Return value for dimension 'i'"""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def n(self,ear):
		"""Return value for N position. N (near) is the minimum Z extent of the box."""
		return self._nukeNode.n(ear)
	#----------------------------------------------------------------------
	def setT(self,top):
		"""Set value for T extent. T (top) is the maximum vertical extent of the box."""
		return self._nukeNode.setT(top)
	#----------------------------------------------------------------------
	def r(self,ight):
		"""Return value for R extent. R (right) is the right extent of the box."""
		return self._nukeNode.r(ight)
	#----------------------------------------------------------------------
	def names(self):
		"""Return name for dimension 'i'"""
		return self._nukeNode.names()
	#----------------------------------------------------------------------
	def setR(self,right):
		"""Set value for R extent. R (right) is the right extent of the box."""
		return self._nukeNode.setR(right)
	#----------------------------------------------------------------------
	def y(self):
		"""Return value for Y position. Y is the minimum vertical extent of the box."""
		return self._nukeNode.y()
	#----------------------------------------------------------------------
	def x(self):
		"""Return value for X position. X is the minimum horizontal extent of the box."""
		return self._nukeNode.x()
	#----------------------------------------------------------------------
	def setX(self):
		"""Set value for X position. X is the minimum horizontal extent of the box."""
		return self._nukeNode.setX()
	#----------------------------------------------------------------------
	def setY(self):
		"""Set value for Y position. Y is the minimum vertical extent of the box."""
		return self._nukeNode.setY()
	#----------------------------------------------------------------------
	def t(self,op):
		"""Return value for T extent. T (top) is the maximum vertical extent of the box."""
		return self._nukeNode.t(op)
################################################################################
class CascadingEnumeration_Knob(Enumeration_Knob):
	pass
################################################################################
class Channel_Knob(Knob):
	#----------------------------------------------------------------------
	def inputNumber(self):
		"""self.inputNumber() -> int"""
		return self._nukeNode.inputNumber()
	#----------------------------------------------------------------------
	def enableChannel(self):
		"""self.enableChannel(name, b) -> None  Enable or disable a channel. @param name: The name of the channel. @param b: True to enable the channel, False to disable it. @return: None"""
		return self._nukeNode.enableChannel()
	#----------------------------------------------------------------------
	def layerSelector(self):
		"""self.layerSelector() -> bool"""
		return self._nukeNode.layerSelector()
	#----------------------------------------------------------------------
	def setEnable(self,name):
		"""self.setEnable(name) -> None  Enable a channel. @param name: The name of the channel to enable. @return: None"""
		return self._nukeNode.setEnable(name)
	#----------------------------------------------------------------------
	def value(self):
		"""self.value() -> str Get the name of the selected channel. @return: The name of the channel as a string."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def checkMarks(self):
		"""self.checkMarks() -> bool"""
		return self._nukeNode.checkMarks()
	#----------------------------------------------------------------------
	def channelSelector(self):
		"""self.channelSelector() -> bool"""
		return self._nukeNode.channelSelector()
	#----------------------------------------------------------------------
	def depth(self):
		"""self.depth() -> int  Get the channel depth. @return: The depth of the channel as an int."""
		return self._nukeNode.depth()
	#----------------------------------------------------------------------
	def setValue(self,name):
		"""self.setValue(name) -> None Set the selected channel using the channel name. @param name: The name of the new channel as a string. @return: None @raise ValueError exception if the channel doesn't exist."""
		return self._nukeNode.setValue(name)
	#----------------------------------------------------------------------
	def setInput(self,num):
		"""self.setInput(num) -> None Set the input number for this knob.@param num: The number of the new input. @return: None"""
		return self._nukeNode.setInput(num)
	#----------------------------------------------------------------------
	def inputKnob(self):
		"""self.inputKnob() -> bool"""
		return self._nukeNode.inputKnob()
	#----------------------------------------------------------------------
	def isChannelEnabled(self,name):
		"""self.isChannelEnabled(name) -> bool  Test if a channel is enabled. @param name: The name of the channel.@return: True if the channel is enabled, False otherwise."""
		return self._nukeNode.isChannelEnabled(name)
################################################################################
class ChannelMask_Knob(Channel_Knob):
	pass
################################################################################
class ColorChip_Knob(Unsigned_Knob):
	pass
################################################################################
class Double_Knob(Array_Knob):
	pass
################################################################################
class EndTabGroup_Knob(Knob):
	pass
################################################################################
class String_Knob(Knob):
	#----------------------------------------------------------------------
	def splitView(self,view):
		"""self.splitView(view) -> None. Split the view away from the current knob value. @param view: Optional view. Default is current view. @return: None."""
		return self._nukeNode.splitView(view)
	#----------------------------------------------------------------------
	def setValue(self):
		"""self.setValue(val, view='default') -> None  Set value of knob. @param val: The new value. @param view: Optional parameter specifying which view to set the value for. If omitted, the value will be set for the default view. @return: None"""
		return self._nukeNode.setValue()
	#----------------------------------------------------------------------
	def setText(self):
		"""self.setValue(val, view='default') -> None  Set value of knob. @param val: The new value. @param view: Optional parameter specifying which view to set the value for. If omitted, the value will be set for the default view. @return: None"""
		return self._nukeNode.setText()
	#----------------------------------------------------------------------
	def getText(self,oc):
		"""self.value(oc) -> str  Get the value of this knob as a string. @param oc: Optional parameter specifying the output context. @return: String value."""
		return self._nukeNode.getText(oc)
	#----------------------------------------------------------------------
	def getValue(self,oc):
		"""self.value(oc) -> str  Get the value of this knob as a string. @param oc: Optional parameter specifying the output context. @return: String value."""
		return self._nukeNode.getValue(oc)
	#----------------------------------------------------------------------
	def value(self,oc):
		"""self.value(oc) -> str  Get the value of this knob as a string. @param oc: Optional parameter specifying the output context. @return: String value."""
		return self._nukeNode.value(oc)
	#----------------------------------------------------------------------
	def unsplitView(self,view):
		"""self.unsplitView(view) -> None. Unsplit the view so that it shares a value with other views. @param view: Optional view. Default is current view. @return: None."""
		return self._nukeNode.unsplitView(view)
################################################################################
class EvalString_Knob(String_Knob):
	#----------------------------------------------------------------------
	def evaluate(self):
		"""self.evaluate() -> String. Evaluate the string, performing substitutions. @return: String."""
		return self._nukeNode.evaluate()
################################################################################
class Eyedropper_Knob(AColor_Knob):
	pass
################################################################################
class File_Knob(EvalString_Knob):
	#----------------------------------------------------------------------
	def fromUserText(self,s):
		"""self.fromUserText(s) -> None. Assign string to knob, parses frame range off the end and opens file to get set the format. @param s: String to assign. @return: None."""
		return self._nukeNode.fromUserText(s)
	#----------------------------------------------------------------------
	def setValue(self,s):
		"""self.fromScript(s) -> None. Assign string to knob. @param s: String to assign. @return: None."""
		return self._nukeNode.setValue(s)
	#----------------------------------------------------------------------
	def fromScript(self,s):
		"""self.fromScript(s) -> None. Assign string to knob. @param s: String to assign. @return: None."""
		return self._nukeNode.fromScript(s)
	#----------------------------------------------------------------------
	def value(self):
		"""self.getEvaluatedValue() -> String. Returns the string on this knob, will be normalized to technical notation if sequence (%4d). @return: String."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def getValue(self):
		"""self.getEvaluatedValue() -> String. Returns the string on this knob, will be normalized to technical notation if sequence (%4d). @return: String."""
		return self._nukeNode.getValue()
	#----------------------------------------------------------------------
	def getEvaluatedValue(self,oc):
		"""self.getValue(oc) -> String. Returns the string on this knob, will be normalized to technical notation if sequence (%4d). Will also evaluate the string for any tcl expressions @parm oc: the output context to use, if None the knob uiContext will be used. @return: String."""
		return self._nukeNode.getEvaluatedValue(oc)
################################################################################
class Font_Knob(Knob):
	#----------------------------------------------------------------------
	def value(self):
		""""""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def setValue(self):
		""""""
		return self._nukeNode.setValue()


################################################################################
class Format_Knob(Knob):
	#----------------------------------------------------------------------
	def setValue(self,format):
		"""setValue(format) -> True if succeeded, False otherwise.  Set value of knob to format (either a Format object or a name of a format, e.g. "NTSC")."""
		return self._nukeNode.setValue(format)
	#----------------------------------------------------------------------
	def fromScript(self,s):
		"""fromScript(s) -> True if succeeded, False otherwise.  Initialise from script s."""
		return self._nukeNode.fromScript(s)
	#----------------------------------------------------------------------
	def value(self):
		"""value() -> Format.  Return value of knob."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def actualValue(self):
		"""actualValue() -> Format.  Return value of knob."""
		return self._nukeNode.actualValue()
	#----------------------------------------------------------------------
	def toScript(self):
		"""toScript(quote, context=current) -> string.  Return the value of the knob in script syntax. Pass True for quote to return results quoted in {}. Pass None for context to get results for all views and key times (as stored in a .nk file)."""
		return self._nukeNode.toScript()
	#----------------------------------------------------------------------
	def notDefault(self):
		"""notDefault() -> True if set to its default value, False otherwise."""
		return self._nukeNode.notDefault()
	#----------------------------------------------------------------------
	def name(self):
		"""name() -> string.  Return name of knob."""
		return self._nukeNode.name()

################################################################################
class GeoSelect_Knob(Knob):
	#----------------------------------------------------------------------
	def getSelection(self):
		"""self.getSelection() -> list of lists of floats Returns the selection weights for each vertex as a float. If you access the result as selection[obj][pt], then obj is the index of the object in the input geometry and pt is the index of the point in that object."""
		return self._nukeNode.getSelection()
	#----------------------------------------------------------------------
	def getGeometry(self):
		"""self.getGeometry() -> _geo.GeometryList Get the geometry which this knob can select from."""
		return self._nukeNode.getGeometry()

################################################################################
class Help_Knob(Knob):
	pass
################################################################################
class Histogram_Knob(Knob):
	pass
################################################################################
class IArray_Knob(Array_Knob):
	#----------------------------------------------------------------------
	def value(self):
		"""Return value of the array at position (x, y)."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def height(self):
		"""Return height of the array."""
		return self._nukeNode.height()
	#----------------------------------------------------------------------
	def width(self):
		"""Return width of the array."""
		return self._nukeNode.width()
	#----------------------------------------------------------------------
	def dimensions(self):
		"""Return number of dimensions."""
		return self._nukeNode.dimensions()

################################################################################
class Int_Knob(Array_Knob):
	#----------------------------------------------------------------------
	def value(self):
		"""self.value() -> int Get the integer value of this knob. @return: The value of this knob as an int."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def setValue(self,val):
		"""self.setValue(val) -> bool Set the integer value of this knob. @param val: The new value. Must be an integer. @return: True if succeeded, False otherwise."""
		return self._nukeNode.setValue(val)
################################################################################
class Keyer_Knob(Array_Knob):
	#----------------------------------------------------------------------
	def highTol(self):
		""""""
		return self._nukeNode.highTol()
	#----------------------------------------------------------------------
	def lowSoft(self):
		""""""
		return self._nukeNode.lowSoft()
	#----------------------------------------------------------------------
	def lowTol(self):
		""""""
		return self._nukeNode.lowTol()
	#----------------------------------------------------------------------
	def value(self):
		"""self.value(outputCtx, n) -> float  Get the value of argument n. @param outputCtx: The OutputContext to evaluate the argument in. @param n: The index of the argument to get the value of. @return: The value of argument n."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def names(self,n):
		"""self.names(n) -> string  @param n: The index of the name to return. @return: The name at position n."""
		return self._nukeNode.names(n)
	#----------------------------------------------------------------------
	def highSoft(self):
		""""""
		return self._nukeNode.highSoft()

################################################################################
class Link_Knob(Knob):
	#----------------------------------------------------------------------
	def setValue(self):
		"""setValue() -> None  Set value of knob."""
		return self._nukeNode.setValue()
	#----------------------------------------------------------------------
	def getLinkedKnob(self):
		"""getLinkedKnob() -> knob """
		return self._nukeNode.getLinkedKnob()
	#----------------------------------------------------------------------
	def value(self):
		"""value() -> string  Return value of knob."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def getLink(self):
		"""getLink() -> s """
		return self._nukeNode.getLink()
	#----------------------------------------------------------------------
	def setLink(self,s):
		"""setLink(s) -> None """
		return self._nukeNode.setLink(s)
	#----------------------------------------------------------------------
	def makeLink(self):
		"""makeLink(s, t) -> None """
		return self._nukeNode.makeLink()

################################################################################
class LookupCurves_Knob(Knob):
	#----------------------------------------------------------------------
	def delCurve(self,curve):
		"""self.delCurve(curve) -> None Deletes a curve. @param curve: The name of the animation curve. @return: None"""
		return self._nukeNode.delCurve(curve)
	#----------------------------------------------------------------------
	def editCurve(self):
		"""self.editCurve(curve, expr=None) -> None Edits an existing curve. @param curve: The name of an animation curve. @param expr: The new expression for the curve. @return: None"""
		return self._nukeNode.editCurve()
	#----------------------------------------------------------------------
	def addCurve(self):
		"""self.addCurve(curve, expr=None) -> None Adds a curve. @param curve: The name of an animation curve, or an AnimationCurve instance. @param expr: Optional parameter giving an expression for the curve. @return: None"""
		return self._nukeNode.addCurve()

################################################################################
class MultiView_Knob(Knob):
	#----------------------------------------------------------------------
	def toScriptPrefix(self):
		""""""
		return self._nukeNode.toScriptPrefix()
	#----------------------------------------------------------------------
	def setValue(self,s):
		"""fromScript(s) -> True if succeeded, False otherwise.  Initialise from script s."""
		return self._nukeNode.setValue(s)
	#----------------------------------------------------------------------
	def fromScript(self,s):
		"""fromScript(s) -> True if succeeded, False otherwise.  Initialise from script s."""
		return self._nukeNode.fromScript(s)
	#----------------------------------------------------------------------
	def value(self):
		"""toScript(quote, context=current) -> string.  Return the value of the knob in script syntax. Pass True for quote to return results quoted in {}. Pass None for context to get results for all views and key times (as stored in a .nk file)."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def toScriptPrefixUserKnob(self):
		""""""
		return self._nukeNode.toScriptPrefixUserKnob()
	#----------------------------------------------------------------------
	def toScript(self):
		"""toScript(quote, context=current) -> string.  Return the value of the knob in script syntax. Pass True for quote to return results quoted in {}. Pass None for context to get results for all views and key times (as stored in a .nk file)."""
		return self._nukeNode.toScript()
	#----------------------------------------------------------------------
	def notDefault(self):
		"""notDefault() -> True if set to its default value, False otherwise."""
		return self._nukeNode.notDefault()
################################################################################
class Multiline_Eval_String_Knob(EvalString_Knob):
	pass

################################################################################
class Obsolete_Knob(Knob):
	#----------------------------------------------------------------------
	def setValue(self):
		""""""
		return self._nukeNode.setValue()
	#----------------------------------------------------------------------
	def value(self):
		""""""
		return self._nukeNode.value()
################################################################################
class OneView_Knob(Enumeration_Knob):
	pass

################################################################################
class Password_Knob(Knob):
	#----------------------------------------------------------------------
	def setValue(self):
		"""self.setValue(val, view='default') -> None  Set value of knob. @param val: The new value. @param view: Optional parameter specifying which view to set the value for. If omitted, the value will be set for the default view. @return: None"""
		return self._nukeNode.setValue()
	#----------------------------------------------------------------------
	def value(self):
		"""self.value() -> str  Get the value of this knob as a string. @return: String value."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def getText(self):
		"""self.getText() -> string  Return text associated with knob."""
		return self._nukeNode.getText()

################################################################################
class Pulldown_Knob(Enumeration_Knob):
	#----------------------------------------------------------------------
	def commands(self,n):
		"""commands(n) -> string  Return command n. The argument n is an integer and in the range of 0 and numValues."""
		return self._nukeNode.commands(n)
	#----------------------------------------------------------------------
	def numValues(self):
		"""numValues() -> int  Return number of values."""
		return self._nukeNode.numValues()
	#----------------------------------------------------------------------
	def value(self):
		""""""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def setValues(self,items):
		"""self.setValues(items) -> None. (Re)initialise knob to the list of items. @param items: Dictionary of name/value pairs. @param sort: Optional parameter as to whether to sort the names. @return: None. Example: w = nuke.nodes.NoOp() k = nuke.Pulldown_Knob('kname', 'klabel') k.setValues({'label/command' : 'eval("3*2")'}) w.addKnob(k) k = w['kname']"""
		return self._nukeNode.setValues(items)
	#----------------------------------------------------------------------
	def itemName(self,n):
		"""itemName(n) -> string  Return name of item n. The argument n is an integer and in the range of 0 and numValues."""
		return self._nukeNode.itemName(n)
################################################################################
class Script_Knob(String_Knob):
	#----------------------------------------------------------------------
	def execute(self):
		"""self.execute() -> None Execute the command. @return: None."""
		return self._nukeNode.execute()
	#----------------------------------------------------------------------
	def setValue(self,cmd):
		"""self.setValue(cmd) -> None Set the new command for this knob. @param cmd: String containing a TCL command. @return: None."""
		return self._nukeNode.setValue(cmd)
	#----------------------------------------------------------------------
	def value(self):
		"""self.value() -> str  Get the current command. @return: The current command as a string, or None if there is no current command."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def command(self):
		"""self.command() -> str  Get the current command. @return: The current command as a string, or None if there is no current command."""
		return self._nukeNode.command()
	#----------------------------------------------------------------------
	def setCommand(self,cmd):
		"""self.setCommand(cmd) -> None Set the new command for this knob. @param cmd: String containing a TCL command. @return: None."""
		return self._nukeNode.setCommand(cmd)
################################################################################
class PyCustom_Knob(Script_Knob):
	#----------------------------------------------------------------------
	def getObject(self):
		"""Returns the custom knob object as created in the by the 'command' argument to the PyCuston_Knob constructor."""
		return self._nukeNode.getObject()
################################################################################
class PyScript_Knob(Script_Knob):
	pass
################################################################################
class PythonCustomKnob(Script_Knob):
	#----------------------------------------------------------------------
	def getObject(self):
		"""Returns the custom knob object as created in the by the 'command' argument to the PyCuston_Knob constructor."""
		return self._nukeNode.getObject()
################################################################################
class PythonKnob(String_Knob):
	pass
################################################################################
class Range_Knob(Array_Knob):
	pass

################################################################################
class Scale_Knob(Array_Knob):
	#----------------------------------------------------------------------
	def value(self):
		"""value(n, oc) -> float  Return value for dimension n. The optional argument oc is an OutputContext."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def names(self,n):
		"""names(n) -> string  Return name for dimension n. The argument n is an integer."""
		return self._nukeNode.names(n)
	#----------------------------------------------------------------------
	def y(self,oc):
		"""y(oc) -> float  Return value for y. The optional oc argument is an OutputContext"""
		return self._nukeNode.y(oc)
	#----------------------------------------------------------------------
	def x(self,oc):
		"""x(oc) -> float  Return value for x. The optional oc argument is an OutputContext"""
		return self._nukeNode.x(oc)
	#----------------------------------------------------------------------
	def z(self,oc):
		"""z(oc) -> float  Return value for z. The optional oc argument is an OutputContext"""
		return self._nukeNode.z(oc)
################################################################################
class SceneView_Knob(Unsigned_Knob):
	#----------------------------------------------------------------------
	def getHighlightedItem(self):
		"""self.getHighlightedItem() -> string  Returns a string containing the item which is currently highlighted."""
		return self._nukeNode.getHighlightedItem()
	#----------------------------------------------------------------------
	def setSelectedItems(self):
		"""self.setSelectedItems() -> None  Takes a list of strings of items contained in the knob and sets them as selected."""
		return self._nukeNode.setSelectedItems()
	#----------------------------------------------------------------------
	def setImportedItems(self,items):
		"""self.setImportedItems(items) -> None  Sets a list of strings containing all items imported into the knob. This will overwrite the current imported items list.@param items: List of imported items. @return: None."""
		return self._nukeNode.setImportedItems(items)
	#----------------------------------------------------------------------
	def setAllItems(self):
		"""self.setAllItems(items, autoSelect) -> None  Sets a list of strings containing all items that the knob can import. After calling this function, only items from this list can be imported into the nosde. @param items: List of imported items. @param autoSelect: If True, all items are automatically set as imported and selected. @return: None."""
		return self._nukeNode.setAllItems()
	#----------------------------------------------------------------------
	def removeItems(self):
		"""self.removeItems() -> None  Removes a list of string items from the knob."""
		return self._nukeNode.removeItems()
	#----------------------------------------------------------------------
	def getAllItems(self):
		"""self.getAllItems() -> list  Returns a list of strings containing all items that the knob can import."""
		return self._nukeNode.getAllItems()
	#----------------------------------------------------------------------
	def getImportedItems(self):
		"""self.getImportedItems() -> list  Returns a list of strings containing all items imported into the knob."""
		return self._nukeNode.getImportedItems()
	#----------------------------------------------------------------------
	def getSelectedItems(self):
		"""self.getSelectedItems() -> list  Returns a list of strings containing all currently selected items in the knob."""
		return self._nukeNode.getSelectedItems()
	#----------------------------------------------------------------------
	def addItems(self):
		"""self.addItems() -> None  Adds a list of string items to the knob. New items are automatically set as imported and selected."""
		return self._nukeNode.addItems()
################################################################################
class Tab_Knob(Knob):
	#----------------------------------------------------------------------
	def setValue(self):
		""""""
		return self._nukeNode.setValue()
	#----------------------------------------------------------------------
	def value(self):
		""""""
		return self._nukeNode.value()
################################################################################
class Text_Knob(Knob):
	#----------------------------------------------------------------------
	def value(self):
		""""""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def setValue(self):
		""""""
		return self._nukeNode.setValue()

################################################################################
class Transform2d_Knob(Knob):
	#----------------------------------------------------------------------
	def value(self,oc):
		"""value(oc) -> matrix  Return transformation matrix. The argument oc is an OutputContext. Both arguments are optional."""
		return self._nukeNode.value(oc)
################################################################################
class UV_Knob(Array_Knob):
	#----------------------------------------------------------------------
	def names(self,n):
		"""names(n) -> string  Return name for dimension n. The argument n is an integer."""
		return self._nukeNode.names(n)

################################################################################
class ViewView_Knob(Knob):
	pass
################################################################################
class WH_Knob(Array_Knob):

	#----------------------------------------------------------------------
	def y_at(self):
		"""Return value for Y position at time 't'."""
		return self._nukeNode.y_at()
	#----------------------------------------------------------------------
	def names(self):
		"""Return name for dimension 'i'."""
		return self._nukeNode.names()
	#----------------------------------------------------------------------
	def y(self):
		"""Return value for Y position."""
		return self._nukeNode.y()
	#----------------------------------------------------------------------
	def x(self):
		"""Return value for X position."""
		return self._nukeNode.x()
	#----------------------------------------------------------------------
	def x_at(self):
		"""Return value for X position at time 't'."""
		return self._nukeNode.x_at()

################################################################################
class XYZ_Knob(Array_Knob):

	#----------------------------------------------------------------------
	def parent(self):
		"""parent() -> XYZ_Knob  Return parent."""
		return self._nukeNode.parent()
	#----------------------------------------------------------------------
	def value(self):
		"""value(n, oc) -> float  Return value for dimension n. The optional argument oc is an OutputContext."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def names(self,n):
		"""names(n) -> string  Return name for dimension n. The argument n is an integer."""
		return self._nukeNode.names(n)
	#----------------------------------------------------------------------
	def y(self,oc):
		"""y(oc) -> float  Return value for y. The optional oc argument is an OutputContext"""
		return self._nukeNode.y(oc)
	#----------------------------------------------------------------------
	def x(self,oc):
		"""x(oc) -> float  Return value for x. The optional oc argument is an OutputContext"""
		return self._nukeNode.x(oc)
	#----------------------------------------------------------------------
	def z(self,oc):
		"""z(oc) -> float  Return value for z. The optional oc argument is an OutputContext"""
		return self._nukeNode.z(oc)
################################################################################
class XY_Knob(Array_Knob):
	#----------------------------------------------------------------------
	def value(self):
		"""value(n, oc) -> float  Return value for dimension n. The optional argument oc is an OutputContext."""
		return self._nukeNode.value()
	#----------------------------------------------------------------------
	def names(self,n):
		"""names(n) -> string  Return name for dimension n. The argument n is an integer."""
		return self._nukeNode.names(n)
	#----------------------------------------------------------------------
	def y(self,oc):
		"""y(oc) -> float  Return value for y. The optional oc argument is an OutputContext"""
		return self._nukeNode.y(oc)
	#----------------------------------------------------------------------
	def x(self,oc):
		"""x(oc) -> float  Return value for x. The optional oc argument is an OutputContext"""
		return self._nukeNode.x(oc)