try :
	import nuke
except ImportError:
	nuke = None
	
def reorder_From_left_to_right(nodeList):
	reorderList = []
	while len(nodeList):
		reorderList.append( left_most_node( nodeList))
		nodeList.remove( left_most_node( nodeList))
	return reorderList

def reorder_from_top_to_bottom(nodeList):
	reorderList = []
	while len(nodeList):
		reorderList.append( top_most_node( nodeList))
		nodeList.remove( top_most_node( nodeList))
	return reorderList


def offset_points_list(start,offset,count):
	return [start + offset * i for i in range(count)]

def nodeList_center(nodeList=None):
	if nodeList == None:
		nodeList=nuke.selectedNodes()
	nNodes = len(nodeList)
	x=0
	y=0
	for n in nodeList:
		x += n.xpos()
	for n in nodeList:
		y += n.ypos()
	try:
		return [x/nNodes,y/nNodes]
	except ZeroDivisionError:
		return [0,0]



def distribted_points_from_center(nNodes,xpos=0,ypos=0,Offset=250,direction="x",secondary_offset=300):
	X = xpos
	Y = ypos

	if direction == "x":
		Y += secondary_offset
	else:
		X += secondary_offset

	xoffset = (nNodes * Offset)

	ajustmentOffset = ( Offset / 2)

	xylist = []

	for i in range(nNodes):
		if direction == "x":
			val = ( X - ( xoffset  /  2 ) + (i * Offset) + ajustmentOffset )
			xylist.append((val,Y))
		else:
			val = ( Y - ( xoffset  /  2 ) + (i * Offset) + ajustmentOffset )
			xylist.append((X,val))

	return xylist

def distribted_points_from_node_center(master,nNodes,Offset=250,direction="x",secondary_offset=300):
	X = master.xpos()
	Y = master.ypos()

	if direction == "x":

		Y += secondary_offset
	else:
		X += secondary_offset

	xoffset = (nNodes * Offset)

	ajustmentOffset = ( Offset / 2)

	xylist = []
	for i in range(nNodes):
		if direction == "x":
			val = ( X - ( xoffset  /  2 ) + (i * Offset) + ajustmentOffset )
			xylist.append((val,Y))
		else:
			val = ( Y - ( xoffset  /  2 ) + (i * Offset) + ajustmentOffset )
			xylist.append((X,val))
	return xylist


def right_most_node(listOfNodes):
	if not listOfNodes:
		return None
	activeNode = listOfNodes[0]

	for node in listOfNodes:
		if node.xpos() > activeNode.xpos():
			activeNode = node
	return activeNode

def left_most_node(listOfNodes):
	if not listOfNodes:
		return None
	activeNode = listOfNodes[0]

	for node in listOfNodes:
		if node.xpos() < activeNode.xpos():
			activeNode = node
	return activeNode

def bottom_most_node(listOfNodes):
	if not listOfNodes:
		return None
	activeNode = listOfNodes[0]

	for node in listOfNodes:
		if node.ypos() > activeNode.ypos():
			activeNode = node
	return activeNode

def top_most_node(listOfNodes):
	if not listOfNodes:
		return None
	activeNode = listOfNodes[0]

	for node in listOfNodes:
		if node.ypos() < activeNode.ypos():
			activeNode = node
	return activeNode

def top_left_point(listOfNodes):
	if not listOfNodes:
		return (0,0)
	y = top_most_node(listOfNodes).ypos()
	x = left_most_node(listOfNodes).xpos()
	return (x,y)

def top_right_point(listOfNodes):
	if not listOfNodes:
		return (0,0)
	y = top_most_node(listOfNodes).ypos()
	x = right_most_node(listOfNodes).xpos()
	return (x,y)

def bottom_left_point(listOfNodes):
	if not listOfNodes:
		return (0,0)
	y = bottom_most_node(listOfNodes).ypos()
	x = left_most_node(listOfNodes).xpos()
	return (x,y)

def bottom_right_point(listOfNodes):
	if not listOfNodes:
		return (0,0)
	y = bottom_most_node(listOfNodes).ypos()
	x = right_most_node(listOfNodes).xpos()
	return (x,y)

def calculate_bounds(selNodes):
	# Calculate bounds for the backdrop node.
	bdX = min([node.xpos() for node in selNodes])
	bdY = min([node.ypos() for node in selNodes])
	bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
	bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY

	# Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
	left, top, right, bottom = (-10, -80, 10, 10)
	bdX += left
	bdY += top
	bdW += (right - left)
	bdH += (bottom - top)

	# Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
	#left, top, right, bottom = (-50, -50, 50, 50)
	#bdX += left
	#bdY += top
	#bdW += (right - left)
	#bdH += (bottom - top)
	return bdX,bdY,bdW,bdH

def vertically_stack_node_list(node_list,offset=100,sort_by_name=True, x=None,y=None):
	nodes = node_list
	if sort_by_name:
		nodes = sort_nodelist_by_name(nodes)
		
	n = left_most_node(nodes)
	
	if x is None:
		x = n.xpos()
	if y is None:
		y = n.ypos()

	for i in range(0,len(node_list)):
		node_list[i].setXYpos( x, y + ( offset * i ) )

def sort_nodelist_by_name(node_list):
	node_names = sorted([n.fullName() for n in node_list])

	sorteded_node_list = []

	while len(node_names):

		node_name = node_names.pop(0)

		for n in node_list:

			if node_name == n.fullName():

				sorteded_node_list.append(n)
				
				continue
	
	return sorteded_node_list
