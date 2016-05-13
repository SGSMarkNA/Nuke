#!/usr/bin/env python


try :
	import nuke
except ImportError:
	nuke = None

from . import placement

def scale_from_center(value=None, X=1, Y=1):
	if value == None:
		value = nuke.getInput("Scale Amount in pixels", "1")
	if not value == None:
		value = float(value)
		nodes = nuke.thisGroup().selectedNodes()
		amount = len( nodes )
		if amount == 0:    return
		allX = 0
		allY = 0
		for n in nodes:
			allX += n.xpos()
			allY += n.ypos()

		centreX = allX / amount
		centreY = allY / amount

		if X and Y:
			for n in nodes:
				n.setXpos( int(centreX + ( n.xpos() - centreX ) * value) )
				n.setYpos( int(centreY + ( n.ypos() - centreY ) * value) )
		elif X:
			for n in nodes:
				n.setXpos( int(centreX + ( n.xpos() - centreX ) * value) )
		elif Y:
			for n in nodes:
				n.setYpos( int(centreY + ( n.ypos() - centreY ) * value) )

def gid_snap_selected():
	n = nuke.selectedNodes();
	for i in n:
		nuke.autoplaceSnap(i)

def aline_Avarage(direction,**kwargs):
	'''Align nodes either horizontally or vertically.'''
	nodes = kwargs.get( "nodes", nuke.thisGroup().selectedNodes() )
	if not len(nodes):
		nuke.message("No Nodes Selected")
	else:
		if direction == "v":
			avrg = int(float(sum([n.ypos() for n in nodes]) / len( nodes )))
			[n.setYpos(avrg) for n in nodes]
		if direction == "h":
			avrg = int(float(sum([n.xpos() for n in nodes]) / len( nodes )))
			[n.setXpos(avrg) for n in nodes]

def aline_horizontal_avarage(**kwargs):
	aline_Avarage("h",**kwargs)

def aline_vertical_avarage(**kwargs):
	aline_Avarage("v",**kwargs)

def Offset(Xofv=0, Yofv=0, Xswch=True, Yswch=True, nodes=None):

	if not nodes:
		nodes = nuke.selectedNodes()

	nodeCount = len(nodes)

	if Xswch:
		reordered = placement.reorder_From_left_to_right(nodes)
		for i in range(1,nodeCount,1):
			reordered[i].setXpos( int(float( reordered[i-1].xpos() + Xofv )) )

	if Yswch:
		reordered = placement.reorder_from_top_to_bottom(nodes)
		for i in range(1,nodeCount,1):
			reordered[i].setYpos( int(float( reordered[i-1].ypos() + Yofv )) )

