#!/usr/bin/env python

import nuke
import os
import glob

def glob_file_matchs(folder_name,file_base_name,file_ext):

	glob_pattern = os.path.join( folder_name, str( file_base_name + "*." + file_ext ) )

	matching_paths = glob.glob(glob_pattern)
	matching_paths.sort()

	return matching_paths

def createWriteDir():
	if "%V" in nuke.filename(nuke.thisNode()):
		#print "Making View Directorys"
		oldname = nuke.filename(nuke.thisNode())
		knb = nuke.thisNode().knob("views")
		root = nuke.root()
		tn = nuke.thisNode()
		fknob = tn.knob("file")
		for v in knb.value().split():
			fknob.setValue(oldname)
			fknob.setValue(fknob.value().replace("%V",v))
			f = nuke.filename(nuke.thisNode(),nuke.REPLACE)
			d = os.path.dirname(f)
			osdir = nuke.callbacks.filenameFilter(d)
			#print "Checking for Dir %s" % osdir
			if not os.path.exists(osdir):
				#print "creating Dir %s" % osdir
				os.makedirs(osdir)
		fknob.setValue(oldname)
	else:
		#print "Making Single Directory"
		f = nuke.filename(nuke.thisNode(),nuke.REPLACE)
		d = os.path.dirname(f)
		osdir = nuke.callbacks.filenameFilter(d)
		if not os.path.exists(osdir):
			os.makedirs(osdir)