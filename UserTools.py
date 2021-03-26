
#Creation Date:  (December 1, 2006)

#Author: Drew Loveridge
import nuke
import nukescripts
try:
	from PySide.QtGui import QAction, QIcon, QApplication, QToolTip
	from PySide.QtCore import QObject, QEvent, Qt
except:
	from PySide2.QtWidgets import QAction, QApplication, QToolTip
	from PySide2.QtGui import QIcon 
	from PySide2.QtCore import QObject, QEvent, Qt
try:
	from pathlib2 import Path
except ImportError:
	from Environment_Access import utilities, System_Paths
	utilities.add_To_System_Path(utilities.path_Builder(System_Paths.AW_GLOBAL_SYSTEMS,"GENERAL_TOOLS"))
	from pathlib2 import Path
	
import os, sys, fnmatch
import re
##_aw_user_scripts_menu_label   = os.environ["USERNAME"] + " Tools"		#### Removed for Mac OS X compatibility... RKB
_aw_user_scripts__main_folder = Path(Path(os.environ["HOME"]).joinpath(".nuke"))
_aw_python_scripts_menu_label = "AW User Tools"
_aw_python_scripts_toolbar_label = "AW User Nodes"
_nuke_global_menu_names = ['Nuke', 'Pane', 'Node Graph', 'Properties', 'Animation', 'Viewer', 'Nodes', 'Axis']
if os.environ.has_key("NUKE_USER_TOOLS_DIR"):
	_aw_user_tools_main_folder    = Path(os.path.expandvars(os.environ["NUKE_USER_TOOLS_DIR"]))
else:
	raise LookupError("Could Not find User Tools Env Variable NUKE_USER_TOOLS_DIR")
#----------------------------------------------------------------------
menu_items_pattern = re.compile(r'''
(\#.+Menu_Item\s)
(?P<params>
(\#.*\s)*
)
(def\s*)
(?P<fn_name>\w*)
(\()
(?P<inputs>.*)
(\)\s*\:)
''',flags=re.VERBOSE|re.MULTILINE)

#----------------------------------------------------------------------
########################################################################
class Menu_Tool_Tip_EventFilter(QObject):
	def eventFilter(self, obj, event):
		mod_key = QApplication.keyboardModifiers()
		if not hasattr(self, "_last_know_mod_key"):
			self._last_know_mod_key = 0
		if not hasattr(self, "_last_know_global_pos"):
			self._last_know_global_pos = None
			
		if event.type() == QEvent.ToolTip:
			act = obj.actionAt(event.pos())
			if act:
				self._last_know_global_pos = event.globalPos()
				QToolTip.showText(event.globalPos(),act.toolTip())
		elif event.type() == QEvent.ShowToParent:
			acts = obj.actions()
			for current_act in acts:
				if hasattr(current_act, "update_text"):
					current_act.update_text()
					current_act.update_icon()
		else:
			if hasattr(event, "globalPos"):
				self._last_know_global_pos = event.globalPos()
			if self._last_know_mod_key != mod_key:
				self._last_know_mod_key = mod_key
				if obj.isVisible():
					acts = obj.actions()
					for current_act in acts:
						if current_act.isVisible():
							if hasattr(current_act, "update_text"):
								current_act.update_text()
								current_act.update_icon()
								act = obj.activeAction()
								#QToolTip.hideText()
								if act is not None:
									QToolTip.showText(self._last_know_global_pos,act.toolTip())
								else:
									QToolTip.showText(self._last_know_global_pos, "This Is A Menu")
			#QToolTip.hideText()
			# standard event processing
		return QObject.eventFilter(self, obj, event)

_menu_tool_tip_eventfilter = Menu_Tool_Tip_EventFilter()
########################################################################
class Menu_Item_QAction(QAction):
	""""""
	#----------------------------------------------------------------------
	def __init__(self, menu_item_build, parent=None):
		"""Constructor"""
		super(Menu_Item_QAction, self).__init__(parent)
		isinstance(menu_item_build, Menu_Item)
		self.script                 = str(menu_item_build.script)
		self.fn_defaults            = menu_item_build.fn_defaults
		self.fn_name                = menu_item_build.fn_name
		self.auto_reload            = menu_item_build.auto_reload
		self.menus                  = menu_item_build.menus
		self._icon                  = menu_item_build._icon
		self.shift_icon             = menu_item_build.shift_icon
		self.alt_icon               = menu_item_build.alt_icon
		self.ctrl_icon              = menu_item_build.ctrl_icon
		self.args                   = menu_item_build.args
		self.shift_args             = menu_item_build.shift_args
		self.alt_args               = menu_item_build.alt_args
		self.ctrl_args              = menu_item_build.ctrl_args
		self.tooltip                = menu_item_build.tooltip
		self.shift_tooltip          = menu_item_build.shift_tooltip
		self.alt_tooltip            = menu_item_build.alt_tooltip
		self.ctrl_tooltip           = menu_item_build.ctrl_tooltip
		self._shortcut              = menu_item_build.shortcut
		self.label                  = menu_item_build.label
		self.shift_label            = menu_item_build.shift_label
		self.alt_label              = menu_item_build.alt_label
		self.ctrl_label             = menu_item_build.ctrl_label
		self.triggered.connect(self.importAndRun)
		
	def importAndRun(self):
		# create the Python command that is invoked by the menu item
		# This could be changed to scrpt.main if that is normal
		# The reload command should have a way of being turned off and on from the UI
		mod_key = QApplication.keyboardModifiers()
		
		exec 'import ' + self.script
		
		if self.auto_reload:
			exec  'reload (' + self.script + ')'
			
		input_args = []
		
		if len(self.args):
			input_args = self.args
			
		if mod_key in [Qt.Modifier.SHIFT|Qt.Modifier.CTRL, Qt.Modifier.CTRL, Qt.Modifier.SHIFT]:
			if mod_key == Qt.Modifier.SHIFT|Qt.Modifier.CTRL and len(self.alt_args):
				input_args = self.alt_args
			elif mod_key == Qt.Modifier.SHIFT and len(self.shift_args):
				input_args = self.shift_args
			elif mod_key == Qt.Modifier.CTRL and len(self.ctrl_args):
				input_args = self.ctrl_args
			
		if len(input_args):
			exec self.script + '.' + self.fn_name + '(%s)' % ",".join(input_args)
		else:
			return getattr(locals()[self.script], self.fn_name)()
			#exec self.script + '.' + self.fn_name + '(%s)' % self.fn_defaults
			
	def toolTip(self):
		mod_key = QApplication.keyboardModifiers()				
		if mod_key == Qt.Modifier.SHIFT and self.shift_tooltip != None:
			return self.shift_tooltip
		elif mod_key == Qt.Modifier.SHIFT|Qt.Modifier.CTRL and self.alt_tooltip != None:
			return self.alt_tooltip
		elif mod_key == Qt.Modifier.CTRL and self.ctrl_tooltip != None:
			return self.ctrl_tooltip
		return self.tooltip
	
	def update_text(self):
		mod_key = QApplication.keyboardModifiers()
		if mod_key == Qt.Modifier.SHIFT and self.shift_label != None:
			self.setText(self.shift_label)
			return
		elif mod_key == Qt.Modifier.SHIFT|Qt.Modifier.CTRL and self.alt_label != None:
			self.setText(self.alt_label)
			return
		elif mod_key == Qt.Modifier.CTRL and self.ctrl_label != None:
			self.setText(self.ctrl_label)
			return
		self.setText(self.label)
	def update_icon(self):
		mod_key = QApplication.keyboardModifiers()
		if mod_key == Qt.Modifier.SHIFT|Qt.Modifier.CTRL and self.alt_icon != None:
			self.setIcon(self.alt_icon)
		elif mod_key == Qt.Modifier.SHIFT and self.shift_icon != None:
			self.setIcon(self.shift_icon)
		elif mod_key == Qt.Modifier.CTRL and self.ctrl_icon != None:
			self.setIcon(self.ctrl_icon)
		elif self._icon != None:
			self.setIcon(self._icon)
		return

########################################################################
class Menu_Item(object):
	#----------------------------------------------------------------------
	def __init__(self, script_name, fn_name, defaults):
		""""""
		self.script                 = str(script_name)
		self.fn_defaults            = defaults
		self.fn_name                = fn_name
		self.auto_reload            = True
		self.menus                  = []
		self._icon                  = None
		self.shift_icon             = None
		self.alt_icon               = None
		self.ctrl_icon              = None
		self.args                   = []
		self.shift_args             = []
		self.alt_args               = []
		self.ctrl_args              = []
		self.tooltip                = None
		self.shift_tooltip          = None
		self.alt_tooltip            = None
		self.ctrl_tooltip           = None
		self.shortcut               = None
		self.label                  = None
		self.shift_label            = None
		self.alt_label              = None
		self.ctrl_label             = None
		self.user_tool_sub_menu     = None
		self.bypass_user_tools_menu = False
		self.has_sub_menus          = False
		self.panelId                = None
	@property
	def sort_name(self):
		if self.user_tool_sub_menu is None:
			return self.label
		else:
			return self.user_tool_sub_menu[0]
			


#----------------------------------------------------------------------
def file_scanner(file_path):
	data = file_path.read_text()
	Builds = []
	for menu_items in menu_items_pattern.finditer(data):
		fn_name = menu_items.groupdict()["fn_name"]
		defaults = menu_items.groupdict()["inputs"]
		if len(menu_items.group()):
			params = menu_items.groupdict()["params"]
			if len(params):
				for build in params.split("[menu_item]")[1:]:
					menu_item = Menu_Item(file_path.baseName, fn_name, defaults)
					for line in build.splitlines():
						if "shift_label:" in line:
							menu_item.shift_label = line.split(":")[1].strip()
						elif "alt_label:" in line:
							menu_item.alt_label = line.split(":")[1].strip()
						elif "ctrl_label:" in line:
							menu_item.ctrl_label = line.split(":")[1].strip()
						elif "label:" in line:
							menu_item.label = line.split(":")[1].strip()
						elif "shift_icon:" in line:
							menu_item.shift_icon = line.split(":")[1].strip()
							menu_item.shift_icon = QIcon(menu_item.shift_icon)
						elif "alt_icon:" in line:
							menu_item.alt_icon = line.split(":")[1].strip()
							menu_item.alt_icon = QIcon(menu_item.alt_icon)
						elif "ctrl_icon:" in line:
							menu_item.ctrl_icon = line.split(":")[1].strip()
							menu_item.ctrl_icon = QIcon(menu_item.ctrl_icon)
						elif "icon:" in line:
							menu_item._icon = line.split(":", 1)[1].strip()
							menu_item._icon = QIcon(menu_item._icon)
						elif "shift_tooltip:" in line:
							menu_item.shift_tooltip = '\n'.join(line.split(":")[1].strip().split("\\n"))
						elif "alt_tooltip:" in line:
							menu_item.alt_tooltip = '\n'.join(line.split(":")[1].strip().split("\\n"))
						elif "ctrl_tooltip:" in line:
							menu_item.ctrl_tooltip = '\n'.join(line.split(":")[1].strip().split("\\n"))
						elif "tooltip:" in line:
							menu_item.tooltip = '\n'.join(line.split(":")[1].strip().split("\\n"))
						elif "shift_arg:" in line:
							menu_item.shift_args.append(line.split(":")[1].strip())
						elif "alt_arg:" in line:
							menu_item.alt_args.append(line.split(":")[1].strip())
						elif "ctrl_arg:" in line:
							menu_item.ctrl_args.append(line.split(":")[1].strip())
						elif "arg:" in line:
							menu_item.args.append(line.split(":")[1].strip())
						elif "shift_args:" in line:
							menu_item.shift_args = [arg.strip() for arg in line.split(":").__getitem__(1).strip().split()]
						elif "alt_args:" in line:
							menu_item.alt_args = [arg.strip() for arg in line.split(":").__getitem__(1).strip().split()]
						elif "ctrl_args:" in line:
							menu_item.ctrl_args = [arg.strip() for arg in line.split(":").__getitem__(1).strip().split()]
						elif "args:" in line:
							menu_item.args = [arg.strip() for arg in line.split(":").__getitem__(1).strip().split()]
						elif "shortcut:" in line:
							menu_item.shortcut = line.split(":")[1].strip()
						elif "parent_menus:" in line:
							menu_item.menus = [arg.strip() for arg in line.split(":").__getitem__(1).strip().split(",")]
						elif "auto_reload:" in line:
							menu_item.auto_reload = bool(line.split(":")[1].strip())
						elif "bypass_user_tools_menu:" in line:
							menu_item.bypass_user_tools_menu = bool(line.split(":")[1].strip())
						elif "user_tool_sub_menu:" in line:
							menu_item.user_tool_sub_menu = line.split(":")[1].strip().split("/")
						elif "panelID:" in line:
							menu_item.panelId = line.split(":")[1].strip()							
					if menu_item.label == None:
						menu_item.label = fn_name
					if menu_item.user_tool_sub_menu is not None:
						menu_item.has_sub_menus = True
					Builds.append(menu_item)
			else:
				menu_item = Menu_Item(file_path.baseName, fn_name, defaults)
				menu_item.label = fn_name
				Builds.append(menu_item)
	return Builds

#----------------------------------------------------------------------
def findFile(path):
	#Find the file named path in the sys.path.
	#Returns the full path name if found, None if not found
	for dirname in sys.path:
		possible = os.path.join(dirname, path)
		if os.path.isfile(possible):
			# print dirname
			return dirname
	# print ("None")
	return None


#----------------------------------------------------------------------
def command_maker(pMenu, builds):
	global _aw_python_scripts_toolbar_label, _aw_python_scripts_menu_label, _nuke_global_menu_names
	for build in builds:
		isinstance(build, Menu_Item)
		if build.has_sub_menus or not len(build.menus):
			active_menu = pMenu
			if build.has_sub_menus:
				for menu_name in build.user_tool_sub_menu:
					active_menu = active_menu.addMenu(menu_name)
				active_menu.action().parent().installEventFilter(_menu_tool_tip_eventfilter)
			act = Menu_Item_QAction(build, parent=active_menu.action().parent())
			act.setText(build.label)	#### Needed for Mac OS X compatibility... RKB.
			if build.shortcut != None:
				act.setShortcut(build.shortcut)
			active_menu.addAction(act)
		else:
			for menu_name in build.menus:
				install_filter = False
				active_menu = None
				sub_menus = menu_name.split("/")
				
				if sub_menus[0] in _nuke_global_menu_names:
					if sub_menus[0] == "Nodes":
						active_menu = nuke.toolbar(sub_menus[0])
					else:
						active_menu = nuke.menu(sub_menus[0])
					if sub_menus[0] == "Nodes":
						active_menu = active_menu.addMenu(_aw_python_scripts_toolbar_label)
					else:
						active_menu = active_menu.addMenu(_aw_python_scripts_menu_label)
					if active_menu != None:
						for sub_menu_name in sub_menus[1:]:
							active_menu = active_menu.addMenu(sub_menu_name)
						
						act = Menu_Item_QAction(build, parent=active_menu.action().parent())
						
						if build.shortcut != None:
							act.setShortcut(build.shortcut)
						if build.panelId != None:
							nukescripts.registerPanel(build.panelId, act.importAndRun)
						active_menu.addAction(act)
						active_menu.action().parent().installEventFilter(_menu_tool_tip_eventfilter)

#----------------------------------------------------------------------
def gen_pythonScripts(mainDir, pMenu, depth=0):
	# this looks in the folder where this script is run from and generates the
	# cascading menues and Python script buttons
	mainDir = Path(mainDir)
	ignors  = ["__init__.py", "userSetup.py", "pythonScripts.py"]
	f_ignors= ["ToolSets", "Template"]
	files   = [f for f in mainDir.glob("*.py") if not f.parts[-1] in ignors]
	folders = [folder for folder in mainDir.iterdir(True) if not folder.baseName in f_ignors]
	folders = sorted(folders)
	if depth != 0:
		full_builds = []
		for current_file in files:
			builds = file_scanner(current_file)
			full_builds.extend(builds)
		full_builds = sorted(full_builds, key=lambda build: build.sort_name)
		# Puts menus at bottom of list
		# full_builds = sorted(full_builds, key=lambda build: build.has_sub_menus)	#### Test...
		command_maker(pMenu, full_builds)
	
	for current_folder in folders:
		if (current_folder.parent.baseName == "Nuke_User_Tools" or current_folder.parent.baseName == ".nuke") and depth == 0:
			label = " ".join(current_folder.baseName.split("_"))
			menu  = pMenu.addMenu(label)
			menu.action().parent().installEventFilter(_menu_tool_tip_eventfilter)
			if not str(current_folder) in sys.path:
				sys.path.append(str(current_folder))

			#start new can scan
			gen_pythonScripts (current_folder, menu, depth+1)
		elif depth <= 1:
			if not str(current_folder) in sys.path:
				sys.path.append(str(current_folder))
			gen_pythonScripts(current_folder, pMenu, depth+1)
#----------------------------------------------------------------------
def importAndRun(scrpt, fn):
	# create the Python command that is invoked by the menu item
	# This could be changed to scrpt.main if that is normal
	# The reload command should have a way of being turned off and on from the UI
	exec 'import ' + scrpt

	exec  'reload (' + scrpt + ')'
	if scrpt == "UserTools":
		exec scrpt + '.pythonScripts()'
	else:
		exec scrpt + '.' + fn + '()'

#----------------------------------------------------------------------
def menu_exist(menu_name):
	menu = nuke.menu('Nuke')
	return menu.findItem(menu_name) == None

#----------------------------------------------------------------------
def delete_menu(menu_name):
	menu = nuke.menu('Nuke')
	if not menu.findItem(menu_name) == None:
		menu.removeItem(menu_name)

#----------------------------------------------------------------------
def create_menu(menu_name):
	Menu = nuke.menu("Nuke").addMenu(menu_name)
	return Menu

#----------------------------------------------------------------------
def create_User_Tools_Sub_menus():
	#'Nuke'          the application menu
	#'Pane'          the UI Panes & Panels menu
	#'Nodes'         the Nodes toolbar (and Nodegraph right mouse menu)
	#'Properties'    the Properties panel right mouse menu
	#'Animation'     the knob Animation menu and Curve Editor right mouse menu
	#'Viewer'        the Viewer right mouse menu
	#'Node Graph'    the Node Graph right mouse menu
	#'Axis'          functions which appear in menus on all Axis_Knobs.
	global _aw_python_scripts_menu_label, _nuke_global_menu_names
	for menu_name in _nuke_global_menu_names:
		if menu_name == "Nodes":
			Menu = nuke.toolbar(menu_name)
		else:
			Menu = nuke.menu(menu_name)
		Menu.addMenu(_aw_python_scripts_menu_label)

#----------------------------------------------------------------------
def clear_User_Tools_Sub_menus():
	global _aw_python_scripts_toolbar_label, _aw_python_scripts_menu_label, _nuke_global_menu_names
	for menu_name in _nuke_global_menu_names:
		Menu = nuke.menu(menu_name)
		if menu_name == "Nodes":
			if Menu.findItem(_aw_python_scripts_toolbar_label) != None:
				sub_menu = Menu.findItem(_aw_python_scripts_toolbar_label)
				sub_menu.clearMenu()
				Menu.removeItem(_aw_python_scripts_toolbar_label)
		elif menu_name == "Pane":
			if Menu.findItem(_aw_python_scripts_menu_label) != None:
				sub_menu = Menu.findItem(_aw_python_scripts_menu_label)
				for item in sub_menu.items(): 
					sub_menu.removeItem(item.name())
		else:
			if Menu.findItem(_aw_python_scripts_menu_label) != None:
				sub_menu = Menu.findItem(_aw_python_scripts_menu_label)
				for item in sub_menu.items(): 
					sub_menu.removeItem(item.name())

#----------------------------------------------------------------------
def pythonScripts():
	global _aw_python_scripts_menu_label, _aw_user_tools_main_folder
	delete_menu(_aw_python_scripts_menu_label)
	##delete_menu(_aw_user_scripts_menu_label)		#### Removed for Mac OS X compatibility... RKB.
	if not str(_aw_user_tools_main_folder) in sys.path:
		sys.path.append(str(_aw_user_tools_main_folder))
	mainDir = _aw_user_tools_main_folder
	clear_User_Tools_Sub_menus()
	#create_User_Tools_Sub_menus()
	pMenu = create_menu(_aw_python_scripts_menu_label)
	#act   = Menu_Item_QAction("UserTools", "")
	pMenu.addCommand("Rebuild Menu", 'UserTools.importAndRun("UserTools","")')
	#pMenu.addAction(act)
	gen_pythonScripts(mainDir, pMenu)
	#pMenu = create_menu(_aw_user_scripts_menu_label)
	#gen_pythonScripts(_aw_user_scripts__main_folder, pMenu)