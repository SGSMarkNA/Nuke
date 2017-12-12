import nuke
from _nukemath import Vector2 as VEC2
from functools import wraps

clear_selection  = lambda : not all([node.setSelected(False) for node in nuke.selectedNodes()])
delete_nodes     = lambda node_list: [nuke.delete(node) for node in node_list]
Select_Replace_Nodes   = lambda node_list:[node.setSelected( node in node_list ) for node in nuke.allNodes()]
Find_Cloned_Groups = lambda id_tag_value: [n for n in [n for n in nuke.allNodes("Group") if n.knobs().has_key("clone_id_tag")] if int(n.knob("clone_id_tag").value()) == id_tag_value]


def Get_Node_Offset(A,B):
	A_Xvec = VEC2(A.xpos(),0)
	B_Xvec = VEC2(B.xpos(),0)

	A_Yvec = VEC2(A.ypos(),0)
	B_Yvec = VEC2(B.ypos(),0)

	x = A_Xvec.distanceBetween(B_Xvec)
	y = A_Yvec.distanceBetween(B_Yvec)

	offset = VEC2(x,y)
	return offset

def Create_Offset_Dict(master):
	data_dict = dict()
	for item in Get_Dependent_Nodes(master):
		if not item.Class()=="Output":
			data_dict[item] = Get_Node_Offset(master,item)
	return data_dict

def Apply_Offset_Dict(master,offset_dict):
	v1 = VEC2(master.xpos(),master.ypos())
	for n,v in offset_dict.items():
		v = v1 + v
		n.setXYpos(int(v.x),int(v.y))

def Get_Pipe_End_Node(node):
	if not len(node.dependent(nuke.INPUTS)):
		return node
	else:
		for n in node.dependent(nuke.INPUTS):
			return Get_Pipe_End_Node(n)

def Get_Pipe_Start_Node(node):
	if not len(node.dependencies(nuke.INPUTS)):
		return node
	else:
		for n in node.dependencies(nuke.INPUTS):
			return Get_Pipe_Start_Node(n)

def Get_Dependent_Nodes(node):
	res = node.dependent(nuke.INPUTS)
	for dependent in res:
		items = Get_Dependent_Nodes(dependent)
		for item in items:
			if not item in res:
				res.append(item)
	return res

def Set_Clone_Clipboard(master_node):
	Start_Node = master_node
	isinstance(Start_Node,nuke.Node)
	Node_List_To_Clone = Get_Dependent_Nodes(Start_Node)
	Select_Replace_Nodes(Node_List_To_Clone)
	nuke.cloneSelected("copy")
	return Node_List_To_Clone

#----------------------------------------------------------------------
def delete_G_CORECTIONS_Nodes():
	res = []
	for node in nuke.allNodes("Group"):
		if node.name().startswith("AASYS_CLONED_CORECTIONS"):
			nuke.delete(node)

#----------------------------------------------------------------------
def Clear_Global_Correction_Node_Group(clone_group):
	clear_selection()
	grp_input   = nuke.allNodes("Input",clone_group)[0]
	grp_output  = nuke.allNodes("Output",clone_group)[0]

	grp_output.setInput(0,grp_input)
	old_nodes = [n for n in clone_group.nodes() if not n in [grp_input,grp_output]]
	delete_nodes(old_nodes)
	
#----------------------------------------------------------------------
def Rebuild_Global_Correction_Node_Group(clone_group):
	clear_selection()
	grp_input   = nuke.allNodes("Input",clone_group)[0]
	grp_output  = nuke.allNodes("Output",clone_group)[0]
	
	with clone_group:
		nuke.nodePaste("%clipboard%")
	
	start_node  = Get_Pipe_Start_Node(clone_group.selectedNode())
	end_node    = Get_Pipe_End_Node(clone_group.selectedNode())

	grp_output.setInput(0,end_node)
	start_node.setInput(0,grp_input)
	offset_data = Create_Offset_Dict(start_node)
	start_node.setXYpos(grp_input.xpos(),grp_input.ypos()+30)
	Apply_Offset_Dict(start_node, offset_data)
	grp_output.setXYpos(end_node.xpos(),end_node.ypos()+30)

#----------------------------------------------------------------------
def make_Global_Correction_Node_Group(master_node):
	clear_selection()

	clone_group = nuke.makeGroup(show=False)
	id_tag_knob = nuke.Int_Knob("clone_id_tag")
	id_tag_knob.setValue(int(master_node.knob("clone_id_tag").value()))
	clone_group.addKnob(id_tag_knob)

	grp_input   = nuke.allNodes("Input",clone_group)[0]
	grp_output  = nuke.allNodes("Output",clone_group)[0]

	with clone_group:
		nuke.nodePaste("%clipboard%")
	
	start_node  = Get_Pipe_Start_Node(clone_group.selectedNode())
	end_node    = Get_Pipe_End_Node(clone_group.selectedNode())
	
	grp_output.setInput(0,end_node)
	start_node.setInput(0,grp_input)
	offset_data = Create_Offset_Dict(start_node)
	start_node.setXYpos(grp_input.xpos(),grp_input.ypos()+30)
	Apply_Offset_Dict(start_node, offset_data)
	grp_output.setXYpos(end_node.xpos(),end_node.ypos()+30)
	return clone_group

#----------------------------------------------------------------------
def assign_Clone_Group_To_Node(clone_group,node,master_node):
	placement = master_node.knob("clone_placement").value()
	dependent_nodes    = node.dependent(nuke.INPUTS)
	dependencies_nodes = node.dependencies(nuke.INPUTS)
	if placement == "Below":
		clone_group.setXpos(node.xpos())
		clone_group.setYpos(node.ypos()+int(master_node.knob("clone_offset").value()))
	else:
		clone_group.setXpos(node.xpos())
		clone_group.setYpos(node.ypos()+int(master_node.knob("clone_offset").value() * -1))
	if placement == "Below":
		for dependent in dependent_nodes:
			input_num = dependent.dependencies(nuke.INPUTS).index(node)
			dependent.setInput(input_num,None)
			dependent.setInput(input_num,clone_group)
		clone_group.setInput(0,node)
	else:
		for dependencie in dependencies_nodes:
			input_num = dependencie.dependent(nuke.INPUTS).index(node)
			clone_group.connectInput(0,dependencie)
		#node.setInput(0,None)
		node.setInput(0,clone_group)
	#clone_group.setInput(0,node)

#----------------------------------------------------------------------
def make_Global_Correction_Groups(master_node):
	with nuke.root():
		selected_nodes = nuke.selectedNodes()
	Set_Clone_Clipboard(master_node)
	for node in selected_nodes:
		if not node == master_node:
			clone_group = make_Global_Correction_Node_Group(master_node)
			assign_Clone_Group_To_Node(clone_group,node,master_node)
			
			
#----------------------------------------------------------------------
def Rebuild_Global_Correction_Groups(master_node):
	with nuke.root():
		clone_groups = Find_Cloned_Groups(int(master_node.knob("clone_id_tag").value()))
	Set_Clone_Clipboard(master_node)
	for clone_group in clone_groups:
		if not clone_group == master_node:
			Clear_Global_Correction_Node_Group(clone_group)
			Rebuild_Global_Correction_Node_Group(clone_group)

#----------------------------------------------------------------------
def Select_Global_Correction_Groups(master_node):
	with nuke.root():
		clone_groups = Find_Cloned_Groups(int(master_node.knob("clone_id_tag").value()))
	if master_node in clone_groups:
		clone_groups.remove(master_node)
	Select_Replace_Nodes(clone_groups)


