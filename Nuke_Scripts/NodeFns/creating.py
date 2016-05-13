try:
	import nuke
except ImportError:
	nuke = None
	
import threading
def simple_create_node(fn,name):
	return create_Node(fn,name=name)

def create_Node(fn,**kwargs):
	n = None
	name = kwargs.get("name",None)
	if name is None or not nuke.exists(name):
		n = fn(**kwargs)
	else:
		n = nuke.toNode(name)
	isinstance(n,nuke.Node)
	return n

def threaded_create_Node(fn,name):
	threading.Thread( None, simple_create_node,None,(fn,name) ).start()

def gizmo_to_group_replace(gizmo):
	if isinstance(gizmo,nuke.Node):

		names = gizmo.fullName().split(".")
		
		if len(names) > 1:
			grp = nuke.toNode(".".join(names[:-1]))
		else:
			grp = nuke.root()
		grp.begin()

		x = gizmo.xpos()
		y = gizmo.ypos()
		name = gizmo.name()
		dependent    = gizmo.dependent()
		dependencies = gizmo.dependencies(nuke.INPUTS|nuke.HIDDEN_INPUTS)
		g = gizmo.makeGroup()
		g.setXYpos(x,y)
		for d in dependent:
			d.setInput(0,g)
		for i,d in enumerate(dependencies):
			d.setInput(i,d)
		nuke.delete(gizmo)
		g.setName(name)
		grp.end()
