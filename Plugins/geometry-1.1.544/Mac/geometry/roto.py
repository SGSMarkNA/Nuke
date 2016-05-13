# Evaluate rotoshapes

import nuke, _nukemath

class Points :
	SHAPE_BEGIN = 6
	if nuke.NUKE_VERSION_MAJOR >= 7:
		@staticmethod
		def convertType(type) :
			if (type>=4 and type<=5) or (type >=7 and type <= 9): # bezier/shapes
				return 0
			elif type==6:     # b-spline
				return 1
			elif type == 14 : # paint
				return 2
			return -1
	else:
		@staticmethod
		def convertType(type) :
			if type==4 or (type >=6 and type <= 7): # bezier/shapes
				return 0
			elif type==5:     # b-spline, broken until 6.2
				return 1
			elif type == 14 : # paint
				return 2
			reutrn -1

	def __init__( self ) :
		# Different versions of Nuke have different versions of Python
		self.sixtwo = True if nuke.NUKE_VERSION_MAJOR > 6 or (nuke.NUKE_VERSION_MAJOR ==6 and nuke.NUKE_VERSION_MINOR >= 2) else False
		self.strmat = self.strtr if self.sixtwo else self.strrp

	def add( self, cp, pts ) :
		pts.append(cp.x)   
		pts.append(cp.y)

	def strrp( self, obj, frame ) :
		return str(obj.getTransform().evaluate(frame).getMatrix()).replace('{','').replace('}','')

	def strtr( self, obj, frame ) :
		return str(obj.getTransform().evaluate(frame).getMatrix()).translate(None, '{}[]')

	def __call__( self, obj, frame, bs, idx ) :
		pts = []
		type = Points.convertType( obj.getAttributes().getValue(frame, 'tt') )
		if type == 0:	 # bezier/shapes
			for cp in obj :
				self.add(cp.center.getPosition(frame), pts)
				self.add(cp.leftTangent.getPosition(frame), pts)
				self.add(cp.rightTangent.getPosition(frame), pts)
		elif type==1:  # b-spline, broken until 6.2
			if not self.sixtwo :
				return pts
			for cp in obj :
				self.add(cp.center.getPosition(frame), pts)
		elif type == 2 : # paint
			for cp in obj :
				self.add(cp.getPosition(frame), pts)				
		else :
			return

		pts.extend(eval('['+self.strmat(obj, frame)+']'))
		attr = obj.getAttributes().getValue(frame, 'bm')
		pts.append( 1 if attr == 12 else 0 )
		pts.append( type )
		pts.append(idx)
		return pts

class Names :
	def __call__( self, obj, frame, bs, idx ) :
		return obj.name

try:
	if nuke.NUKE_VERSION_MAJOR >= 7:
		import _curveknob as layers
	else:
		import _rotopaint as layers

	class RotoEvaluate :	
		def __init__( self, node, evaluate = None ) :
			self.node = node
			self.evaluate = evaluate if evaluate else Points()
	
		def layers( self, layer, frame, idx = 0 ) :
			curves = []
			for obj in layer :
				if obj.getVisible(frame) :
					tp = type(obj)
					if tp == layers.Layer :
						curves.extend(self.layers(obj, frame, idx+1))
					elif tp == layers.Shape:
						curves.append(self.evaluate(obj, frame, 1, idx))
					elif tp == layers.Stroke:
						curves.append(self.evaluate(obj, frame, 0, idx))
			#curves[0].extend(curves[1])
			#return [ curves[0] ]
			return curves
	
		def parse( self, frame = 0 ) :
			if self.node :
				crvs = self.node.knob('curves')
				if crvs :
					return self.layers(crvs.rootLayer, frame)

except ImportError:
	pass
