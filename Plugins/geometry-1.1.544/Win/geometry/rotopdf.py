# Create roto shapes from a pdf file's shapes
# text is currently ignored

import nuke
import nuke.rotopaint as rotopaint
from _nukemath import Vector3, Matrix4

if nuke.NUKE_VERSION_MAJOR >= 7:
	from _curveknob import Shape, Layer, ShapeControlPoint
else:
	from _rotopaint import Shape, Layer, ShapeControlPoint
		
from PyPDF2 import pdf

def Matrix2(a=1,b=0,c=0,d=1,e=0,f=0) :
	m = Matrix4()
	m[0] = float(a)
	m[1] = float(b)
	m[2] = 0
	m[3] = 0
	m[4] = float(c)
	m[5] = float(d)
	m[6] = 0
	m[7] = 0
	m[8] = 0
	m[9]  = 0
	m[10] = 1
	m[11] = 0
	m[12] = float(e)
	m[13] = float(f)
	m[14] = 0
	m[15] = 1
	return m

def coypMatrix2(m):
	return Matrix4(m)
	
def operandToVectors( operands ) :
	rval = []
	while len(operands):
		y, x = float(operands.pop()), float(operands.pop())
		rval.insert( 0, Vector3(x, y,0) )
	return rval

class State():
	def __init__(self):
		self.path = -1
		self.zero = Vector3(0,0,0)
		self.xform = Matrix2()
		self.xforms = [Matrix2()]
		self.reset()

	def save(self):
		self.xforms.append( coypMatrix2(self.xform) )
		self.xform = Matrix2()

	def reset(self):
		self.pos = Vector3(0,0,0)
		self.tanIn, self.closed, self.skip = None, False, False
		self.strokeColor, self.fillColor, self.fill = None, None, False
		self.path = self.path+1

	def setStroke(self,c):
		self.strokeColor = c

	def setFill(self,c):
		self.fillColor = c

	def restore(self):
		self.xforms.pop()
		self.xform = self.xforms[-1] if len(self.xforms) else Matrix2()
		self.reset()

	def transform(self, vec, tin = None):
		self.pos = self.xform.transform(vec)
		self.tanIn = tin
	
	def tangentIn(self):
		return self.tanIn if self.tanIn else self.zero

	def setName(self, shape):
		shape.name = 'Path ' + str(self.path)
		if self.fill: shape.name = shape.name + '(Fill)';
		elif not self.closed: shape.name = shape.name + '(Open)'

class PDFToRoto():
	def __init__(self, path):
		self.path = path
		self.input = pdf.PdfFileReader(file(path, 'rb'))

	def pages(self):
		return self.input.getNumPages()

	def parsePDF(self, page = 0 ) :
		page = self.input.getPage(page)
		content = page['/Contents'].getObject()
		return page, pdf.ContentStream(content, page.pdf)

	@staticmethod
	def pdfAttrs(obj,attrs):
		while len(attrs) and obj.get(attrs[0]):
			obj = obj[attrs[0]]
			attrs.pop(0)
		return obj

	@staticmethod
	def setColor( attrs, cf, pfx = ''):
		if cf and len(cf)>=3:
			attrs.set('r'+pfx, cf[0])
			attrs.set('g'+pfx, cf[1])
			attrs.set('b'+pfx, cf[2])

	@staticmethod
	def finish(state, shape, skipEmpty):
		if state.skip and skipEmpty:
			return None

		if state.tanIn:
			if state.closed or state.fill:
				cp = shape[0]
				cp.leftTangent.setPosition(state.tanIn)
				cp.featherLeftTangent.setPosition(state.tanIn)
			else:
				shape.setFlag(rotopaint.FlagType.eOpenFlag,1) # Nuke bug has no effect
				shape.append( ShapeControlPoint(state.pos, state.tanIn, state.zero, state.zero, state.tanIn, state.zero) )
		elif not state.closed:
			shape.append(state.pos)

		state.setName(shape)
		attrs = shape.getAttributes()
		if state.fillColor:
			PDFToRoto.setColor(attrs, state.fillColor)
		if state.strokeColor:
			PDFToRoto.setColor(attrs, state.strokeColor, 'o')

		return shape

	def parse(self, node, page = 0, skipEmpty = False, needGS = False ) :
		knob = node.knob('curves')
		root = knob.rootLayer

		page, content = self.parsePDF(page)
		root.removeAll()

		shape, layer = None, None
		state = State()
		for operands,operator in content.operations:
			# print operands,operator
			if needGS:
				if operator=='gs': needGS = False;
				continue

			#if operator == 'gs':
				#page['/Resources']['/ExtGState'][operands[0]]['/BM'] blend mode
				#page['/Resources']['/ExtGState'][operands[0]]['/CA'] stroke alpha
				#page['/Resources']['/ExtGState'][operands[0]]['/ca'] non-stroke alpha

			if operator == 'BDC':  # properties
				layer = Layer(knob)
				name = PDFToRoto.pdfAttrs(page, ['/Resources', '/Properties',operands[1],'/Name'])
				if name: layer.name = str(name)

			elif operator == 'n':  # end, no-fill, no-stroke
				state.skip = True
			elif operator == 'h':  # close path
				state.closed = True
			elif operator == 's':  # close, stroke
				state.closed = True
			#elif operator == 'S':  # stroke
			elif operator == 'f' or operator == 'F' or operator == 'f*':   # fill
				state.fill = True

			elif operator == 'q':  # save graphics state
				state.save()
			elif operator == 'cm':  # concat matrix abcdef
				state.xform *= Matrix2(operands[0], operands[1], operands[2], operands[3], operands[4], operands[5])	

			elif operator == 'rg':  # r,g,b non-stroke (fill)
				state.setFill([float(v) for v in operands])
			elif operator == 'RG':  # r,g,b stroke
				state.setStroke([float(v) for v in operands])
			elif operator == 'EMC': # end layer
				root.append(layer)
				layer = None
			elif operator == 'Q':  # restore graphics state
				if shape:
					shape = PDFToRoto.finish(state, shape, skipEmpty)
					if shape:
						if layer != None:
							layer.insert(0,shape)
						else:
							root.insert(0,shape)
						shape = None
				state.restore()

			elif operator == 'm':  # new path at x,y
				if not shape: shape = Shape(knob);
				state.transform(operandToVectors(operands)[0])
			elif operator == 'l':  # line x, y
				if state.tanIn:
					shape.append( ShapeControlPoint(state.pos, state.tanIn, state.zero, state.zero, state.tanIn, state.zero) )
				else:
					shape.append(state.pos)
				state.transform(operandToVectors(operands)[0])

			elif operator == 'c':  # bezier [C, P1, P2, P3 ]
				v = [ state.xform.transform(v) for v in operandToVectors(operands) ]
				tanIn, tanOut = state.tangentIn(), v[0]-state.pos
				shape.append( ShapeControlPoint(state.pos, tanIn, tanOut, state.zero, tanIn, tanOut) )
				state.pos = v[2]
				state.tanIn = v[1]-state.pos
			elif operator == 'v':  # bezier [C, C,  P2, P3 ] 
				v = [ state.xform.transform(v) for v in operandToVectors(operands) ]
				tanIn, tanOut = state.tangentIn(), state.zero
				shape.append( ShapeControlPoint(state.pos, tanIn, tanOut, state.zero, tanIn, tanOut) )
				state.pos = v[1]
				state.tanIn = v[0]-state.pos
			elif operator == 'y':  # bezier [C, P1, P2, P2 ]
				v = [ state.xform.transform(v) for v in operandToVectors(operands) ]
				tanIn, tanOut = state.tangentIn(), v[0]-state.pos
				shape.append( ShapeControlPoint(state.pos, tanIn, tanOut, state.zero, tanIn, tanOut) )
				state.pos = v[1]
				state.tanIn = state.zero

			elif operator == 're': # rectangle x, y, width, height
				rec = operandToVectors(operands)
				pt, size = state.xform.transform(rec[0]), rec[1]
				recShape = Shape(knob)
				recShape.append(pt)
				recShape.append(Vector3(pt.x+size.x, pt.y,0))
				recShape.append(Vector3(pt.x+size.x, pt.y+size.y,0))
				recShape.append(Vector3(pt.x, pt.y+size.y,0))
				root.append(recShape)

		if shape != None:
			if layer != None:
				layer.insert(0,shape)
				shape = layer
			root.insert(0,shape)

	def create(self, page = 0, skipEmpty = False, needGS = False ) :
		self.parse(nuke.createNode('Roto'), page, skipEmpty, needGS)


def build():
	node = nuke.thisNode()
	import geometry.rotopdf
	PDFToRoto(node.knob('file').getValue()).parse(node)
