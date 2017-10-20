import nuke
class Node(nuke.Node):

	def __new__(cls,typ,options=""):
		opts = options.split()
		if "name" in opts:
			val = opts[opts.index("name")+1]
			if nuke.exists(val):
				n = nuke.toNode(val)
				return n
		return nuke.createNode(typ,options,False)

	@property
	def getNumKnobs(self):
		"""self.numKnobs() -> The number of knobs. @return: The number of knobs."""
		return super(Node).getNumKnobs()
	
	@property
	def Autoplace(self):
		"""self.autoplace() -> None. Automatically place nodes, so they do not overlap. @return: None."""
		return self.autoplace()

	@property
	def forceValidate(self):
		"""self.forceValidate() -> None  Force the node to validate itself, updating its hash."""
		return super(Node).forceValidate()

	@property
	def help(self):
		"""self.help() -> str @return: Help for the node."""
		return super(Node).help()

	@property
	def lastFrame(self):
		"""self.lastFrame() -> int. Last frame in frame range for this node. @return: int."""
		return super(Node).lastFrame()

	@property
	def treeHasError(self):
		"""treeHasError() -> bool True if the node or any in its input tree have an error, or False otherwise.  Error state of the node and its input tree. Note that this will always return false for viewers, which cannot generate their input trees.  Instead, choose an input of the viewer (e.g. the active one), and call treeHasError() on that."""
		return super(Node).treeHasError()

	@property
	def maximumInputs(self):
		"""self.maximumInputs() -> Maximum number of inputs this node can have. @return: Maximum number of inputs this node can have."""
		return super(Node).maximumInputs()

	@property
	def hasError(self):
		"""hasError() -> bool True if the node itself has an error, regardless of the state of the ops in its input tree, or False otherwise.  Error state of the node itself, regardless of the state of the ops in its input tree. Note that an error on a node may not appear if there is an error somewhere in its input tree, because it may not be possible to validate the node itself correctly in that case."""
		return super(Node).hasError()

	@property
	def height(self):
		"""self.height() -> int. Height of the node. @return: int."""
		return super(Node).height()

	@property
	def maximumOutputs(self):
		"""self.maximumOutputs() -> Maximum number of outputs this node can have. @return: Maximum number of outputs this node can have."""
		return super(Node).maximumOutputs()

	@property
	def screenWidth(self):
		"""self.screenWidth() -> int. Width of the node when displayed on screen in the DAG, at 1:1 zoom, in pixels. @return: int."""
		return super(Node).screenWidth()

	@property
	def minimumInputs(self):
		"""self.minimumInputs() -> Minimum number of inputs this node can have. @return: Minimum number of inputs this node can have."""
		return super(Node).minimumInputs()

	@property
	def firstFrame(self):
		"""self.firstFrame() -> int. First frame in frame range for this node. @return: int."""
		return super(Node).firstFrame()

	@property
	def shown(self):
		"""self.shown() -> true if the properties panel is open. This can be used to skip updates that are not visible to the user. @return: true if the properties panel is open. This can be used to skip updates that are not visible to the user."""
		return super(Node).shown()

	@property
	def numKnobs(self):
		"""self.numKnobs() -> The number of knobs. @return: The number of knobs."""
		return super(Node).numKnobs()

	@property
	def maxInputs(self):
		"""self.maximumInputs() -> Maximum number of inputs this node can have. @return: Maximum number of inputs this node can have."""
		return super(Node).maxInputs()

	@property
	def isSelected(self):
		"""self.isSelected() -> bool  Returns the current selection state of the node.  This is the same as checking the 'selected' knob. @return: True if selected, or False if not."""
		return super(Node).isSelected()

	@property
	def opHashes(self):
		"""self.opHashes() -> list of int  Returns a list of hash values, one for each op in this node."""
		return super(Node).opHashes()

	@property
	def width(self):
		"""self.width() -> int. Width of the node. @return: int."""
		return super(Node).width()

	@property
	def allKnobs(self):
		"""self.knobs() -> dict  Get a dictionary of (name, knob) pairs for all knobs in this node.  For example:     >>> b = nuke.nodes.Blur()    >>> b.knobs()  @return: Dictionary of all knobs."""
		return super(Node).allKnobs()

	@property
	def knobs(self):
		"""self.knobs() -> dict  Get a dictionary of (name, knob) pairs for all knobs in this node.  For example:     >>> b = nuke.nodes.Blur()    >>> b.knobs()  @return: Dictionary of all knobs."""
		return super(Node).knobs()

	@property
	def Class(self):
		"""self.Class() -> Class of node. @return: Class of node."""
		return super(Node).Class()

	@property
	def maxOutputs(self):
		"""self.maximumOutputs() -> Maximum number of outputs this node can have. @return: Maximum number of outputs this node can have."""
		return super(Node).maxOutputs()

	@property
	def inputs(self):
		"""self.inputs() -> Number of inputs. @return: Number of inputs."""
		return super(Node).inputs()

	def xpos(self):
		"""self.xpos() -> X position of node in node graph. @return: X position of node in node graph."""
		return super(Node).xpos()

	def ypos(self):
		"""self.ypos() -> Y position of node in node graph. @return: Y position of node in node graph."""
		return super(Node).ypos()

	def setXpos(self,x):
		"""self.setXpos(x) -> None. Set the x position of node in node graph. @param x: The x position of node in node graph. @return: None."""
		return super(Node).setXpos(x)

	def setYpos(self,y):
		"""self.setYpos(y) -> None. Set the y position of node in node graph. @param y: The y position of node in node graph. @return: None."""
		return super(Node).setYpos(y)

	x = property(xpos,setXpos)
	y = property(ypos,setYpos)

	@property
	def format(self):
		"""self.format() -> Format. Format of the node. @return: Format."""
		return super(Node).format()

	@property
	def running(self):
		"""self.running() -> Node rendering when paralled threads are running or None. Class method. @return: Node rendering when paralled threads are running or None."""
		return super(Node).running()

	@property
	def pixelAspect(self):
		"""self.pixelAspect() -> int. Pixel Aspect ratio of the node. @return: float."""
		return super(Node).pixelAspect()

	@property
	def proxy(self):
		"""self.proxy() -> bool @return: True if proxy is enabled, False otherwise."""
		return super(Node).proxy()

	@property
	def clones(self):
		"""self.clones() -> Number of clones. @return: Number of clones."""
		return super(Node).clones()

	@property
	def fullName(self):
		"""self.fullName() -> str Get the name of this node and any groups enclosing it in 'group.group.name' form. @return: The fully-qualified name of this node, as a string."""
		return super(Node).fullName()

	@property
	def resetKnobsToDefault(self):
		"""self.resetKnobsToDefault() -> None  Reset all the knobs to their default values."""
		return super(Node).resetKnobsToDefault()

	@property
	def channels(self):
		"""self.channels() -> String list. List channels output by this node. @return: String list."""
		return super(Node).channels()

	@property
	def name(self):
		"""self.name() -> str @return: Name of node."""
		return super(Node).name()

	@property
	def minInputs(self):
		"""self.minimumInputs() -> Minimum number of inputs this node can have. @return: Minimum number of inputs this node can have."""
		return super(Node).minInputs()

	@property
	def hideControlPanel(self):
		"""self.hideControlPanel() -> None @return: None"""
		return super(Node).hideControlPanel()

	@property
	def optionalInput(self):
		"""self.optionalInput() -> Number of first optional input. @return: Number of first optional input."""
		return super(Node).optionalInput()

	@property
	def screenHeight(self):
		"""self.screenHeight() -> int. Height of the node when displayed on screen in the DAG, at 1:1 zoom, in pixels. @return: int."""
		return super(Node).screenHeight()

	@property
	def frameRange(self):
		"""self.frameRange() -> FrameRange. Frame range for this node. @return: FrameRange."""
		return super(Node).frameRange()

	@property
	def error(self):
		"""error() -> bool True if the node or any in its input tree have an error, or False otherwise.  Error state of the node and its input tree.  Deprecated; use hasError or treeHasError instead. Note that this will always return false for viewers, which cannot generate their input trees.  Instead, choose an input of the viewer (e.g. the active one), and call treeHasError() on that."""
		return super(Node).error()

	@property
	def redraw(self):
		"""self.redraw() -> None. Force a redraw of the node. @return: None."""
		return super(Node).redraw()

	@property
	def bbox(self):
		"""self.bbox() -> List of x, y, w, h. Bounding box of the node. @return: List of x, y, w, h."""
		return super(Node).bbox()

	#def addKnob(self,k):
	#    """self.addKnob(k) -> None. Add knob k to this node or panel. @param k: Knob. @return: None."""
	#    return self._node.addKnob(k)

	#def metadata(self,*args,**kwargs):
		#"""self.metadata(key, time, view) -> value or dict Return the metadata item for key on this node at current output context, or at optional time and view. If key is not specified a dictionary containing all key/value pairs is returned. None is returned if key does not exist on this node. @param key: Optional name of the metadata key to retrieve. @param time: Optional time to evaluate at (default is taken from node's current output context). @param view: Optional view to evaluate at (default is taken from node's current output context). @return: The requested metadata value, a dictionary containing all keys if a key name is not provided, or None if the specified key is not matched."""
		#return super(Node).bbox()
		#return self._node.metadata(*args,**kwargs)
	#def knob(self,p):
	#    """self.knob(p) -> The knob named p or the pth knob. @param p: A string or an integer. @return: The knob named p or the pth knob."""
	#    return self._node.knob(p)
	#
	#def readKnobs(self,s):
	#    """self.readKnobs(s) -> None. Read the knobs from a string (TCL syntax). @param s: A string. @return: None."""
	#    return self._node.readKnobs(s)
	#
	#
	#def writeKnobs(self,i):
	#    """self.writeKnobs(i) -> String in .nk form. Return a tcl list. If TO_SCRIPT | TO_VALUE is not on, this is a simple list of knob names. If it is on, it is an alternating list of knob names and the output of to_script().  Flags can be any of these or'd together: - nuke.TO_SCRIPT produces to_script(0) values - nuke.TO_VALUE produces to_script(context) values - nuke.WRITE_NON_DEFAULT_ONLY skips knobs with not_default() false - nuke.WRITE_USER_KNOB_DEFS writes addUserKnob commands for user knobs - nuke.WRITE_ALL writes normally invisible knobs like name, xpos, ypos  @param i: The set of flags or'd together. Default is TO_SCRIPT | TO_VALUE. @return: String in .nk form."""
	#    return self._node.writeKnobs(i)
	#
	#def setSelected(self,selected):
	#    """self.setSelected(selected) -> None. Set the selection state of the node.  This is the same as changing the 'selected' knob. @param selected: New selection state - True or False. @return: None."""
	#    return self._node.setSelected(selected)
	#
	#
	#def showControlPanel(self):
	#    """self.showControlPanel(forceFloat = false) -> None @param forceFloat: Optional python object. If it evaluates to True the control panel will always open as a floating panel. Default is False. @return: None"""
	#    return self._node.showControlPanel()
	#
	#def showInfo(self,s):
	#    """self.showInfo(s) -> None. Creates a dialog box showing the result of script s. @param s: A string. @return: None."""
	#    return self._node.showInfo(s)
	#
	#def dependent(self,what):
	#    """self.dependent(what) -> List of nodes.  List all nodes that read information from this node.  'what' is an optional integer (see below). You can use any combination of the following constants or'ed together to select what types of dependent nodes to look for: 	 nuke.EXPRESSIONS = expressions 	 nuke.INPUTS = visible input pipes 	 nuke.HIDDEN_INPUTS = hidden input pipes. The default is to look for all types of connections.  Example: nuke.toNode('Blur1').dependent( nuke.INPUTS | nuke.EXPRESSIONS ) @param what: Or'ed constant of nuke.EXPRESSIONS, nuke.INPUTS and nuke.HIDDEN_INPUTS to select the types of dependent nodes. The default is to look for all types of connections. @return: List of nodes."""
	#    return self._node.dependent(what)
	#
	#def setXYpos(self):
	#    """self.setXYpos(x, y) -> None. Set the (x, y) position of node in node graph. @param x: The x position of node in node graph. @param y: The y position of node in node graph. @return: None."""
	#    return self._node.setXYpos()
	#
	#def setName(self):
	#    """self.setName(name, uncollide=True) -> None Set name of the node and resolve name collisions if optional named argument 'uncollide' is True. @param name: A string. @param uncollide: Optional boolean to resolve name collisions. Defaults to True. @return: None"""
	#    return self._node.setName()
	#
	#def deepSampleCount(self):
	#    """self.deepSampleCount(x, y) -> Integer value. Return number of samples for a pixel on a deep image. This requires the image to be calculated, so performance may be very bad if this is placed into an expression in a control panel. @param x: Position to sample (X coordinate). @param y: Position to sample (Y coordinate). @return: Integer value."""
	#    return self._node.deepSampleCount()
	#
	#def removeKnob(self,k):
	#    """self.removeKnob(k) -> None. Remove knob k from this node or panel. Throws a ValueError exception if k is not found on the node. @param k: Knob. @return: None."""
	#    return self._node.removeKnob(k)
	#
	#def input(self,i):
	#    """self.input(i) -> The i'th input. @param i: Input number. @return: The i'th input."""
	#    return self._node.input(i)
	#
	#def sample(self):
	#    """self.sample(c, x, y, dx, dy) -> Floating point value. Return pixel values from an image. This requires the image to be calculated, so performance may be very bad if this is placed into an expression in a control panel. Produces a cubic filtered result. Any sizes less than 1, including 0, produce the same filtered result, this is correct based on sampling theory. Note that integers are at the corners of pixels, to center on a pixel add .5 to both coordinates. If the optional dx,dy are not given then the exact value of the square pixel that x,y lands in is returned. This is also called 'impulse filtering'. @param c: Channel name. @param x: Centre of the area to sample (X coordinate). @param y: Centre of the area to sample (Y coordinate). @param dx: Optional size of the area to sample (X coordinate). @param dy: Optional size of the area to sample (Y coordinate). @return: Floating point value."""
	#    return self._node.sample()
	#
	#def setInput(self):
	#    """self.setInput(i, node) -> bool Connect input i to node if canSetInput() returns true. @param i: Input number. @param node: The node to connect to input i. @return: True if canSetInput() returns true, or if the input is already correct."""
	#    return self._node.setInput()
	#
	#def dependencies(self,what):
	#    """self.dependencies(what) -> List of nodes.  List all nodes referred to by this node. 'what' is an optional integer (see below). You can use the following constants or'ed together to select what types of dependencies are looked for: 	 nuke.EXPRESSIONS = expressions 	 nuke.INPUTS = visible input pipes 	 nuke.HIDDEN_INPUTS = hidden input pipes. The default is to look for all types of connections.  Example: nuke.toNode('Blur1').dependencies( nuke.INPUTS | nuke.EXPRESSIONS ) @param what: Or'ed constant of nuke.EXPRESSIONS, nuke.INPUTS and nuke.HIDDEN_INPUTS to select the types of dependencies. The default is to look for all types of connections. @return: List of nodes."""
	#    return self._node.dependencies(what)
	#
	#def canSetInput(self):
	#    """self.canSetInput(i, node) -> bool Check whether the output of 'node' can be connected to input i.  @param i: Input number. @param node: The node to be connected to input i. @return: True if node can be connected, False otherwise."""
	#    return self._node.canSetInput()
	#
	#def deepSample(self):
	#    """self.deepSample(c, x, y, n) -> Floating point value. Return pixel values from a deep image. This requires the image to be calculated, so performance may be very bad if this is placed into an expression in a control panel. @param c: Channel name. @param x: Position to sample (X coordinate). @param y: Position to sample (Y coordinate). @param n: Sample index (between 0 and the number returned by deepSampleCount() for this pixel, or -1 for the frontmost). @return: Floating point value."""
	#    return self._node.deepSample()
	#
	#def linkableKnobs(self,knobType):
	#    """self.linkableKnobs(knobType) -> List  Returns a list of any knobs that may be linked to from the node as well as some meta information about the knob. This may include whether the knob is enabled and whether it should be used for absolute or relative values. Not all of these variables may make sense for all knobs.. @param knobType A KnobType describing the type of knobs you want.@return: A list of LinkableKnobInfo that may be empty ."""
	#    return self._node.linkableKnobs(knobType)
	#

	#def connectInput(self):
	#    """self.connectInput(i, node) -> bool Connect the output of 'node' to the i'th input or the next available unconnected input. The requested input is tried first, but if it is already set then subsequent inputs are tried until an unconnected one is found, as when you drop a connection arrow onto a node in the GUI. @param i: Input number to try first. @param node: The node to connect to input i. @return: True if a connection is made, False otherwise."""
	#    return self._node.connectInput()

