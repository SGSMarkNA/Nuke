try :
	import nuke
except ImportError:
	nuke = None
	
def display_knobs():
	nod = nuke.selectedNode()
	
	res =  "Node Name = %s(%s)\n" % (nod.name(),nod.Class())
	res += "Knob Count = %i\n" % nod.numKnobs()
	for key,val in nod.knobs().items():
		res += "-"*60
		res +="\n"
		res  += "%s :: %s :: %s\n" % (key,val.Class(),repr(val.value()))
	return res

def knob_infoviewer():
	nuke.display("Scripts.KnobFns.info.display_knobs()",None)