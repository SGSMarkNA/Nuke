try :
	import nuke
except ImportError:
	nuke = None

def filter_out_groups(nodelist):
	return [n for n in nodelist if not n.Class() == "Group"]

def filter_only_groups(nodelist):
	return [n for n in nodelist if n.Class() == "Group"]

def filter_remove_node_class(nodelist,types):
	return list([n for n in nodelist if not n.Class() in types])

def filter_only_node_class(nodelist,types):
	if isinstance(types,str):
		return list([n for n in nodelist if n.Class() == types])
	elif isinstance(types,list):
		return list([n for n in nodelist if n.Class() in types])

def filter_node_class_recursivly(types,group=None,collected=None):
	if group == None:
		group=nuke.root()
	if collected == None:
		collected = []
	nodes = group.nodes()
	for n in filter_only_node_class(nodes,types):
		collected.append(n)
	for grp in filter_only_groups(nodes):
		filter_node_class_recursivly(types, grp, collected)
	return collected

def filter_node_class(typ, grp=None):
	if grp == None:
		grp = nuke.thisGroup()
	return nuke.allNodes(typ, grp)

def filter_duplicate_read_nodes(grp = None):
	"""Returns A List Of ReadNodes With Duplicate ReadPath Filtered Out"""
	if grp == None:
		grp = nuke.root()
	# GET A LIST OF NODES OF TYPE READ FROM THE INPUT GROUP
	readNodes = nuke.allNodes("Read",grp)
	# STORAGE CONTAINER FOR FILE PATHS
	readPaths = []
	# STORAGE CONTAINER FOR DUPLACAT READNODES
	dupCollectionSets = []
	# SCAN THROUGH THE LIST OF READ NODES
	# GET THE FILE PATH FOR EACH AND SORT IT
	for n in readNodes:
		path = nuke.filename(n,nuke.REPLACE)
		name = n.fullName()
		readPaths.append(path)
	# SCAN THROUGH THE LIST OFF READ NODES
	for Iter_A in readNodes:
		# GET THE FILE PATH
		pathA = full_file_path(Iter_A)
		# CHECK IF THE PATH APPEARS MORE THAN ONCE
		if readPaths.count(pathA) > 1:
			# TEMP STORAGE CONTAINER FOR DUPLACAT READNODES
			dupCollector = []
			for Iter_B in readNodes:
				# GET THE FILE PATH
				pathB = full_file_path(Iter_B)
				if pathA == pathB:
					dupCollector.append(Iter_B)
			dupCollectionSets.append(dupCollector)
			for Iter_B in dupCollector:
				readNodes.remove(Iter_B)
				fpath = full_file_path(Iter_B)
				readPaths.remove(fpath)
	return readNodes