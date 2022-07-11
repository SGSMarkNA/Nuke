import nuke
import os
from _nukemath import Vector2 as VEC2
from functools import wraps
clear_selection  = lambda : not all([node.setSelected(False) for node in nuke.allNodes()])
delete_nodes     = lambda node_list: [nuke.delete(node) for node in node_list]
Select_Replace_Nodes   = lambda node_list:[node.setSelected( node in node_list ) for node in nuke.allNodes()]
Find_Cloned_Groups = lambda id_tag_value: [n for n in [n for n in nuke.allNodes("Group") if "clone_id_tag" in n.knobs()] if int(n.knob("clone_id_tag").value()) == id_tag_value]
_Global_UnClonable_Node_Types = ["Roto","RotoPaint","Group","Dot"]
#===============================================================================
def find_upstream_node( matchclass=None, startnode=None ):
	"""
	In the simplest way possible, this function will go upstream and find
	the first node matching the specified class.
	"""

	if matchclass == None:
		return None
	elif startnode == None:
		return None
	elif  startnode.Class() == matchclass:
		return startnode
	else:
		for node in startnode.dependencies(nuke.INPUTS):
			val = find_upstream_node( matchclass=matchclass, startnode=node )
			if val is not None:
				return val

#===============================================================================
def up_stream_nodes(nodes=None,nlist=None,stop_node=None):
	if nlist == None:
		nlist = []
	if nodes == None:
		nodes = nuke.selectedNodes()
	elif isinstance(nodes,nuke.Node):
		up_stream_nodes(nodes.dependencies(),nlist,stop_node)
	if isinstance(nodes,list):
		for n in nodes:
			if not n == stop_node and not stop_node in n.dependent():
				nlist.append(n)
				if n.inputs():
					up_stream_nodes(n.dependencies(nuke.INPUTS),nlist,stop_node)
	return nlist

def filter_Out_Cloneable_Nodes(node_list):
	res = [n for n in node_list if n.Class() in _Global_UnClonable_Node_Types]
	return res

def filter_Out_Non_cloneable_Nodes(node_list):
	res = [n for n in node_list if not n.Class() in _Global_UnClonable_Node_Types]
	return res

#----------------------------------------------------------------------
def disconnect_All_Dependent(node):
	for n in node.dependent():
		for i in range(n.inputs()):
			if n.input(i) == node:
				n.setInput(i,None)
#----------------------------------------------------------------------
def disconnect_All_Dependencies(node):
	""""""
	while len(node.dependencies()):
		for i in range(node.inputs()):
			node.setInput(i, None)

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
	for item in Get_Nodes_To_Clone(master):
		if not item.Class()=="Output":
			data_dict[item] = Get_Node_Offset(master,item)
	return data_dict

def Create_Clone_Group_Offset_Dict(clone_group,start_node):
	data_dict = dict()
	for item in clone_group.nodes():
		if not item.Class()=="Output" and not item.Class()== "Input":
			data_dict[item] = Get_Node_Offset(start_node,item)
	return data_dict

def Apply_Offset_Dict(master,offset_dict):
	v1 = VEC2(master.xpos(),master.ypos())
	for n,v in list(offset_dict.items()):
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

#===============================================================================
def Get_Nodes_To_Clone(master_node):
	up_stream_node_list = []
	stop_node_name = master_node.knobs()["Assigned_Clone_Stop_Link"].getLink()
	if stop_node_name is not None and not stop_node_name == "":
		stop_node_name = stop_node_name.replace(".name","")
		if nuke.exists(stop_node_name):
			stop_node = nuke.toNode(stop_node_name)
			up_stream_node_list = up_stream_nodes(stop_node,[],master_node)
			up_stream_node_list.append(stop_node)
	return filter_Out_Non_cloneable_Nodes(up_stream_node_list)

#===============================================================================
def Get_Nodes_To_Duplicate(master_node,from_Node_list=[]):
	if len(from_Node_list):
		return filter_Out_Cloneable_Nodes(from_Node_list)
	else:
		up_stream_node_list = []
		stop_node_name = master_node.knobs()["Assigned_Clone_Stop_Link"].getLink()
		if stop_node_name is not None and not stop_node_name == "":
			stop_node_name = stop_node_name.replace(".name","")
			if nuke.exists(stop_node_name):
				stop_node = nuke.toNode(stop_node_name)
				up_stream_node_list = up_stream_nodes(stop_node,[],master_node)
				up_stream_node_list.append(stop_node)
		return filter_Out_Cloneable_Nodes(up_stream_node_list)


def Get_Dependent_Nodes(node):
	res = node.dependent(nuke.INPUTS)
	for dependent in res:
		items = Get_Dependent_Nodes(dependent)
		for item in items:
			if not item in res:
				res.append(item)
	return res

def Assign_Stop_Node(master_node,stop_node):
	name_knb = stop_node.knob("name")    
	master_node.knobs()["Assigned_Clone_Stop_Link"].makeLink(stop_node.fullName(),name_knb.name())

def Set_Clone_Clipboard(master_node):
	Node_List_To_Clone = Get_Nodes_To_Clone(master_node)
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
def apply_clone_placement(master_node,clone_group):
	""""""
	grp_input   = nuke.allNodes("Input",clone_group)[0]
	grp_output  = nuke.allNodes("Output",clone_group)[0]
	for item in clone_group.nodes():
		if not item.Class()=="Output" and not item.Class()== "Input":
			real_item = nuke.toNode(item.name())
			item.setXYpos(real_item.xpos(),real_item.ypos())
	grp_input.setXYpos(grp_input.dependent(nuke.INPUTS)[0].xpos(),grp_input.dependent(nuke.INPUTS)[0].ypos()-100)
	grp_output.setXYpos(grp_output.dependencies(nuke.INPUTS)[0].xpos(),grp_output.dependencies(nuke.INPUTS)[0].ypos()+100)
#----------------------------------------------------------------------
def Rebuild_None_Cloneable_Nodes(master_node,clone_group):
	""""""
	def connect_clone_from_real(real_node,cloned_version,clone_group):
		for real_dependent in real_node.dependent():
			for i in range(real_dependent.inputs()):
				real_dependent_input_node = real_dependent.input(i)
				if real_dependent_input_node == real_node:
					clone_dependent = clone_group.node(real_dependent.name())
					clone_dependent.setInput(i,cloned_version)
		for real_dependencie in real_node.dependencies():
			for real_dependencie_dependent in real_dependencie.dependent():
				if real_dependencie_dependent == real_node:
					clone_dependencie = clone_group.node(real_dependencie.name())
					cloned_version.connectInput(0,clone_dependencie)
	
	for clone_node in filter_Out_Cloneable_Nodes(clone_group.nodes()):
		disconnect_All_Dependencies(clone_node)
		disconnect_All_Dependent(clone_node)
		nuke.delete(clone_node)
	
	nodes_to_dup = Get_Nodes_To_Duplicate(master_node)	
	if len(nodes_to_dup):		
		Select_Replace_Nodes(nodes_to_dup)
		nuke.nodeCopy('%clipboard%')
		clear_selection()
		#for node in nodes_to_dup:
			#cloned_version = clone_group.node(node.name())
			#if cloned_version is not None:
				#if placement_dict.has_key(cloned_version.name()):
					#values = placement_dict[cloned_version.name()]
					#cloned_version.setXYpos(values[0],values[1])
		
		with clone_group:
			clear_selection()
			nuke.nodePaste('%clipboard%')
			clear_selection()
			
		for real_node in nodes_to_dup:
			cloned_version = clone_group.node(real_node.name())
			connect_clone_from_real(real_node,cloned_version,clone_group)
#----------------------------------------------------------------------
def Rebuild_Global_Correction_Node_Group(master_node,clone_group):
	clear_selection()
	grp_input   = nuke.allNodes("Input",clone_group)[0]
	grp_output  = nuke.allNodes("Output",clone_group)[0]

	with clone_group:
		nuke.nodePaste("%clipboard%")
		clear_selection()
	master_node_start  = master_node.dependent()[0].name()
	start_node = [n for n in clone_group.nodes() if n.name() == master_node_start][0]
	master_node_end = master_node.knobs()["Assigned_Clone_Stop_Link"].getLink().replace(".name","")
	end_node = [n for n in clone_group.nodes() if n.name() == master_node_end][0]

	#start_node  = Get_Pipe_Start_Node(clone_group.selectedNode())
	#end_node    = Get_Pipe_End_Node(clone_group.selectedNode())

	grp_output.setInput(0,end_node)
	start_node.setInput(0,grp_input)
#----------------------------------------------------------------------
def make_Global_Correction_Node_Group(master_node):
	clear_selection()
	clone_group = nuke.makeGroup(show=False)
	id_tag_knob = nuke.Int_Knob("clone_id_tag")
	id_tag_knob.setValue(int(master_node.knob("clone_id_tag").value()))
	clone_group.addKnob(id_tag_knob)
	Rebuild_Global_Correction_Node_Group(master_node, clone_group)
	return clone_group
#----------------------------------------------------------------------
def assign_Clone_Group_To_Node(clone_group,node,master_node):
	placement = master_node.knob("clone_placement").value()
	dependent_nodes    = node.dependent(nuke.INPUTS)
	dependencies_nodes = node.dependencies(nuke.INPUTS)
	if placement == "Below Selected":
		clone_group.setXpos(node.xpos())
		clone_group.setYpos(node.ypos()+int(master_node.knob("clone_offset").value()))
	else:
		clone_group.setXpos(node.xpos())
		clone_group.setYpos(node.ypos()+int(master_node.knob("clone_offset").value() * -1))
	if placement == "Below Selected":
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
			Set_Clone_Clipboard(master_node)
			clone_group = make_Global_Correction_Node_Group(master_node)
			assign_Clone_Group_To_Node(clone_group,node,master_node)
			Rebuild_None_Cloneable_Nodes(master_node,clone_group)
			apply_clone_placement(master_node, clone_group)
			clear_selection()
#----------------------------------------------------------------------
def Rebuild_Global_Correction_Groups(master_node,only_Non_Cloneable=False):
	with nuke.root():
		clone_groups = Find_Cloned_Groups(int(master_node.knob("clone_id_tag").value()))
	Set_Clone_Clipboard(master_node)
	for clone_group in clone_groups:
		if not clone_group == master_node:
			Set_Clone_Clipboard(master_node)
			if not only_Non_Cloneable:
				Clear_Global_Correction_Node_Group(clone_group)
				Rebuild_Global_Correction_Node_Group(master_node,clone_group)
			Rebuild_None_Cloneable_Nodes(master_node,clone_group)
			apply_clone_placement(master_node, clone_group)
#----------------------------------------------------------------------
def Select_Global_Correction_Groups(master_node):
	with nuke.root():
		clone_groups = Find_Cloned_Groups(int(master_node.knob("clone_id_tag").value()))
	if master_node in clone_groups:
		clone_groups.remove(master_node)
	Select_Replace_Nodes(clone_groups)
#----------------------------------------------------------------------
def _Multi_Clone_On_Create():
	gizmo_node = nuke.thisNode()
	if isinstance(gizmo_node,nuke.Gizmo):
		if int(gizmo_node.knob("clone_id_tag").value()) == 0:
			vals = []
			with nuke.root():
				for node in nuke.allNodes("Multi_Clone_Control"):
					vals.append(int(node.knob("clone_id_tag").value()))
			if len(vals):
				next_val = max(vals)+1
			else:
				next_val = 1
			gizmo_node.knob("clone_id_tag").setValue(next_val)
	else:
		knb = gizmo_node.knobs()["onCreate"]
		knb.clearFlag(nuke.INVISIBLE)
