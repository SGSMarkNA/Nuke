try :
	import nuke
except ImportError:
	nuke = None
	
def auto_crop(first=None, last=None, inc=None, layer="a", views=None, Read_Overides=True, nodes=None, grp=None):
	"""Run the CurveTool's AutoCrop function on each selected node over the
	specified frame range and channels. If the range values are None, the
	project first_frame and last_frame are used; if inc is None, 1 is used.
	After execution, the CurveTool AutoCrop results are copied into a Crop
	node attached to each selected node."""
	# Sort out execute range
	root = nuke.root()
	if grp is None:
		grp = nuke.thisGroup()
	if nodes is None:
		with grp:
			nodes = nuke.selectedNodes()
	if first is None:
		first = int(root.knob("first_frame").value())
	if last is None:
		last = int(root.knob("last_frame").value())
	if inc is None:
		inc = 1
	if views is None:
		if "main" in nuke.views():
			views = ["main"]
		else:
			views = [nuke.views()[0]]
	F_ranges = nuke.FrameRanges()
	F_ranges.add(nuke.FrameRange(first,last,inc))
	# Remember original set of selected nodes...we'll need this
	original_nodes = nodes
	croped_nodes   = []
	# Deselect everything so we can add CurveTool nodes
	with grp:
		all_nodes = nuke.allNodes()
		for i in all_nodes:
			i.knob("selected").setValue(False)

		for i in original_nodes:

			read_buffer = None
			if i.Class() in ["Read","Input"]:
				if i.Class() == "Read":
					read_buffer = i
				else:
					check = nuke.toNode(".".join(i.fullName().split(".")[:-1])).input(0)
					if check.Class() == "Read":
						read_buffer = check


			# Reselect originally selected nodes and create a CurveTool node,
			# which will automatically connect to the last selected.
			i.knob("selected").setValue(True)
			autocropper = nuke.createNode("CurveTool",'''name autoCropCurve operation 0 ROI {0 0 input.width input.height} Layer %s label "Processing Crop..." selected true''' % (str(layer), ), False)
			on_error = None
			if not read_buffer is None:
				on_error = read_buffer["on_error"].value()
				read_buffer["on_error"].setValue('nearest frame')

			if not read_buffer is None and Read_Overides:
				# Execute the CurveTool node thru Read Node frame Range
				start,end = read_buffer["first"].value(), read_buffer["last"].value()
				R_ranges = nuke.FrameRanges()
				R_ranges.add(nuke.FrameRange(start,end,inc))
				nuke.executeMultiple([autocropper,], R_ranges,views)
			else:
				# Execute the CurveTool node thru all the frames
				nuke.executeMultiple([autocropper,], F_ranges,views)

			if not read_buffer is None:
				read_buffer["on_error"].setValue(on_error)    
			# select the curvewriter
			autocropper.setSelected(True)

			# add crop node
			cropnode = nuke.createNode("Crop", "name Master_Auto_Crop label AutoCrop", False)

			# put the new data from the autocrop into the new crop
			cropbox = cropnode.knob("box");
			autocropbox = autocropper.knob("autocropdata");

			cropbox.copyAnimations(autocropbox.animations())

			# turn on the animated flag
			cropnode.knob("indicators").setValue(1)

			for anim in cropbox.animations():
				anim.changeInterpolation(anim.keys(),nuke.CONSTANT)

			# deselect everything
			all_nodes = nuke.allNodes()
			for j in all_nodes:
				j.knob("selected").setValue(False)

			# select the curvewriter and delete it
			autocropper.knob("selected").setValue(True)

			# delete the autocropper to make it all clean
			nuke.delete(nuke.selectedNode())

			# deselect everything
			all_nodes = nuke.allNodes()
			for j in all_nodes:
				j.knob("selected").setValue(False)

			# select the new crop
			cropnode.knob("selected").setValue(True)

			# place it in a nice spot
			nuke.autoplace(cropnode)

			# De-Select it
			cropnode.knob("selected").setValue(False)

			#knb = nuke.Int_Knob("cropoffset","Crop Offset")

			#knb.setValue(4)

			#cropnode.addKnob(knb)

			box = cropnode.knob("box")
			x_A, y_A, r_A, t_A = box.animations()
			removeable_indices = []
			for i in range(x_A.size()):
				x_K = x_A.keys()[i]
				y_K = y_A.keys()[i]
				r_K = r_A.keys()[i]
				t_K = t_A.keys()[i]
				if int(abs(x_K.y))==0 and int(abs(y_K.y))==0 and int(abs(r_K.y))==0 == int(abs(t_K.y))==0:
					x_K.y = 0.0
					y_K.y = 0.0
					r_K.y = 0.5
					t_K.y = 0.5
			
			#for crv in box.animations():
				#if crv.knobIndex() <= 1:
					#crv.setExpression('curve - 2')
				#else:
					#crv.setExpression('curve + 2')

			croped_nodes.append(cropnode)
	return croped_nodes
#===============================================================================
def auto_crop_selected():
	nodes = nuke.selectedNodes()
	for n in nuke.allNodes():
		n.setSelected(False)
	for n in nodes:

		auto_crop()

		for n in nuke.selectedNodes():
			n.setSelected(False)