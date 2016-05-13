# Object->Axis building

import nuke, _nukemath

#
# The following is used by PolyText, PolyShape, PolyShards plugins

def versionGreater(major, minor):
	if nuke.NUKE_VERSION_MAJOR == major:
		return nuke.NUKE_VERSION_MINOR >= minor
	return True if nuke.NUKE_VERSION_MAJOR > major else False

def Matrix4( cm ) :
	m = _nukemath.Matrix4()
	for r in xrange(0,4) :
		for c in xrange(0,4) :
			m[r*4 + c] = cm[c*4 + r]
	return m

class AxisPivots :
	def errOut( self, str ) :
		self.len = 0

	def __init__( self, node, offset = 3, inputs = False) :
		n = node.inputs()
		if inputs and n < 4:
			return self.errOut("There must be AxisOp inputs to operate on")

		self.imatrix = Matrix4(node.knob('matrix').getValue()).inverse()
		self.getGeometry = self.nodeGeometry if versionGreater(6,3) else self.getGeometry6

		geo = self.getGeometry(node)
		nobjs = len(geo)
		if nobjs == 0 :
			return self.errOut("There seems to be no objects to operate on")

		self.offset = offset
		self.node = node 
		self.geo = geo
		self.len = nobjs if not inputs else min(n - self.offset, nobjs)

	def parentMatrix( self, node, i ) :
		axis = node.input(i)
		if not axis :
			m = _nukemath.Matrix4()
			m.makeIdentity()
			return m

		return self.parentMatrix(axis, 0) * Matrix4(axis.knob('matrix').getValue())

	def nodeGeometry( self, node, name = 'geo_select' ) :
		k = node.knob(name)
		if not k:
			return self.errOut("Node has no geo knob")
	
		geo = k.getGeometry()
		return geo

	def getGeometry6( self, node ) :
		viewer = nuke.activeViewer()
		if viewer :
			i = viewer.activeInput()
			if type(i) != type(None) :
				vn = viewer.node()
				if vn.inputs()==1 and vn.input(0) == node :
					return self.nodeGeometry(vn, 'geo')

		viewer = nuke.createNode('Viewer') # getattr(nuke.nodes, 'Viewer')()
		for i in xrange(1, viewer.inputs()) :
			viewer.setInput(i, None)
		if viewer.input(0) != node :
			viewer.setInput(0, node)
		rval = self.nodeGeometry(viewer, 'geo')
		nuke.delete(viewer)
		return rval

	def range ( self ) :
		return xrange(0, self.len)

	def input ( self, i ) :
		return self.node.input(i+self.offset)

	def setInput( self, i, op ) :
		self.node.setInput(i+self.offset, op)

	def same( self, a, b ) :
		return a[0] == b[0] and a[1] == b[1] and a[2] == b[2]

	def set( self, i, axis, prev ) :
		xfrm = self.geo[i].transform()
		xfrm = [xfrm[12], xfrm[13], xfrm[14]]
		piv = axis.knob('pivot')
		if prev :
			if not self.same(piv.getValue(), xfrm) :
				trk = axis.knob('translate')
				tr = trk.getValue()
				xfrm = [xfrm[0]-tr[0],xfrm[1]-tr[1], xfrm[2]-tr[2]]
		else :
			axis.knob('display').setValue(0)

		piv.setValue(self.imatrix.transform( _nukemath.Vector3(xfrm[0], xfrm[1], xfrm[2])))

	def clear( self ) :
		for i in xrange(self.len+self.offset, self.node.inputs()):
			self.node.setInput(i, None)

	def setName( self, i, c, name ) :
		c = c.encode('utf8')
		node = self.node.input(i)
		node.knob('label').setValue(c)
		if name :
			try : node.setName(name + c);
			except ValueError: node.setName(name + node.name())
		return node

	def labels( self ) :
		clz = self.node.Class();
		if clz.find('PolyText')!=-1:
			return self.node.knob('message').value().decode('utf8')
		elif clz.find('PolyShape')!=-1:
			import roto
			return roto.RotoEvaluate(self.node.input(0), roto.Names()).parse(0)

	def ui( self, name = None, stepx = 60, stepy = 80 ) :
		if type(name) == type(None): name = self.node.name()+'_'
		n = self.node.inputs()
		msg = self.labels()
		ns = 0
		if stepx != 0 or stepy != 0 :
			maxrun = 0
			start = 0
			startx = self.node.xpos() - (stepx * (n-self.offset))
			y = self.node.ypos()
			x = startx
			for i in xrange(self.offset, n) :
				if msg:
					while msg[i-self.offset+ns].isspace() :
						c = i-self.offset+ns
						if ( msg[c] == '\n' ) :
							y = y + stepy
							maxrun = max(maxrun, c-start)
							start = c+1
							x = startx
						ns = ns + 1
					node = self.setName(i, msg[i-self.offset+ns], name)
				else:
					node = self.node.input(i)
				node.setXpos(x)
				node.setYpos(y)
				x += stepx
			maxrun = max(maxrun, n-start)
			if maxrun != n :
				dx = startx - (self.node.xpos() - (stepx * maxrun))
				for i in xrange(self.offset, n) :
					node = self.node.input(i)
					node.setXpos(node.xpos()-dx)
		elif msg :
			for i in xrange(self.offset, n) :
				while msg[i-self.offset+ns].isspace() : ns = ns + 1;
				self.setName(i, msg[i-self.offset], name).autoplace()


