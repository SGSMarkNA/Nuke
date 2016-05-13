try:
	import nuke
except ImportError:
	nuke = None

#import PyQt4_Callbacks
#from .onCreate import _aw_config_build_type_knb, _aw_config_data_file_knb, _aw_project_type_knb

def Change_AW_Project_Settings():
	if nuke.thisKnob() == _aw_project_type_knb:
		if _aw_project_type_knb.value() == "General":
			for knb in [_aw_config_build_type_knb, _aw_config_data_file_knb]:
				knb.setVisible(False)

			nuke.removeKnobChanged(Trim_Build_Viewer_Gizmo.On_Knob_Changed, (), {}, "Group")

		elif _aw_project_type_knb.value() == "Infiniti Global Configurator":
			for knb in [_aw_config_build_type_knb, _aw_config_data_file_knb]:
				knb.setVisible(True)#if nuke.GUI:
	#nuke.addKnobChanged(Trim_Build_Viewer_Gizmo.On_Knob_Changed, (), {}, "Group")

#nuke.addKnobChanged(Change_AW_Project_Settings, (), {}, "Root")
#nuke.addKnobChanged(PyQt4_Callbacks.Emit_Node_Pos_Changed, (), {})
#nuke.addKnobChanged(PyQt4_Callbacks.Emit_Node_Selection_Changed, (), {})

