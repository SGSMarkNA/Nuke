try :
	import nuke
except ImportError:
	nuke = None

def add_knob(node,knb):
	"""will only add the knob to the node if it does not exists"""
	# check if the knob name is allready on the node
	if not knb.name() in node.knobs().keys():
		node.addKnob(knb)
	else:
		knb = node[knb.name()]
	return knb

def knob_exists(node,name):
	return name in node.knobs().keys()