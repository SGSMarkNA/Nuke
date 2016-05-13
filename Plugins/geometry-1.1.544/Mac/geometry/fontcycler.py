
import nuke, defaults

class FontCycler :
	_instance = None

	@staticmethod
	def instance() :
		if not FontCycler._instance:
			FontCycler._instance = FontCycler()
		return FontCycler._instance

	def __init__( self, path = None ) :
		self.setDirectory( path if path else defaults.font())

	def setDirectory( self, path ) :
		import os
		self.path = path if os.path.isdir(path) else os.path.dirname(path)
		self.fonts = os.listdir(self.path)
		self.index = 0
		self.join = os.path.join

	def cycle( self, i ) :
		self.index = self.index + i
		if   self.index < 0: self.index = len(self.fonts)-1;
		elif self.index >= len(self.fonts): self.index = 0
		self.setFont()

	def next( self ) :
		self.cycle(1)

	def prev( self ) :
		self.cycle(-1)

	def setFont( self ) :
		font = self.join(self.path, self.fonts[self.index])
		nds = nuke.selectedNodes()
		for node in nds :
			if node.Class().find('PolyText')!=-1:
				node.knob('font').setValue(font)

# want to cleanup FontCycler.instance so we should track these

def addCommand( name, cycle=0, key=0, menu=None ) :
	if not menu: menu = nuke.menu('Nuke')
	if key and cycle:
		menu.addCommand(name, 'geometry.fontcycler.FontCycler.instance().cycle('+str(cycle)+')', key);
	elif name:
		menu.removeItem(name)