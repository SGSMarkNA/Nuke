try:
	import nuke
except ImportError:
	nuke = None


###############################
##SuperDot

def superdot():
	# Get selection and de-select everything
	selNodes = nuke.selectedNodes()
	for n in selNodes:
		n['selected'].setValue(False)

	# Store the name of the selected node and select it
	for n in selNodes:
		n['selected'].setValue(True)
		Name = n.name()

		# Create the Dot (like it would be created through the UI)
		sD = nuke.createNode("Dot", inpanel=False)
		sD.setInput(0, n)

		# Enter the stored name into the Name and Label fields of the dot
		sD.setName(Name)
		sD.knob('label').setValue(Name)

		# De-select the node so the next node generation doesn't get confused
		n['selected'].setValue(False)