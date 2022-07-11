#!/usr/bin/env python
try:
	import nuke
except ImportError:
	nuke = None
	
import os
import sys

_GIZMO_PATH_STORAGE_DICT = {}

def generate_Gizmo_Menu():
	menu = nuke.menu( 'Nuke' ).addMenu("Gizmos")	
	for m,gs in sorted(_GIZMO_PATH_STORAGE_DICT.items()):
		m = menu.addMenu(m)
		for g in sorted(gs, key=str.lower):
			m.addCommand(g , "nuke.createNode('%s')" % g)

def recursively_Scan_And_Set_Gizmo_Paths(Directory_Path,addToSystemPath=False):
	root, dirs, files = next(os.walk(Directory_Path))
	addit = 0
	for f in files:
		if os.path.splitext(f)[-1] ==  ".gizmo":
			addit=1
			break
	if addit:
		nuke.pluginAddPath(Directory_Path.replace("\\","/"), addToSystemPath)
		if os.name == "nt":
			m = os.path.normpath(root).split("\\")[-1]
		else:
			m = os.path.normpath(root).split("/")[-1]
		if not m in list(_GIZMO_PATH_STORAGE_DICT.keys()):
			_GIZMO_PATH_STORAGE_DICT[m] = []
		for f in files:
			fsplit = f.split(".")
			if fsplit[-1] == "gizmo":
				_GIZMO_PATH_STORAGE_DICT[m].append(fsplit[0])
			
	for d in dirs:
		if not d.startswith("."):
			path = root+"/"+d
			recursively_Scan_And_Set_Gizmo_Paths(path,addToSystemPath)
			
			
def AddGizmo_Paths(Directory_Path,addToSystemPath=False):
	recursively_Scan_And_Set_Gizmo_Paths(Directory_Path,addToSystemPath)