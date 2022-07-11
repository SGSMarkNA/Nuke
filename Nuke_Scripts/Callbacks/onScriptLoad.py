import nuke

def Load_Active_Session():
	from ..Config_Project_Tools.Active_Session import active_session
	knb = nuke.root().knob("aw_prj_project_type")
	if not knb == None:
		if knb.value() == "Infiniti Global Configurator":
			active_session.rebuild_session_from_nuke_knob()
			#active_session.add_timer()


def Convert_Global_Config_Gizmo_To_Project():
	from ..Config_Project_Tools.Active_Session import active_session
	from .onCreate import _aw_project_type_knb, _aw_config_data_file_knb
	knb   = nuke.root().knob("aw_prj_project_type")
	nodes = nuke.allNodes("Global_Config_Data", nuke.root())
	if len(nodes):
		gcd = nodes[0]
		if not knb == None:
			if not knb.value() == "Infiniti Global Configurator":
				knb.setValue("Infiniti Global Configurator")
				path = gcd.knob("config_file").value()

				if gcd.knob("config_prj_type").value() == "INT":
					nuke.root().knob("aw_prj_config_build_type").setValue(list(nuke.root().knob("aw_prj_config_build_type").values())[0])
				else:
					nuke.root().knob("aw_prj_config_build_type").setValue(list(nuke.root().knob("aw_prj_config_build_type").values())[1])

				nuke.root().knob("aw_prj_config_data_file").setValue(path)
				nuke.delete(gcd)
				active_session.rebuild_session_from_nuke_knob()
				active_session.add_timer()

#nuke.addOnScriptLoad(Convert_Global_Config_Gizmo_To_Project, (), {}, "Root")
#nuke.addOnScriptLoad(Load_Active_Session, (), {}, "Root")