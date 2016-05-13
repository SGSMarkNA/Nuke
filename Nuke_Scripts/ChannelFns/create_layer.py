try:
	import nuke
except ImportError:
	nuke = None

def create_channel_layer(layer_name):
	expression = "add_layer {%s" % layer_name
	for color in ".red .green .blue .alpha".split():
		expression += " %s" % color
	expression += "}"
	nuke.tcl(expression)