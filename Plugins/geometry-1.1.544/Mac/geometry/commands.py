# Nuke menu-commands

import nuke, fontcycler, preftab, defaults
import threading

#
# PolyText routines

def createPolyText() :
	n = nuke.createNode('GT_PolyText')
	k = n.knob('font')
	if k.value() == 'default' :
		k.setValue( defaults.font() )
	return n

def polyTextKeysChanged( knob = None , k1 = None ) :
	if k1: polyTextKeysChanged(k1, None);
	if not knob: knob = nuke.thisKnob()
	name = knob.name()
	if name.find('polyTextFont')==0:
		dir = name.split('polyTextFont')[1]
		fontcycler.addCommand(name, 1 if dir=='Next' else -1,  knob.getValue())

def setupTextCurve(curveDistr, text):
	curveDistr.knob('turn').setValue(0.75)
	if text.Class() == 'GT_PolyText':
		k = text.knob('place')
		k.setValue(k.value()+' Center-X')

def createCurveDistribute():
	sel = nuke.selectedNodes()
	node = nuke.createNode('GT_CurveDistribute')
	if len(sel)>1:
		setupTextCurve(node, sel[1])
	return node

def createCurveEdit():
	node = nuke.createNode('GT_PolyEdit')
	node.setName('CurveEdit1')
	node.knob('action').setValue(2)
	node.knob('culling').setValue(2)
	return node

def createPolyUVView():
	node = nuke.createNode('GT_PolyUV')
	node.knob('selectable').setValue(False)
	node.knob('gl_color').setValue(0xff0000ff)
	return node

def rotoPDF():
	node = nuke.createNode('RotoPDF')
	node.knob('Import').setFlag(0)
	file = nuke.getFilename('Choose Illustrator/PDF file', '*.ai *.pdf')
	if file:
		node.knob('file').setValue(file)
		node.knob('reload').execute()
	return node

def addCommand(menu, node, cmd=None, index=None) :
	if cmd==None:
		cmd = 'nuke.createNode("GT_'+node+'")'
	if index==None:
		menu.addCommand(node, cmd, icon=node+'.png')
	else:
		menu.addCommand(node, cmd, icon=node+'.png',index=index)

def subMenu( menu, *args ) :
	for node in args:
		if node=='-':
			menu.addSeparator()
		else:
			addCommand(menu, node)
	return menu

def setupNodes( tb, path = None ) :
	ply = subMenu( tb.addMenu('Poly'), 'PolyShape', 'PolyShards', '-', 'PolyBoolean', 'PolyExtrude', 'PolyEdit', 'PolyFacet', 'PolySubdivide', 'PolyUV')
	addCommand(ply, 'PolyUV (View)', 'geometry.commands.createPolyUVView()')
	addCommand(ply, 'PolyText', 'geometry.commands.createPolyText()', 0)
	addCommand(ply, 'PolyCube', 'nuke.createNode("PolyCube")', 3)
	addCommand(ply, 'PolyFuse', 'nuke.createNode("PolyFuse")')

	crv = subMenu( tb.addMenu('Curve'), 'Curve3D', '-', 'CurveSweep', 'CurveRevolve', '-', 'CurveSampler')
	addCommand(crv, 'Circle3D', 'nuke.createNode("Circle3D")', 1)
	addCommand(crv, 'Rectangle3D', 'nuke.createNode("Rectangle3D")', 2)
	addCommand(crv, 'CurveExtrude', 'nuke.createNode("CurveExtrude")', 6)
	addCommand(crv, 'CurveDistribute', 'geometry.commands.createCurveDistribute()', 8)
	addCommand(crv, 'CurveAttractor', 'nuke.createNode("GT_CurveAttractor")', 9)
	addCommand(crv, 'CurveAttach', 'nuke.createNode("CurveAttach")', 10)
	addCommand(crv, 'CurveEdit', 'geometry.commands.createCurveEdit()', 11)

	dfrm = subMenu( tb.addMenu('Deform'), 'DeformBend', 'DeformBulge', 'DeformTaper', 'DeformTwist', 'DeformTransform')

	utl = subMenu(tb.addMenu('Utility'), 'CopyGeo', 'ModifyAttributes', 'Field')
	addCommand(utl, 'Text3D', 'geometry.commands.createPolyText()')
	addCommand(utl, 'Roto3D', 'nuke.createNode("Roto");nuke.createNode("GT_PolyShape")')
	addCommand(utl, 'RotoPDF', 'geometry.commands.rotoPDF();')

	#############  Added docs help link... RKB 07-14-15  ############################
	docs = subMenu(tb.addMenu('Help'))
	addCommand(docs, 'Docs Link', 'geometry.commands.open_docs_url()')
	#################################################################################
	
	if not path :
		import sys
		path = defaults.kGlobalSettings[sys.platform]

	hotKeys = defaults.kGlobalSettings['hotkeys']
	prefs = preftab.PrefTab()
	if ( prefs.setDefaults('Geometry') ) :
		prefs.set([['polyTextFont', path]], 'File_Knob')
		if hotKeys:
			ks = prefs.set([ ['polyTextFontNext', '','Hotkey to advance PolyText.font forward'],
							 ['polyTextFontPrev', '','Hotkey to advance PolyText.font backward']],
							'String_Knob')
			ks[1].clearFlag(nuke.STARTLINE)

		prefs.set([['geometryPointOver', 0x5DBBF7FF], ['geometryPointSelect', 0xF7931EFF],
					  ['geometryEdgeOver', 0x5DBBF7FF], ['geometryEdgeSelect', 0xF7931EFF],
					  ['geometryFaceOver', 0x5DBBF7FF], ['geometryFaceSelect', 0xF7931EFF],
					  ['geometryCurve3DTangent', 0xCC00CCff]], 'ColorChip_Knob')
		prefs.set([['geometryOutlineSize', 1.0], ['geometryPointSize', 7.0]], 'Double_Knob')

		prefs.set([['geometryWireSize', 0.5]], 'Double_Knob', False)
		ks = prefs.set([['geometryWirePattern', 1], ['geometryOverPattern', 3]], 'Int_Knob')
		ks[0].setRange(0,80); ks[0].setFlag(0x00000002);
		ks[1].setRange(0,10); ks[1].setFlag(0x00000002);ks[1].clearFlag(nuke.STARTLINE);
		prefs.set([['geometryWireColor', 0x6f6f6fff]], 'ColorChip_Knob')
		prefs.set([['geometryEditGeoWidth', 0.5]], 'Double_Knob', False)
		prefs.set([['geometryMenuSelect', 'rmb'], ['geometryRaySelect', 'meta+rmb'], ['geometryFrustSelect', 'lmb']], 'String_Knob', False)
		prefs.set([['geometryLiveSelect', True]], 'Boolean_Knob')

	# prefs don't have loaded values yet, and the following fixes that
	# but to heavy handed for default installation ?
	if hotKeys :
		prefs.watch(polyTextKeysChanged)
		t = threading.Timer(2, nuke.executeInMainThreadWithResult, [polyTextKeysChanged, (prefs.knob('polyTextFontNext'), prefs.knob('polyTextFontPrev'))])
		t.start()

#############  Added docs help link... RKB 07-14-15  ############################

def open_docs_url():

	import os
	import sys

	try:
		import subprocess
		def _run(cmd, shell, wait):
			opener = subprocess.Popen(cmd, shell=shell)
			if wait:
				opener.wait()
			return opener.pid
	except ImportError:
		import popen2
		def _run(cmd, shell, wait):
			opener = popen2.Popen3(cmd)
			if wait:
				opener.wait()
			return opener.pid

	def _open(url, wait=0):
		if sys.platform == "darwin":
			cmd = ["open", url]
		elif hasattr(os, "startfile"):
			return os.startfile(url)
		elif "KDE_FULL_SESSION" in os.environ or "KDE_MULTIHEAD" in os.environ or \
		     "GNOME_DESKTOP_SESSION_ID" in os.environ or "GNOME_KEYRING_SOCKET" in os.environ:
			cmd = ["xdg-open", url]
		else:
			raise OSError("Desktop not supported.")

		return _run(cmd, 0, wait)

	_open('http://greyangle.com/nuke/docs/geometry/')

#################################################################################

