try:
	import nuke
except ImportError:
	nuke = None

import operator, random
from Nuke_Scripts.NodeFns.creating import create_Node
from Nuke_Scripts.NodeCls.Vec2 import Vector2
from Nuke_Scripts.NodeCls.Node_List import Node_List
from Nuke_Scripts import NukeNodes

def Make_backdrop(name,x,y,w,h,grp=None):
	"""Create A BakedropNode At pos x,y with width and height set to w,h of the backdrop exists it is then set to the given inputs"""
	if grp==None:
		grp = nuke.thisGroup()
	with grp:
		if not nuke.exists(name):
			bd = create_Node(nuke.nodes.BackdropNode,name=name)
			bd.setXYpos(x,y)
			bd["bdwidth"].setValue(w)
			bd["bdheight"].setValue(h)
		else:
			bd = create_Node(nuke.nodes.BackdropNode,name=name)
	return bd

def make_nodes_offset_dict(bd):
	res = {}
	nodes = backdrop_contents(bd)
	for n in nodes:
		res[n]=get_node_backdrop_offset(bd,n)
	return res

def make_Offset_backdrop_dict(backdrops=None,grp=None):
	res = {}
	if gro==None:
		grp = nuke.thisGroup()

	if backdrops==None:
		with grp:
			backdrops = nuke.allNodes("BackdropNode")

	for bd in backdrops:
		res[bd]=make_nodes_offset_dict(bd)

	return res

def Offset_backdrop(bd,xoffset=0,yoffset=0):
	x = bd.xpos()+xoffset
	y = bd.ypos()+yoffset
	bd.setXYpos(x,y)

def get_backdrop_Bottom_Left(bd):
	bd_wh = Vector2(bd["bdwidth"].value(),bd["bdheight"].value())
	bd_xy = Vector2(bd.xpos(),bd.ypos())
	bd_wpos = Vector2(bd_xy.x,bd_xy.y+bd_wh.y)
	return bd_wpos

def get_backdrop_Bottom_Right(bd):
	bd_wh = Vector2(bd["bdwidth"].value(),bd["bdheight"].value())
	bd_xy = Vector2(bd.xpos(),bd.ypos())
	bd_wpos = Vector2(bd_xy.x+bd_wh.x,bd_xy.y+bd_wh.y)
	return bd_wpos

def extend_backdrop_Right(bd,value):
	bd["bdwidth"].setValue(bd["bdwidth"].value()+value)

def extend_backdrop_Down(bd,value):
	bd["bdheight"].setValue(bd["bdheight"].value()+value)

def extend_backdrop_Left(bd,value):
	old = get_backdrop_Top_Left(bd)
	bd.setXpos(bd.xpos() - value)
	new = get_backdrop_Top_Left(bd)
	dif = new.distanceBetween(old)
	extend_backdrop_Right(bd, dif)

def extend_backdrop_Up(bd,value):
	old = get_backdrop_Bottom_Right(bd)
	bd.setYpos(bd.ypos() - value)
	new = get_backdrop_Bottom_Right(bd)
	dif = new.distanceBetween(old)
	extend_backdrop_Down(bd, dif)

def get_backdrop_Top_Left(bd):
	bd_xy = Vector2(bd.xpos(),bd.ypos())
	return bd_xy

def get_backdrop_Top_Right(bd):
	bd_wh = Vector2(bd["bdwidth"].value(),bd["bdheight"].value())
	bd_xy = Vector2(bd.xpos(),bd.ypos())
	bd_wpos = Vector2(bd_xy.x+bd_wh.x,bd_xy.y)
	return bd_wpos

def get_backdrop_Center(bd):
	bd_wh = Vector2(bd["bdwidth"].value(),bd["bdheight"].value())
	bd_xy = Vector2(bd.xpos()+(bd_wh.x/2),bd.ypos()+(bd_wh.y/2))
	return bd_xy

def get_backdrop_BBox(bd):
	bd_wh = Vector2(bd["bdwidth"].value(),bd["bdheight"].value())
	bd_xy = Vector2(bd.xpos(),bd.ypos())
	bd_wh = bd_xy + bd_wh

	return Box(x=bd_xy.x, y=bd_wh.y, r=bd_wh.x, t=bd_xy.y)

def apply_Offset_node_dict(bd,data):
	v1 = Vector2(bd.xpos(),bd.ypos())
	for n,v in list(data.items()):
		v = v1 + v
		n.setXYpos(v.x,v.y)

def apply_Offset_Backdrops_dict(data):
	for bd,node_data in list(data.items()):
		apply_Offset_node_dict(bd, node_data)

def get_node_backdrop_offset(bd,n):
	bdXvec = Vector2(bd.xpos(),0)
	nXvec  = Vector2(n.xpos(),0)

	bdYvec = Vector2(bd.ypos(),0)
	nYvec = Vector2(n.ypos(),0)

	x = bdXvec.distanceBetween(nXvec)
	y = bdYvec.distanceBetween(nYvec)

	offset = Vector2(x,y)
	return offset

def backdrop_contents(backdropNode=None):
	'''
	Returns all the nodes contained in backdropNode input or all selected Backdrop nodes.
	'''
	bdNodes = []
	bdRanges = []
	if not backdropNode is None and isinstance(backdropNode,nuke.Node):
		if backdropNode.Class() == "BackdropNode":
			bdNodes.append(backdropNode)
	if not len(bdNodes):
		if not nuke.selectedNodes("BackdropNode"):
			return
		bdNodes = nuke.selectedNodes("BackdropNode")
	for bd in bdNodes:
		left = bd.xpos()
		top = bd.ypos()
		right = left + bd['bdwidth'].value()
		bottom = top + bd['bdheight'].value()
		bdRanges.append((left, right, top, bottom))
	inNodes = []
	for node in nuke.allNodes():
		if node.Class() == "Viewer":
			continue
		for r in bdRanges:
			if node.xpos() > r[0] and node.xpos() + node.screenWidth() < r[1] and node.ypos() > r[2] and node.ypos() + node.screenHeight() < r[3]:
				inNodes.append(node)
				break
	return inNodes

def randomGray(Min = .1, Max = .3):
	'''
	return a random darkish gray as hex code to assign to tile and gl colours
	'''
	v = random.random() * Min + (Max-Min)
	return int('%02x%02x%02x%02x' % (v*255,v*255,v*255,v*255),16)

def simple_backdrop():
	selNodes = nuke.selectedNodes()
	if not selNodes:
		return nuke.nodes.BackdropNode()

	# find min and max of positions
	positions = [(i.xpos(), i.ypos()) for i in selNodes]
	xPos = sorted(positions, key = operator.itemgetter(0))
	yPos = sorted(positions, key = operator.itemgetter(1))
	xMinMaxPos = (xPos[0][0], xPos[-1:][0][0])
	yMinMaxPos = (yPos[0][1], yPos[-1:][0][1])

	n = nuke.nodes.BackdropNode(xpos = xMinMaxPos[0]-60, bdwidth = xMinMaxPos[1]-xMinMaxPos[0]+200,
		                        ypos = yMinMaxPos[0]-85,
		                        bdheight = yMinMaxPos[1]-yMinMaxPos[0]+160,
		                        note_font_size = 42)
	n['selected'].setValue(False)

	# revert to previous selection
	for i in selNodes:
		i['selected'].setValue(True)

	return n

def auto_backdrop(selNodes,**kwargs):

	# Calculate bounds for the backdrop node.
	bdX = min([node.xpos() for node in selNodes])
	bdY = min([node.ypos() for node in selNodes])
	bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
	bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY

	# Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
	left = kwargs.pop("left",-10)
	top = kwargs.pop("top",-50)
	right = kwargs.pop("right",10)
	bottom = kwargs.pop("bottom",10)

	bdX += left
	bdY += top
	bdW += (right - left)
	bdH += (bottom - top)
	kwargs["xpos"]=bdX
	kwargs["ypos"]=bdY
	kwargs["bdwidth"]=bdW
	kwargs["bdheight"]=bdH
	kwargs["note_font_size"]=kwargs.get("note_font_size",50)
	n = create_Node(nuke.nodes.BackdropNode,**kwargs)

	return n


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

class BackdropNode(NukeNodes.BackdropNode):

	def __init__(self,obj, x=0, y=0, w=500, h=500, grp=None):
		if isinstance(obj,str):
			self._nukeNode  = Make_backdrop(obj, x, y, w, h, grp)
		elif isinstance(obj,nuke.Node) and obj.Class() == "BackdropNode":
			self._nukeNode  = obj

		self.make_nodelist()
		self.make_backdrop_BBox()
		self.make_nodes_offset_dict()

	def x():
		def fget(self):return self._nukeNode.xpos()
		def fset(self,val): self._nukeNode.setXpos(val)
		return locals()
	x = property(**x())
	def y():
		def fget(self): return self._nukeNode.xpos()
		def fset(self,val): self._nukeNode.setYpos(val)
		return locals()
	y = property(**y())
	def xy():
		def fget(self): return Vector2(self.x,self.y)
		def fset(self,val): self._nukeNode.setXYpos(val.x,val.y)
		return locals()
	xy = property(**xy())

	def update_box(self):
		self._box.set(int(self.L), int(self.B), int(self.R), int(self.T))

	def update_backdrop(self):
		self.make_nodelist()
		self.update_box()
		self.make_nodes_offset_dict()

	@property
	def nodes(self):
		return self._nodes

	def make_nodelist(self):
		self._nodes = Node_List(backdrop_contents(self._nukeNode))

	def make_backdrop_BBox(self):
		self._box = get_backdrop_BBox(self._nukeNode)

	def make_nodes_offset_dict(self):
		self._nodes_dict = make_nodes_offset_dict(self._nukeNode)

	@property
	def nodes_offset_dict(self):
		return self._nodes_dict

	def rebuild_offset_dict(self):
		self._nodes_dict = self.make_nodes_offset_dict()

	def apply_node_Offset(self):
		return apply_Offset_node_dict(self._nukeNode, self._nodes_dict)

	@property
	def center(self):
		return Vector2(self._box.centerX,self._box.centerY)

	def get_Top_Left(self):
		return get_backdrop_Top_Left(self._nukeNode)

	def get_Bottom_Left(self):
		return get_backdrop_Bottom_Left(self._nukeNode)

	def get_Top_Right(self):
		return get_backdrop_Top_Right(self._nukeNode)

	def get_Bottom_Right(self):
		return get_backdrop_Bottom_Right(self._nukeNode)

	def set_Top_Left(self,x,y):
		extend_backdrop_Left(self._nukeNode, x)
		extend_backdrop_Up(self._nukeNode, y)
		self._update_box()

	def set_Top_Right(self,x,y):
		# Get The Current pos
		current = self.get_Top_Right()
		vec1 = Vector2(y,0)
		vec2 = Vector2(y,0)
		yd = vec1.distanceBetween(vec2)

		old_x = self._nukeNode.xpos()
		vec1 = Vector2(old_x,0)
		self._nukeNode.setXpos(x)
		vec2 = Vector2(self._nukeNode.xpos(),0)
		xd = vec1.distanceBetween(vec2)

		offset = Vector2(xd,yd)

		if y > old_L:
			self._nukeNode["bdwidth"].setValue(self._nukeNode["bdwidth"].value() + offset.y)
		else:
			self._nukeNode["bdwidth"].setValue(self._nukeNode["bdwidth"].value()+ (offset.y * -1))

		if x > self.R:
			self._nukeNode["bdheight"].setValue(self._nukeNode["bdheight"].value()+offset.x)
		else:
			self._nukeNode["bdheight"].setValue(self._nukeNode["bdheight"].value()+ (offset.x * -1))
		self._update_box()

	def set_Bottom_Left(self,x,y):
		old_L = self.L
		vec1 = Vector2(self.L,0)
		self._nukeNode.setXpos(x)
		vec2 = Vector2(self.L,0)
		xd = vec1.distanceBetween(vec2)
		vec1 = Vector2(self.B,0)
		vec2 = Vector2(y,0)
		yd = vec1.distanceBetween(vec2)
		offset = Vector2(xd,yd)

		if x < old_L:
			self._nukeNode["bdwidth"].setValue(self._nukeNode["bdwidth"].value() + offset.x)
		else:
			self._nukeNode["bdwidth"].setValue(self._nukeNode["bdwidth"].value()+ (offset.x * -1))

		if y > self.B:
			self._nukeNode["bdheight"].setValue(self._nukeNode["bdheight"].value()+offset.y)
		else:
			self._nukeNode["bdheight"].setValue(self._nukeNode["bdheight"].value()+ (offset.y * -1))
		self._update_box()

	def set_Bottom_Right(self,x,y):
		vec1 = Vector2(self.R,0)
		vec2 = Vector2(x,0)
		xd = vec1.distanceBetween(vec2)
		vec1 = Vector2(self.B,0)
		vec2 = Vector2(y,0)
		yd = vec1.distanceBetween(vec2)
		offset = Vector2(xd,yd)

		if x > self.R:
			self._nukeNode["bdwidth"].setValue(self._nukeNode["bdwidth"].value()+offset.x)
		else:
			self._nukeNode["bdwidth"].setValue(self._nukeNode["bdwidth"].value()+ (offset.x * -1))

		if y > self.B:
			self._nukeNode["bdheight"].setValue(self._nukeNode["bdheight"].value()+offset.y)
		else:
			self._nukeNode["bdheight"].setValue(self._nukeNode["bdheight"].value()+ (offset.y * -1))
		self._update_box()

	def extend_Left(self,val):
		extend_backdrop_Left(self._nukeNode, val)
		self._update_box()

	def extend_Right(self,val):
		extend_backdrop_Right(self._nukeNode, val)
		self._update_box()

	def extend_Up(self,val):
		extend_backdrop_Up(self._nukeNode, val)
		self._update_box()

	def extend_Down(self,val):
		extend_backdrop_Down(self._nukeNode, val)
		self._update_box()

	def Offset(self,x=0,y=0):
		Offset_backdrop(self._nukeNode,x,y)
		self._update_box()

	@property
	def L(self):
		return self._nukeNode.xpos()
	@property
	def T(self):
		return self._nukeNode.ypos()
	@property
	def R(self):
		return self.get_Bottom_Right().x
	@property
	def B(self):
		return self.get_Bottom_Right().y