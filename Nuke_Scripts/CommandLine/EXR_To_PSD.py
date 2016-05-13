import os
import sys
import glob
import nuke

currentDir = os.getcwd()
g_readNodes = []
def fixPath (string):
	string = string.replace('\\', "/")
	return string

def deselect_all():
	for node in nuke.allNodes():
		node.setSelected(False)

def glob_exr_files(folder_name=None):
	global currentDir
	if folder_name == None:
		folder_name = currentDir
	glob_pattern = os.path.join( folder_name, str(".*.exr") )
	matching_paths = glob.glob(glob_pattern)
	matching_paths.sort()
	matching_paths =  [fixPath(f) for f in matching_paths]
	return matching_paths

def load_read_nodes():
	"""Loads all the read nodes and turns off postage stamp"""
	global currentDir, g_readNodes
	exr_files = glob_exr_files(currentDir)
	readNodes = []
	for exr in exr_files:
		new_read = nuke.createNode('Read')
		new_read.knob('file').fromUserText(exr)
		new_read.knob("postage_stamp").setValue(0)
		readNodes.append(new_read)
	g_readNodes = readNodes
	return readNodes

def save():
	# saves the script
	nuke.scriptSave("ready.nk")
	return 0

def loopReads():
	global currentDir, g_readNodes

	# loops over all the read nodes
	# start the counter
	count = 0
	# lets define our constant node
	constant = nuke.createNode('Constant')
	format = g_readNodes[0].knob('format').value()
	constant.knob('format').setValue(format)
	#grab all the read nodes
	all = nuke.selectAll()
	readNodes = nuke.selectedNodes('Read')
	#grab all the channels
	allChannels = nuke.layers()
	#lets start looping
	for node in g_readNodes:
		for channel in allChannels:
			if testChannel(channel):
				count = count + 1
				nodeOptions(count,constant,node,channel)
	# time to end
	return 0

def testChannel (channel):
	# test the channel of the node if it should be written out
	badChannels = ["mask","disparityR","disparityL","disparity","backward","forward","motion","rgba","none","depth","rotopaint_mask"]
	for index in range(len(badChannels)):
		if channel == badChannels[index]:
			return False
	return True

def nodeOptions (count, constant, node, channel):
	global currentDir
	deselect_all()
	node.setSelected(True)
	# creates any addtional nodes for specfic channels
	# grab the name of the channel for output
	fname = node.knob("file").getValue()
	fname = str(fname).strip(".exr")
	#cname = fname.split("_")
	#fname = cname
	nname = str(channel).strip("'[]")
	fname = fixPath(os.path.join(currentDir, (fname+"_"+nname+".tiff")))
	#print fname
	#create shuffle node and connect it
	ssn = nuke.createNode('Shuffle')
	nuke.Node.connectInput(ssn,1,node)
	ssn.knob("in").setValue(nname)
	#spectial options for channel types
	if nname.find('Normal') != -1:
		grad = nuke.createNode('Grade')
		nuke.Node.connectInput(grad,1,ssn)
		grad.knob("black").setValue(.5)
		grad.knob('maskChannelMask').setValue('none')
		fix = nuke.createNode('Merge')
		fix.knob("operation").setValue("plus")
		nuke.Node.connectInput(fix,0,constant)
		nuke.Node.connectInput(fix,2,node)
	elif nname.find('normal') != -1:
		grad = nuke.createNode('Grade')
		nuke.Node.connectInput(grad,1,ssn)
		grad.knob("black").setValue(.5)
		grad.knob('maskChannelMask').setValue('none')
		fix = nuke.createNode('Merge')
		fix.knob("operation").setValue("plus")
		nuke.Node.connectInput(fix,0,constant)
		nuke.Node.connectInput(fix,2,node)
	elif nname.find('normals') != -1:
		grad = nuke.createNode('Grade')
		nuke.Node.connectInput(grad,1,ssn)
		grad.knob("black").setValue(.5)
		grad.knob('maskChannelMask').setValue('none')
		fix = nuke.createNode('Merge')
		fix.knob("operation").setValue("plus")
		nuke.Node.connectInput(fix,0,constant)
		nuke.Node.connectInput(fix,2,node)
	elif nname.find('bumpnormals') != -1:
		grad = nuke.createNode('Grade')
		nuke.Node.connectInput(grad,1,ssn)
		grad.knob("black").setValue(.5)
		grad.knob('maskChannelMask').setValue('none')
		fix = nuke.createNode('Merge')
		fix.knob("operation").setValue("plus")
		nuke.Node.connectInput(fix,0,constant)
		nuke.Node.connectInput(fix,2,node)
	elif nname.find('bumpnormal') != -1:
		grad = nuke.createNode('Grade')
		nuke.Node.connectInput(grad,1,ssn)
		grad.knob("black").setValue(.5)
		grad.knob('maskChannelMask').setValue('none')
		fix = nuke.createNode('Merge')
		fix.knob("operation").setValue("plus")
		nuke.Node.connectInput(fix,0,constant)
		nuke.Node.connectInput(fix,2,node)
	elif nname.find('alpha') != -1:
		fix = nuke.createNode('Grade')
	elif nname.find('amb') != -1:
		fix = nuke.createNode('Grade')
	elif nname.find('VRayWireColor') != -1:
		grad = nuke.createNode('Grade')
		nuke.Node.connectInput(grad,1,ssn)
		fix = nuke.createNode('Merge')
		fix.knob("operation").setValue("plus")
		nuke.Node.connectInput(fix,0,constant)
		nuke.Node.connectInput(fix,2,node)
	elif nname.find('depth') != -1:
		grad = nuke.createNode('Grade')
		grad.knob("gamma").setValue(0.1)
		nuke.Node.connectInput(grad,1,ssn)
		fix = nuke.createNode('Merge')
		fix.knob("operation").setValue("plus")
		nuke.Node.connectInput(fix,0,constant)
		nuke.Node.connectInput(fix,2,node)
	elif nname.find('Brakes') != -1:
		fix = nuke.createNode('Grade')
	elif nname.find('Rimz') != -1:
		fix = nuke.createNode('Grade')
	elif nname.find('Trim') != -1:
		fix = nuke.createNode('Grade')
	elif nname.find('RGBm') != -1:
		grad = nuke.createNode('Grade')
		nuke.Node.connectInput(grad,1,ssn)
		fix = nuke.createNode('Merge')
		fix.knob("operation").setValue("plus")
		nuke.Node.connectInput(fix,0,constant)
		nuke.Node.connectInput(fix,2,node)
	elif nname.find('RGBo') != -1:
		grad = nuke.createNode('Grade')
		nuke.Node.connectInput(grad,1,ssn)
		fix = nuke.createNode('Merge')
		fix.knob("operation").setValue("plus")
		nuke.Node.connectInput(fix,0,constant)
		nuke.Node.connectInput(fix,2,node)
	elif nname.find('AMB') != -1:
		grad = nuke.createNode('Grade')
		nuke.Node.connectInput(grad,1,ssn)
		fix = nuke.createNode('Merge')
		fix.knob("operation").setValue("plus")
		nuke.Node.connectInput(fix,0,constant)
		nuke.Node.connectInput(fix,2,node)
	elif nname.find('MultiMatte') != -1:
		fix = nuke.createNode('Grade')
	elif nname.find('Multimatte') != -1:
		fix = nuke.createNode('Grade')
	elif nname.find('mm') != -1:
		fix = nuke.createNode('Grade')
	elif nname.find('mI') != -1:
		fix = nuke.createNode('Grade')
	elif nname.find('MM') != -1:
		fix = nuke.createNode('Grade')
	else:
		fix = nuke.createNode('SoftClip')
		fix.knob("conversion").setValue("preserve hue and brightness")
		fix.knob("softclip_min").setValue(0.8)
		fix.knob("softclip_max").setValue(3)
	#needs to return endNode for writeNodes
	endNode = fix
	count = count
	writeNodes(count, fname, endNode)
	return 0

def writeNodes (count, fname, endNode):
	# adds the write out node for the good channels
	wr = nuke.createNode('Write')
	nuke.Node.connectInput(wr,1,endNode)
	wr.knob("file").setValue(fname)
	wr.knob("file_type").setValue("tiff")
	wr.knob("compression").setValue("PackBits")
	if count == 4 :
		wr.knob("afterFrameRender").setValue("nuke.memory(\"free\")")
		count = 0
	return 0

def main():
	#main functions
	load_read_nodes()
	loopReads()
	save()
	return 0

# starts main loop
main()