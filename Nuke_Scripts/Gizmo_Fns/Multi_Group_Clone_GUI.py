from . import Gizmo_UI_Widgets
from . import Multi_Group_Clone_Builder
import os
import nuke
import importlib
class Multi_Group_Clone_Controls(Gizmo_UI_Widgets.UI_Base_Widget_Knob):
	def __init__(self,node,parent=None):
		_ui_foulder = os.path.join(os.path.dirname(__file__), "UI")
		ui_file = os.path.join(_ui_foulder,"Multi_Clone_Control.ui")
		super(Multi_Group_Clone_Controls,self).__init__(node,ui_file,parent)
		self._knb_name_to_att_dict = dict(clone_offset=self.file_wig.Create_Clone_Offset.setValue,
                                          clone_id_tag=self.file_wig.Control_ID_Number.setValue)
		self._update_knobs()
		self.file_wig.Control_ID_Number.editingFinished.connect(self._update_clone_id_tag_knob)
		self.file_wig.Create_Clone_Placement.currentIndexChanged.connect(self._update_clone_placement_knob)
		self.file_wig.Assign_Stop_Node_Button.clicked.connect(self.Assign_Stop_Node)
		self.file_wig.Select_Stop_Node_Button.clicked.connect(self.Select_Stop_Node)
		self.file_wig.Select_Clones_Button.clicked.connect(self.Select_Clones)
		self.file_wig.Create_Clone_Button.clicked.connect(self.make_Global_Correction_Groups)
		self.file_wig.Rebuild_Clones_Button.clicked.connect(self.Rebuild_Global_Correction_Groups)
		self.file_wig.Rebuild_Non_Cloneable_Button.clicked.connect(self.Rebuild_Non_Cloneable)
		self.file_wig.Create_Clone_Offset.valueChanged.connect(self._update_clone_offset_knob)
	## NUKE NODE KNOB UPDATING
	#----------------------------------------------------------------------
	@Gizmo_UI_Widgets.PYQT.Slot()
	def _update_clone_id_tag_knob(self):
		""""""
		self._nuke_node.knob("clone_id_tag").setValue(self.file_wig.Control_ID_Number.value())
	#----------------------------------------------------------------------
	@Gizmo_UI_Widgets.PYQT.Slot()
	def _update_clone_placement_knob(self):
		""""""
		text = self.file_wig.Create_Clone_Placement.currentText()
		self._nuke_node.knob("clone_placement").setValue(str(text))
	#----------------------------------------------------------------------
	@Gizmo_UI_Widgets.PYQT.Slot()
	def _update_clone_offset_knob(self):
		""""""
		val = self.file_wig.Create_Clone_Offset.value()
		self._nuke_node.knob("clone_offset").setValue(int(val))

	## GUI WIDGET UPDATING
	#----------------------------------------------------------------------
	def _set_Clone_Offset_Widget(self):
		""""""
		clone_placement = self._nuke_node.knob("clone_placement")
		index = list(clone_placement.values()).index(clone_placement.value())
		self.file_wig.Create_Clone_Placement.setCurrentIndex(index)
	#----------------------------------------------------------------------
	def _set_Assigned_Clone_Stop_Widget(self):
		""""""
		clone_stop = self._nuke_node.knobs()["Assigned_Clone_Stop_Link"]
		link = clone_stop.getLink()
		if link is not None and link is not "":
			link = link.replace(".name","")
			self.file_wig.Stop_Node_Name.setText(link)
		else:
			self.file_wig.Stop_Node_Name.setText("")
	#----------------------------------------------------------------------
	def _update_knobs(self):
		""""""
		for key,val in self._knb_name_to_att_dict.items():
			knb = self._nuke_node.knob(key)
			val(knb.value())
		self._set_Clone_Offset_Widget()
		self._set_Assigned_Clone_Stop_Widget()

	## INTEGRITY CHECK
	#----------------------------------------------------------------------
	def is_First_Input_Valid(self):
		""""""
		first_input = self._nuke_node.dependent()
		if len(first_input):
			first_input = first_input[0]
			if not first_input.Class() == "Dot":
				return True
			else:
				return False
		else:
			return False
		link = clone_stop.getLink()
		if link is None or link == "":
			return False
		else:
			if nuke.exists(link.replace(".name","")):
				return True
			else:
				return False
	#----------------------------------------------------------------------
	def is_Stop_Node_Valid(self):
		""""""
		clone_stop = self._nuke_node.knobs()["Assigned_Clone_Stop_Link"]
		link = clone_stop.getLink()
		if link is None or link == "":
			return False
		else:
			if nuke.exists(link.replace(".name","")):
				return True
			else:
				return False
	#----------------------------------------------------------------------
	def is_Stop_Node_In_Pipe_Tree(self):
		""""""
		if self.is_Stop_Node_Valid():
			clone_stop = self._nuke_node.knobs()["Assigned_Clone_Stop_Link"]
			link = clone_stop.getLink()
			link_node=nuke.toNode(link.replace(".name",""))
			master = Multi_Group_Clone_Builder.find_upstream_node(self._nuke_node.Class(),link_node)
			if not master == self._nuke_node:
				return False
			else:
				return True
		else:
			return False
	#----------------------------------------------------------------------
	def on_knob_changed(self,knb):
		""""""
		pass
	## GUI BUTTON ACTIONS
	#----------------------------------------------------------------------
	@Gizmo_UI_Widgets.PYQT.Slot()
	def Assign_Stop_Node(self):
		if not len(nuke.selectedNodes()):
			nuke.message("Nothing Is Selected")
		else:
			selected_node = nuke.selectedNode()
			if selected_node == self._nuke_node:
				nuke.message("The Clone Stop Node Can not be set to the master control node")
			else:
				master = Multi_Group_Clone_Builder.find_upstream_node(self._nuke_node.Class(),selected_node)
				if not master == self._nuke_node:
					nuke.message("Can Not Set The Selected Node To Be The Node Stop Because It Is Not Within The Pipe Tree Of the Master Control Node")
				else:
					Multi_Group_Clone_Builder.Assign_Stop_Node(self._nuke_node,selected_node)
					self._set_Assigned_Clone_Stop_Widget()
	#----------------------------------------------------------------------
	def _error_message_stop_node_does_not_exist(self):
		""""""
		nuke.message("Can Not Preform Action Because The Node Assined To The Stop Clone Does Not Exist")
	#----------------------------------------------------------------------
	def _error_message_stop_node_not_in_pipe_tree(self):
		""""""
		nuke.message("Can Not Preform Action Because The Node Stop Is Not Within The Pipe Tree Of the Master Control Node")
	#----------------------------------------------------------------------
	def _error_message_first_input(self):
		""""""
		nuke.message("Can Not Preform Action Because The First Input Of The Master Control Node Can Not Be A Dot Node")
	#----------------------------------------------------------------------
	def get_Stop_Node_Nuke_Node(self):
		""""""
		clone_stop = self._nuke_node.knobs()["Assigned_Clone_Stop_Link"]
		link = clone_stop.getLink()
		link_node=nuke.toNode(link.replace(".name",""))
		return link_node
	#----------------------------------------------------------------------
	@Gizmo_UI_Widgets.PYQT.Slot()
	def Select_Stop_Node(self):
		if not self.is_Stop_Node_Valid():
			self._error_message_stop_node_does_not_exist()
		else:
			stop_node = self.get_Stop_Node_Nuke_Node()
			Multi_Group_Clone_Builder.Select_Replace_Nodes([stop_node])
	#----------------------------------------------------------------------
	@Gizmo_UI_Widgets.PYQT.Slot()
	def Select_Clones(self):
		importlib.reload(Multi_Group_Clone_Builder)
		Multi_Group_Clone_Builder.Select_Global_Correction_Groups(self._nuke_node)
	#----------------------------------------------------------------------
	@Gizmo_UI_Widgets.PYQT.Slot()
	def Rebuild_Global_Correction_Groups(self):
		importlib.reload(Multi_Group_Clone_Builder)
		if not self.is_Stop_Node_Valid():
			self._error_message_stop_node_does_not_exist()
		elif not self.is_Stop_Node_In_Pipe_Tree():
			self._error_message_stop_node_not_in_pipe_tree()
		elif not self.is_First_Input_Valid():
			self._error_message_first_input()
		else:
			Multi_Group_Clone_Builder.Rebuild_Global_Correction_Groups(self._nuke_node)
	#----------------------------------------------------------------------
	@Gizmo_UI_Widgets.PYQT.Slot()
	def Rebuild_Non_Cloneable(self):
		importlib.reload(Multi_Group_Clone_Builder)
		if not self.is_Stop_Node_Valid():
			self._error_message_stop_node_does_not_exist()
		elif not self.is_Stop_Node_In_Pipe_Tree():
			self._error_message_stop_node_not_in_pipe_tree()
		elif not self.is_First_Input_Valid():
			self._error_message_first_input()
		else:
			Multi_Group_Clone_Builder.Rebuild_Global_Correction_Groups(self._nuke_node,True)
		
	#----------------------------------------------------------------------
	@Gizmo_UI_Widgets.PYQT.Slot()
	def make_Global_Correction_Groups(self):
		importlib.reload(Multi_Group_Clone_Builder)
		if not self.is_Stop_Node_Valid():
			self._error_message_stop_node_does_not_exist()
		elif not self.is_Stop_Node_In_Pipe_Tree():
			self._error_message_stop_node_not_in_pipe_tree()
		elif not self.is_First_Input_Valid():
			self._error_message_first_input()
		else:
			Multi_Group_Clone_Builder.make_Global_Correction_Groups(self._nuke_node)