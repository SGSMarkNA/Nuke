try:
	import nuke
	import nukescripts
except ImportError:
	nuke = None
	nukescripts = None


def view_indices():
	viewIndices = dict()
	for i,v in enumerate(nuke.views()):
		viewIndices[v]=i
	return viewIndices

def view_indices2(joinview):
	viewIndices = dict()
	for i,v in enumerate(joinview["viewassoc"].value().splitlines()):
		viewIndices[v]=i
	return viewIndices

def views_connecter(OneViews,joinView):
	views = view_indices()
	for oneview in OneViews:
		if hasattr(oneview,"Class"):
			if oneview.Class() == "OneView":
				knob = oneview.knob("view")
				joinView.setInput(views[knob.value()], oneview)
			elif oneview.Class() ==  'Read_To_Many_Views_Connector':
				view_names = oneview.knob("view_names").value().split()
				if len(view_names):
					for i,v in enumerate(view_names):
						if views.has_key(v):
							joinView.setInput(views[v], oneview)

			elif "views" in oneview.knobs():
				lines = []
				if oneview.knob("views").toScript().startswith("{") and oneview.knob("views").toScript().endswith("}"):
					n = nuke.toNode(oneview.knob("views").toScript().replace("{","").replace("}","").replace(".views",""))
					if not n == None:
						lines = n.knob("views").toScript().split()
					else:
						print oneview.knob("views").toScript()
				else:
					lines = oneview.knob("views").toScript().split()
				if len(lines):
					for i,v in enumerate(lines):
						if i%2 == 0:
							if views.has_key(v):
								joinView.setInput(views[v], oneview)

def connect_oneviews_to_joinview():
	grp = nuke.thisGroup().begin()
	nodes = nuke.selectedNodes()
	ovs = [n for n in nodes if n.Class() == "OneView" or "views" in n.knobs() or "view" in n.knobs() and not n.Class()=="Write"]
	jv = [n for n in nodes if n.Class() == "JoinViews"][0]
	views_connecter(ovs,jv)
	grp.end()

def get_input_view_names(grp=None):
	if grp is None:
		grp = nuke.selectedNode()
	res = dict()
	for index in range(grp.inputs()):
		n = grp.input(index)
		if n.Class() == "OneView":
			res[index]=n['view'].value()
	return res

def get_group_input_dict(grp):
	input_dict = {}
	for item in nuke.allNodes("Input",grp):
		input_dict[int(item.knob("number").value())]=item
	return input_dict

def get_group_joinview_dict(grp):
	jv = nuke.allNodes("JoinViews",grp)[0]
	isinstance(jv,nuke.Node)
	return jv

def set_inner_group_joinview(grp):
	jv = get_group_joinview_dict(grp)
	input_view_dic = get_input_view_names(grp)
	viewIndices = view_indices2(jv)
	input_dict = get_group_input_dict(grp)

	for k,v in input_view_dic.items():
		nodeToconnect = input_dict[k]
		joinview_input_index = viewIndices[v]
		jv.setInput(joinview_input_index, nodeToconnect)

def create_joinview_group(oneview_inputs=None):
	if oneview_inputs is None:
		oneview_inputs = nuke.selectedNodes("OneView")
	if not len(oneview_inputs):
		raise ValueError,"A list of oneview Nodes must be input or selected for this fn to work"
	inputs = []
	oneviews = []
	grp = nuke.nodes.Group()
	grp.begin()
	for i in range(len(oneview_inputs)):
		name = oneview_inputs[i]['view'].value()+"_Input"
		ipn = nuke.nodes.Input(name=name)
		inputs.append(ipn)
		ov = nuke.nodes.OneView(view=oneview_inputs[i]['view'].value(),inputs=[ipn])
		oneviews.append(ov)

	jv = nuke.createNode("JoinViews")
	nuke.nodes.Output(inputs=[jv])
	for i in range(len(oneview_inputs)):
		grp.setInput(i,oneview_inputs[i])
	set_inner_group_joinview(grp)
	grp.end()
	return grp