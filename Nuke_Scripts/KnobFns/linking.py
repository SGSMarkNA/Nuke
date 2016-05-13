try :
	import nuke
except ImportError:
	nuke = None
	
def link_bounding_boxs(From,To):
	writeNode = To.dependencies(nuke.INPUTS)[0]
	argname = From.name()
	options = nuke.WRITE_ALL | nuke.WRITE_USER_KNOB_DEFS | nuke.TO_SCRIPT
	args = To.writeKnobs(options)
	box = str("box {{%s.box.x} {%s.box.y} {%s.box.r} {%s.box.t}}" %
		      (argname,argname,argname,argname))

	args2 = str(args[ : args.find('box {')] + box)
	new = nuke.createNode("CropPNG",args2)
	new.connectInput(0,writeNode)
	nuke.delete(To)
	
def link_selected_bounding_boxes():
	selList = nuke.selectedNodes()
	Master = selList.pop(0)
	for n in selList:
		link_bounding_boxs(Master,n)