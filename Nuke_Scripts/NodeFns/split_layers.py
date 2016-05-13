
try:
	import nuke
except ImportError:
	nuke = None
	
from Nuke_Scripts.NodeGraphFns import selecting, placement
from Nuke_Scripts.NodeFns import croping
import os

def None_To_Selected(val):
	"""Simple Function That Checks If the Input arg val == None or is not instance of nuke.Node set The val to the last selected node"""
	if not isinstance(val,nuke.Node) or val == None: val = nuke.selectedNode()
	return val


def get_node_layers_dict(node=None):
	if node is None:
		node = nuke.selectedNode()
	res = {}

	channels = node.channels()

	layers = sorted(list(set([ch.split( '.' )[0] for ch in channels])))

	for layer in layers:
		channalSet = set()
		for each in channels:
			layer_name,channel_name = each.split( '.' )
			if layer_name == layer:
				channalSet.add(channel_name)
		res[layer]=sorted(list(channalSet))
	return res

def get_node_layers_dict_catagorized(node=None):
	bit_32_types = "point normalworld depth".split()
	bit_16_types = "rgba diffuse warmcool refraction specular clay reflection occ reflectionBeauty beauty fresnel".split()

	catagorized_channels = {'rgb':{}, 'rgba':{}, 'alpha':{}, 'depth':{}, 'motion':{}, 'forward':{}, 'backward':{},'mask':{}, 'deep':{}}

	catagorized_layers  = dict(util={} , beauty={}, mask={},other={})

	layers = get_node_layers_dict(G_node)
	for layer,channel in layers.items():
		if layer.lower ()in bit_32_types:
			catagorized_layers["util"][layer]=channel
		elif layer.lower() in bit_16_types:
			catagorized_layers["beauty"][layer]=channel
		elif "matte".lower() in layer.lower():
			catagorized_layers["mask"][layer]=channel
		else:
			catagorized_layers["other"][layer]=channel

	return catagorized_layers


def split_layers(node=None):

	def make_Extract_Group(node):
		if nuke.exists(node.name()+"_Exr_Extracted_Layers"):
			return nuke.toNode(node.name()+"_Exr_Extracted_Layers")
		else:
			return nuke.nodes.Group(name=node.name()+"_Exr_Extracted_Layers")

	Shuffle_node_List1 = []
	Shuffle_node_List2 = []
	Write_Node_List    = []
	node = None_To_Selected(node)
	NodeGraphFns.selecting.deselect_everything()
	grp = None
	
	grp = make_Extract_Group(node)

	inputNode = None
	with grp:
		croping.auto_crop
		inputNode = nuke.nodes.Input()
		nuke.createNode("Output","",False)
	grp.setInput(0,node)

	oldNode = node
	if node.Class() == "Input":
		oldNode  = node
		node = nuke.toNode("".join(node.fullName().split(".")[0:-1])).input(0)

	layerDic = get_node_layers_dict(node)

	write_32bit_prefs = 'channels %s file_type exr datatype "%i bit float"'
	shuffleCopy = None
	with grp:
		for layer,chans in layerDic.items():
			shuffle_name  = layer+"_Shuffle"
			write_name    = layer+"_Write"

			shuffle_prefs = "name %s_Shuffle in %s" % (shuffle_name,layer)
			write_prefs = ""
			if not nuke.exists(shuffle_name):
				if len(chans) == 1:

					if chans[0].lower() == "alpha":
						shuffle_prefs += ' out rgba red black green black blue black alpha red'
						write_prefs   += write_32bit_prefs % ("rgba",16)

					elif chans[0].lower() == "z":
						shuffle_prefs += ' out rgba'
						write_prefs   += write_32bit_prefs % ("rgba",32)

				elif len(chans) == 2:
					shuffle_prefs += ' out rgba'
					write_prefs   += write_32bit_prefs % ("rgba",32)

				elif len(chans) == 3:
					shuffle_prefs += ' out rgba'
					write_prefs   += write_32bit_prefs % ("rgba",32)

				elif len(chans) == 4:
					shuffle_prefs += ' out rgba'
					write_prefs   += write_32bit_prefs % ("rgba",32)

				shuffle = nuke.createNode( 'Shuffle', shuffle_prefs, inpanel=False )
				shuffle.setInput(0,inputNode)
				shuffle.setName(shuffle_name)

				write = nuke.createNode( 'Write', write_prefs, inpanel=False )
				write.setInput(0,shuffle)
				write.setName(write_name)
				
				write["use_limit"].setValue(False)
				write["autocrop"].setValue(False)
				#write["datatype"].setValue('16 bit half')

				#write["reading"].setExpression("%s.read_file" % grp.fullName())
				#write["checkHashOnRead"].setExpression("%s.read_file" % grp.fullName())

				fname   = nuke.filename(node)

				dirname = os.path.dirname(fname)

				fpath = dirname + "/layers/" + layer + "/" + layer + ".##.exr"
				#try:
					#os.makedirs(dirname + "/layers/" + layer)
				#except WindowsError:
					#pass

				write.knob("file").setValue(fpath)
				if shuffleCopy == None:
					shuffleCopy = nuke.createNode( 'Shuffle', "", inpanel=False )
					shuffleCopy.connectInput(0,write)
					if chans[0].lower() == "alpha" and len(chans)==1:
						shuffleCopy.knob("in").fromScript("alpha")
						shuffleCopy.knob("red").fromScript("red")
					elif chans[0].lower() == "depth" and len(chans)==1:
						shuffleCopy.knob("in").fromScript("rgba")
						shuffleCopy.knob("red").fromScript("red")
					else:
						shuffleCopy.knob("in").setValue(shuffle["out"].value())

					shuffleCopy.knob("out").setValue(shuffle["in"].value())
				else:
					tnod = nuke.createNode( 'ShuffleCopy', "", inpanel=False )
					tnod.setInput(0,shuffleCopy)
					tnod.setInput(1,write)
					if chans[0].lower() == "alpha" and len(chans)==1:
						tnod.knob("in").setValue("alpha")
						tnod.knob("red").fromScript("red")
					else:
						tnod.knob("in").setValue(shuffle["out"].value())
					tnod.knob("out").setValue(shuffle["in"].value())
					tnod.knob("in2").setValue(shuffleCopy["out2"].value())
					tnod.knob("out2").setValue(shuffleCopy["in2"].value())

					if len(chans)== 4:
						tnod.knob("red").fromScript("red")
						tnod.knob("green").fromScript("green")
						tnod.knob("blue").fromScript("blue")
						tnod.knob("alpha").fromScript("alpha")
					elif len(chans)== 3:
						tnod.knob("red").fromScript("red")
						tnod.knob("green").fromScript("green")
						tnod.knob("blue").fromScript("blue")
					elif len(chans)== 2:
						tnod.knob("red").fromScript("red")
						tnod.knob("green").fromScript("green")
					elif len(chans)== 1:
						tnod.knob("red").fromScript("red")
					shuffleCopy  = tnod
					isinstance(shuffleCopy,nuke.Node)

				shuffleCopy.setXYpos(write.xpos(),write.ypos()+250)
				write.setYpos(shuffle.ypos()+100)
				shuffleCopy.setName(layer+"_Shuffle_Copy")
			Shuffle_node_List1.append(nuke.toNode(shuffle_name))
			Shuffle_node_List2.append(nuke.toNode(layer+"_Shuffle_Copy"))
			Write_Node_List.append(nuke.toNode(write_name))

		center = NodeGraphFns.placement.nodeList_center(Write_Node_List)
		inputNode.setXYpos(center[0],center[1]-300)
		node.setSelected(True)
		opnode = nuke.allNodes("Output",nuke.thisGroup())
		if len(opnode):
			opnode = opnode[0]
		if isinstance(opnode,nuke.Node):
			opnode.setInput(0,Shuffle_node_List2[-1])
			opnode.setXYpos(Shuffle_node_List2[-1].xpos(),Shuffle_node_List2[-1].ypos()+200)