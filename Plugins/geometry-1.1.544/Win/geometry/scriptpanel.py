# Expression editing window

import nuke, nukescripts

class ScriptPanel( nukescripts.PythonPanel ):
	size = [500,300]

	def __init__( self, kedit, name = "" ):
		nukescripts.PythonPanel.__init__(self, "Edit " + name, "geometry.ScriptPanel")
		self.script = nuke.Multiline_Eval_String_Knob( "script", "" )
		self.addKnob( self.script )
		self.script.setTooltip('Multiline attribute expression.\nValue is set via  @b;ret@n; variable')
		self.script.setValue(kedit.getText());
		# self.setMinimumSize(ScriptPanel.size[0], ScriptPanel.size[1])
		self.setupSize(kedit)
	
	def setupSize( self, kedit ) :
		w = 80
		h = 20
		if kedit:
			exprs = kedit.getText()
			lines = exprs.split('\n')
			h = max(h, len(lines))
			for line in lines:
				w = max(w, len(line))
		self.script.setValue(exprs)
		self.setMinimumSize(int(w*7.5), int(h*15))
	
	def showModalDialog( self ):
		return nukescripts.PythonPanel.showModalDialog(self)
		#return self.script.getText() if  else None

def run( name = None ):
	kname = nuke.thisKnob().name()
	print kname
	node = nuke.thisNode()
	knob = node[kname.replace('Edit', 'Expression')]
	p = ScriptPanel(knob, name if name else node[kname.replace('Edit', 'Name')].getText())
	if p.showModalDialog() :
		knob.setText(p.script.getText())
	ScriptPanel.size = [p.width(), p.height()]
	p.destroy()
