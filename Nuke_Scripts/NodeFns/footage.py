try:
	import nuke
except ImportError:
	nuke = None

import os
import re
import subprocess

def full_file_path(nod):
	""" Bakes Any Expression or Variables And Returns The Full File Path Name From A Read Or Write Node"""
	# GET THE FULL FILE PATH NAME
	res = nuke.filename(nod, nuke.REPLACE)
	return str(res)

def reload_all_footage(*args,**kargs):
	group = kargs.get("group",nuke.root())
	for n in nuke.allNodes("Read",group=group):
		if not n["disable"].value():
			if os.path.exists(nuke.filename(n,nuke.REPLACE)):
				filename = os.path.dirname(nuke.filename(n,nuke.REPLACE))+"/"+os.path.basename(nuke.filename(n,nuke.REPLACE)).split(".")[0]
				print("Readloading '%s'" % filename)
				n.knob("reload").execute()
	groups = nuke.allNodes("Group",group=group)+[n for n in nuke.allNodes(group=group) if isinstance(n,nuke.Gizmo)]
	for i in groups:
		reload_all_footage(group=i)

def collect_read_nodes(scanGroup="Start",storageGroup=None):
	if scanGroup == "Start":
		scanGroup = nuke.root()
	if storageGroup == None:
		with nuke.root():
			storageGroup = nuke.nodes.Group(name = "ReadNode_storageGroup")
	for n in nuke.allNodes(group=scanGroup):
		n.setSelected(False)

	for n in nuke.allNodes("Read",scanGroup):
		print("Selecting ReadNode %s" % n.fullName())
		n.setSelected(True)
	with scanGroup:
		if len(nuke.selectedNodes()):
			nuke.nodeCopy ( '%clipboard%' )
			with storageGroup:
				nuke.nodePaste( '%clipboard%' )

	for n in nuke.allNodes("Group",scanGroup):
		print(n.fullName())
		if not n.name() == "ReadNode_storageGroup":
			collect_read_nodes(n,storageGroup)

def get_read_paths(method):
	"""Returns file names from all Read nodes.

	Options:
	file - outputs only file names
	dir  - outputs only directory names
	long - outputs the entire path"""
	# create variable for the text
	finalmsg = ""
	#go thru all the nodes
	allnodes = nuke.allNodes(group = nuke.root())

	for i in allnodes:
		_class = i.Class()

		if _class == "Read":
			# get the name of the file dir (just the last part)
			# use this to get only the filename
			curname = ""
			name = nuke.filename(i)

			if name is None:
				continue

			if method == "file":
				curname = os.path.basename(name)

			# use this to get only the dir
			if method == "dir" or method == "":
				curname = os.path.dirname(name)

			# get the whole path
			if method == "long":
				curname = name

		curname = re.sub("\.%.*", "", curname)
		# add on to existing variable
		# make sure to avoid adding the slate image :)
		match = re.search("slate", curname)
		if match is None:
			finalmsg += curname

		finalmsg += "\n"
	return finalmsg

def go_to_file():
	'''This is the function that is currently being accessed via CNTRL-f(Win) or CMD-f(Mac)... 09-22-15 RKB.'''
	grp = nuke.thisGroup()
	with grp:
		node = nuke.selectedNode()
		try:
			filePath = nuke.filename(node.knob("file").node(), nuke.REPLACE)
		except:
			raise ValueError("The selected node '%s' does not have a File_Knob." % node.name())
	
	if filePath == None:
		nuke.message("The selected node '%s' does not have a valid file path." % node.name())
	else:
		if os.name == 'nt':
			filePath = "\\".join(filePath.replace("/","\\").split("\\")[:-1])
			if os.path.exists(filePath):
				print(filePath)
				os.system( 'C:/WINDOWS/explorer ' + filePath)
			else:
				nuke.message("The selected node's '%s' File_Knob value\n%r\ncould not be accesed through Windows Explorer or does not exist." % (node.name(),filePath))
		elif os.name == 'posix':
			filePath = '/'.join(filePath.split('/')[:-1])
			if os.path.exists(filePath):
				print(filePath)
				subprocess.Popen(['open', filePath])
			else:
				nuke.message("The selected node's '%s' File_Knob value\n%r\ncould not be accesed through the Finder or does not exist." % (node.name(),filePath))

def go_To_This_Nodes_file():
	node = nuke.thisNode()
	try:
		filePath = nuke.filename(node.knob("file").node())
	except:
		nuke.message("The selected node '%s' does not have a File_Knob.\nSincerely, and with great sadness,\nYour Friend,\nThe Message Writer." % node.name())

	if filePath == None:
		nuke.message("The selected node '%s' does not have a valid file path.\nSincerely, and with great sadness,\nYour Friend,\nThe Message Writer." % node.name())
	else:
		if os.name == 'nt':
			filePath = "\\".join(filePath.replace("/","\\").split("\\")[:-1])
			if os.path.exists(filePath):
				print(filePath)
				os.system( 'C:/WINDOWS/explorer ' + filePath)
			else:
				nuke.message("The selected node's '%s' File_Knob value\n%r\ncould not be accesed through Windows Explorer or does not exist.\nSincerely, and with great confusion,\nyour friend,\nThe Message Writer." % (node.name(),filePath))
		elif os.name == 'posix':
			filePath = '/'.join(filePath.split('/')[:-1])
			if os.path.exists(filePath):
				print(filePath)
				subprocess.Popen(['open', filePath])
			else:
				nuke.message("The selected node's '%s' File_Knob value\n%r\ncould not be accesed through the Finder or does not exist." % (node.name(),filePath))

def missingFrames():
	"""find the missing frames in a given read node and return them"""
	missingFiles = []
	completeFileName = ""

	# first check if a node is selected and if so if it is a read node
	selectedNodes = nuke.selectedNodes()

	# either nothing or too much is selected
	if (len(selectedNodes) != 1):
		nuke.message("This only works if you select one Read node!")
		return "Fail"

	nodeType = selectedNodes[0].Class()

	if (nodeType != "Read"):
		nuke.message("This only works if you select one Read node!")
		return "Fail"

	#now we are sure one read node is selected, so go on.

	readNode = selectedNodes[0]

	fileNameLong = readNode.knob("file").value()
	startFrame = readNode.knob("first").value()
	endFrame = readNode.knob("last").value()

	# split the long file name with path to its subsections
	splitFileNameLong = os.path.split(fileNameLong)
	fileNameShort = splitFileNameLong[1]
	pathName = splitFileNameLong[0]
	splitFileName = fileNameShort.split(".")

	if (len(splitFileName) != 3):
		nuke.message("File does not have the format name.number.ext.\nSearch the missing frames yourself :)")
		return "Fail"

	fileName = splitFileName[0]
	filePaddingOrg = splitFileName[1]
	filePaddingLength = len((filePaddingOrg) % 0)
	fileExtension = splitFileName[2]


	# now with all that given information search for missing files in the sequence
	for i in range(startFrame, endFrame+1):
		# first build the string of the padded frameNumbers
		frameNumber = str(i)

		while(len(frameNumber) < filePaddingLength):
			frameNumber = "0" + frameNumber

		completeFileName = pathName + "/" + fileName + "." + frameNumber + "." + fileExtension

		if not os.path.isfile(completeFileName):
			missingFiles.append(i)

	if(len(missingFiles) == 0):
		nuke.message("No file seems to be missing")
		return

	cleanedUpMissingFiles = cleanUpList(missingFiles)

	nuke.message("In the frame range: " + str(startFrame) + "-" + str(endFrame) + "\nThe following files are missing:\n\n" + cleanedUpMissingFiles)

	return

def cleanUpList(missingFrames):
	"""from a sequencial array create a readable list which is returned"""
	cleanMissingFrames = []
	missingFramesNice = ""
	dirtySize = 0
	minV = 0
	maxV = 0

	dirtySize = len(missingFrames)

	minV = missingFrames[0]
	maxV = missingFrames[0]

	for i in range(dirtySize):
		if (missingFrames[i] == (maxV+1)):
			#as long as the frames are in sequence, update the maxV value
			maxV = missingFrames[i]
		else:
			#if not in sequence, set the values
			cleanMissingFrames.append(minV)
			cleanMissingFrames.append(maxV)
			minV = maxV = missingFrames[i];

		if (i == (dirtySize-1)):
			#write the values if the list is at the end
			cleanMissingFrames.append(minV)
			cleanMissingFrames.append(maxV)

	for i in range(2,len(cleanMissingFrames),2):
		# create the formated output of the frames in the window for the user to shorten the list
		if(cleanMissingFrames[i] == cleanMissingFrames[i+1]):
			missingFramesNice += (str)(cleanMissingFrames[i]) + ", "
		else:
			missingFramesNice += (str)(cleanMissingFrames[i]) + "-" + (str)(cleanMissingFrames[i+1]) + ", "


	return missingFramesNice

def png_to_mov():

	for i in nuke.selectedNodes():
		curPath = i.knob('file').value()
		curDir = os.path.dirname(curPath)
		curFile = os.path.basename(curPath)
		baseName = re.sub(r'%04d.png$', "", curFile)
		qtDir = os.path.join(curDir,baseName+'tif')
		qtFile = baseName + '.tif'
		qtPath = os.path.join(qtDir, qtFile)
		qtPathN = qtPath.replace('\\','/')
		try:
			os.mkdir(qtDir)
		except OSError:
			pass
		ypos = i.knob('ypos').value()+100
		xpos = i.knob('xpos').value()
		m = nuke.createNode('Write')
		m.setInput(0,i)
		m.knob('ypos').setValue(ypos)
		m.knob('xpos').setValue(xpos)
		print(qtFile)
		m.knob('file').setValue(qtPathN)
		#m.knob('codec').setValue(0)

def exr2exr():

	for i in nuke.selectedNodes():
		curPath = i.knob('file').value()
		curDir = os.path.dirname(curPath)
		curDirN = curDir + ('/')
		curFile = os.path.basename(curPath)
		baseName = re.sub(r'%04d.exr$', "", curFile)
		qtFile = baseName + '.exr'
		qtPath = os.path.join(curDirN, qtFile)
		ypos = i.knob('ypos').value()+100
		xpos = i.knob('xpos').value()
		m = nuke.createNode('Write')
		m.setInput(0,i)
		m.knob('ypos').setValue(ypos)
		m.knob('xpos').setValue(xpos)
		m.knob('file').setValue(qtPath)
		m.knob('colorspace').setValue(1)
		m.knob("channels").setValue("rgba")

def exr2tif():
	reads = nuke.selectedNodes()

	for i in reads:
		curPath = i.knob('file').value()
		curDir = os.path.dirname(curPath)
		curDirN = curDir + ('/')
		curFile = os.path.basename(curPath)
		baseName = re.sub(r'%04d.exr$', "", curFile)
		qtFile = baseName + '.tif'
		qtPath = os.path.join(curDirN, qtFile)
		ypos = i.knob('ypos').value()+100
		xpos = i.knob('xpos').value()
		m = nuke.createNode('Write')
		m.setInput(0,i)
		m.knob('ypos').setValue(ypos)
		m.knob('xpos').setValue(xpos)
		m.knob('file').setValue(qtPath)
		m.knob('colorspace').setValue(1)
		m.knob("channels").setValue("rgba")
		m.knob('datatype').setValue(1)
		m.knob('compression').setValue(2)
