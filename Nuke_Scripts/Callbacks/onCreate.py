import nuke
import os
import threading

from Nuke_Scripts.KnobFns.add_remove_update import knob_exists, add_knob


_aw_global_settings_knb    = nuke.Tab_Knob("aw_prj_global_settings", "AW Global Settings")
_aw_project_type_knb       = nuke.Enumeration_Knob("aw_prj_project_type", "AW Project Types", ["General","Infiniti Global Configurator"])
_aw_config_data_file_knb   = nuke.File_Knob("aw_prj_config_data_file", "Global Configurator Data file")
_aw_config_build_type_knb  = nuke.Enumeration_Knob("aw_prj_config_build_type", "Configurator Build Types", ["Interior", "Exterior"])

def add_aw_tracking_knobs():
	idknb = nuke.Int_Knob("aw_node_id_counter")
	userknb = nuke.String_Knob("aw_current_username")
	idknb.setVisible(False)
	userknb.setVisible(False)
	idknb.setValue(1)
	idknb   = add_knob(nuke.root(), idknb)
	userknb = add_knob(nuke.root(), userknb)
	try:
		userknb.setValue(os.environ.get("USERNAME", ""))
	except:
		userknb.setValue("UNKNOWN")

def add_aw_project_type_knob():
	global _aw_global_settings_knb, _aw_project_type_knb, _aw_config_data_file_knb, _aw_config_build_type_knb

	root = nuke.root()
	if not knob_exists(root, _aw_project_type_knb.name()):
		inishalize = True
	else:
		inishalize = False
	_aw_global_settings_knb    = add_knob(root, _aw_global_settings_knb)
	_aw_project_type_knb       = add_knob(root, _aw_project_type_knb)
	_aw_config_data_file_knb   = add_knob(root, _aw_config_data_file_knb)
	_aw_config_build_type_knb  = add_knob(root, _aw_config_build_type_knb)
	if inishalize:
		for knb in [_aw_config_build_type_knb, _aw_config_data_file_knb]:
			knb.setVisible(False)

#nuke.addOnCreate(add_aw_tracking_knobs, (), {}, "Root")
#nuke.addOnCreate(add_aw_project_type_knob, (), {}, "Root")
#nuke.addOnCreate( Trim_Build_Viewer_Gizmo.onCreate, (), {}, "Group")