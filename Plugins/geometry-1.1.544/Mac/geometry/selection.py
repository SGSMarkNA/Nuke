# Selection utilities

import nuke

def nodeFromViewer():
	av = nuke.activeViewer()
	i = av.activeInput()
	n = av.node().input(i)
	return n

def setMode( mode = None ):
	try : n = nuke.selectedNode()
	except ValueError : n = nodeFromViewer()
	if not n: return
	k = n.knob('action')
	if not k: return

	if mode == None:
		mode = k.getValue()+1;
		mode = int( mode if mode <= 2 else 0 )
	elif type(mode)==int:
		if mode < 0 : mode = k.getValue()+mode; mode = int( mode if mode >= 0 else 2 );
	elif mode=='f' or mode=='face':
		mode = 'Select faces'
	elif mode=='e' or mode=='edge':
		mode = 'Select edges'
	elif mode=='v' or mode=='vertices':
		mode = 'Select vertices'
	n.knob('action').setValue(mode)

def pyKnob():
	try : n = nuke.selectedNode()
	except ValueError : n = nodeFromViewer()
	return n.knob('polySelection') if n else None

def edgeLoop( useOver = True ):
	k = pyKnob()
	if k: k.loop(useOver);

def edgeRing( useOver = True ):
	k = pyKnob()
	if k: k.ring(useOver);

def growSelection( n=1, mask=0x00000004 ):
	# if mask < 1 or mask > 7 throw ValueError
	k = pyKnob()
	if k:
		for i in xrange(0,n):
			k.growSelection(mask);
