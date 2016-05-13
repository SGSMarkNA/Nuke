try:
	import nuke
except ImportError:
	nuke = None
	
def get_knob_values(knob_name,nodes=None):
	if nodes is None:
		nodes = nuke.selectedNodes()
	values = [n.knob(knob_name).value() for n in nodes if knob_name in n.knobs().keys()]
		

def all_node_info():
	this = nuke.toNode("this")
	knobdata = this.writeKnobs(nuke.TO_SCRIPT)
	knobdata = re.sub("}", "", knobdata)
	knobdata = re.sub(" {", "", knobdata)
	knobdata = re.sub("{", "", knobdata)
	output = "Node Info for : " + this.fullName()
	output += "\n" + nuke.showInfo()
	output += " -- \nKnob Info:"
	output += "\n\t" + knobdata

	classname = this.Class()
	if classname == "Read" or classname == "Write":
		fileknob = this.knob("file").value()
		proxyknob = this.knob("proxy").value()

	# fileknob and proxyknob can be None object
	# set to empty string in order to avoid any exception
	if fileknob == None:
		fileknob = ""

	if proxyknob == None:
		proxyknob = ""

	output += "\n\nFile Info:"
	output += "\n\tFull Res Path : \n\t\t" + fileknob
	output += "\n\n\tProxy Res Path : \n\t\t" + proxyknob
	output += "\n --"
	output += "\n\tFull Res File : \n\t\t" + os.path.basename(fileknob)
	output += "\n\n\tProxy Res File : \n\t\t" + os.path.basename(proxyknob)
	return output