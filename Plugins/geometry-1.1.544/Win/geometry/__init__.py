# Initialize the Geometry plugins
#
# Setup plug-in paths with optional sub-directories for nuke version and platform:
#   Assuming Nuke 9.0 run on OS X setupPaths would do the following:
# setupPaths()               -> <installion root>/plug-ins
# setupPaths(True)           -> <installion root>/plug-ins/9.0
# setupPaths(True, True)     -> <installion root>/plug-ins/9.0/macos
# setupPaths(False, True)    -> <installion root>/plug-ins/macos

import nuke
def setupPaths(versioned=False, platformed = False):
	import os.path as op, posixpath as pp
	base = op.dirname(op.dirname(__file__))
	plugs = pp.join(base, 'plug-ins')
	if versioned:
		plugs = pp.join(plugs, '%s.%s'%(nuke.NUKE_VERSION_MAJOR, nuke.NUKE_VERSION_MINOR))
	if platformed:
		platform = 'macos' if nuke.env.get('MACOS') else 'linux' if nuke.env.get('LINUX') else 'windows'
		plugs = pp.join(plugs, platform)

	nuke.pluginAddPath( plugs )
	nuke.pluginAppendPath(plugs)
	nuke.pluginAddPath( pp.join(base, 'rsrc') )
	nuke.pluginAddPath( pp.join(base, 'icons') )
	nuke.pluginAppendPath(pp.join(base, 'icons') )
	nuke.pluginAppendPath(pp.join(base, 'rsrc'))

setupPaths()

# Callbacks from Geometry node buttons, theoretically these could only be defined
# if in GUI mode, but nice to support nuke.toNode(name).knob(name).execute() when not

# Entry point for PolyText, PolyShape, PolyShards plugins
def createAxisPivots( node, local = True, offset = 4 ) :
	import geometry.axis
	aPiv = geometry.axis.AxisPivots(node, offset)
	if not aPiv.len: return;

	for i in aPiv.range() :
		axis = aPiv.input(i)
		prev = axis != None
		if not prev :
			axis = getattr(nuke.nodes, 'Axis')()
			aPiv.setInput(i, axis)
		if local : aPiv.set(i, axis, prev);

	aPiv.clear()
	aPiv.ui()


def rotoPoints( name, frame ) :
	import geometry.roto
	return geometry.roto.RotoEvaluate(nuke.toNode(name)).parse(frame)


# ModifyAttributes
# Only way to consistently update the UI is doing this in python
def attributesVisible(node, vis=None): 
	nActive = node.knob('nActive')
	idx = int(nActive.getValue())
	if vis: idx = idx + 1

	names = ['agroup', 'Group', 'Type', 'Enable', 'Name', 'Value', 'Expression', 'Edit']
	call = nuke.Knob.clearFlag if vis else nuke.Knob.setFlag
	for name in names:
		k = node.knob('attribute%s%s'%(idx,name))
		# k.setVisible(vis)
		call(k, nuke.INVISIBLE)

def scriptPanel():
	import geometry.scriptpanel
	geometry.scriptpanel.run()

# Lock CurveAttach.pos as READ_ONLY and other UI setup
def setupCurveAttach():
	node = nuke.thisNode()
	k = node.knob('pos')
	if k:
		k.setFlag(0x10000000)
	k = node.knob('flags')
	if k and not int(k.getValue()) & 0x00000001:
		k = node.knob('up')
		if k:
			k.setFlag(nuke.DISABLED)

nuke.addOnCreate(setupCurveAttach, nodeClass='CurveAttach')
