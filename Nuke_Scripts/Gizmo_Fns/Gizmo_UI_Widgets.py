import nuke
import os, sys
_ui_foulder = os.path.join(os.path.dirname(__file__), "UI")
moduleName = __name__

if moduleName == '__main__':
	moduleName = ''
else:
	moduleName = moduleName

import PYQT

class UiLoader(PYQT.QUiLoader):
	''''''
	def __init__(self,*args,**kwargs):
		''''''
		super(UiLoader,self).__init__(*args,**kwargs)
		self._custom_wigets = dict()
		self._wigs = []
	#----------------------------------------------------------------------
	def createAction(self,parent=None,name=None):
		"""
		createAction(parent=None,name=None)
			parent=QtCore.QObject
			name=unicode

		Creates a new action with the given parent and name .
		The function is also used internally by the PySide.QtUiTools.QUiLoader class whenever it creates a widget
		Hence, you can subclass PySide.QtUiTools.QUiLoader and reimplement this function to intervene process of constructing a user interface or widget
		However, in your implementation, ensure that you call PySide.QtUiTools.QUiLoader s version first.
		"""
		res = super(UiLoader,self).createAction(parent,name)
		isinstance(res,PYQT.QAction)
		return res
	#----------------------------------------------------------------------
	def createActionGroup(self,parent=None,name=None):
		"""
		createActionGroup(parent=None,name=None)
			parent=QtCore.QObject
			name=unicode

		Creates a new action group with the given parent and name .
		The function is also used internally by the PySide.QtUiTools.QUiLoader class whenever it creates a widget
		Hence, you can subclass PySide.QtUiTools.QUiLoader and reimplement this function to intervene process of constructing a user interface or widget
		However, in your implementation, ensure that you call PySide.QtUiTools.QUiLoader s version first.
		"""
		res = super(UiLoader,self).createActionGroup(parent,name)
		isinstance(res,PYQT.QActionGroup)
		return res
	#----------------------------------------------------------------------
	def createLayout(self,className,parent=None,name=None):
		"""
		createLayout(className,parent=None,name=None)
			className=unicode
			parent=QtCore.QObject
			name=unicode

		Creates a new layout with the given parent and name using the class specified by className .
		The function is also used internally by the PySide.QtUiTools.QUiLoader class whenever it creates a widget
		Hence, you can subclass PySide.QtUiTools.QUiLoader and reimplement this function to intervene process of constructing a user interface or widget
		However, in your implementation, ensure that you call PySide.QtUiTools.QUiLoader s version first.
		"""
		res = super(UiLoader,self).createLayout(className,parent,name)
		isinstance(res,PYQT.QLayout)
		return res
	#----------------------------------------------------------------------
	def createWidget(self,className,parent=None,name=None):
		"""
		createWidget(className,parent=None,name=None)
			className=unicode
			parent=QtGui.QWidget
			name=unicode

		Creates a new widget with the given parent and name using the class specified by className
		You can use this function to create any of the widgets returned by the PySide.QtUiTools.QUiLoader.availableWidgets() function.
		The function is also used internally by the PySide.QtUiTools.QUiLoader class whenever it creates a widget
		Hence, you can subclass PySide.QtUiTools.QUiLoader and reimplement this function to intervene process of constructing a user interface or widget
		However, in your implementation, ensure that you call PySide.QtUiTools.QUiLoader s version first.
		"""
		if className in self._custom_wigets:
			res = self._custom_wigets[className](parent=parent)
			res.setObjectName(name)
		else:
			res = super(UiLoader,self).createWidget(className,parent,name)
		isinstance(res,PYQT.QWidget)
		self._wigs.append(res)
		return res
	#----------------------------------------------------------------------
	def load(self,*args,**kwargs):
		"""
		load(device,parentWidget=None)
			device=QtCore.QIODevice
			parentWidget=QtGui.QWidget

		load(arg__1,parentWidget=None)
			arg__1=unicode
			parentWidget=QtGui.QWidget

		Loads a form from the given device and creates a new widget with the given parentWidget to hold its contents.
		"""
		res = super(UiLoader,self).load(*args,**kwargs)
		isinstance(res,PYQT.QWidget)
		return res
	#----------------------------------------------------------------------
	def load_file(self, file_path, parent_widget=None):
		""""""
		Qfile = PYQT.QFile(file_path)
		Qfile.open(PYQT.QFile.ReadOnly)
		ui_wig = self.load(Qfile,parent_widget)
		Qfile.close()
		return ui_wig
	#----------------------------------------------------------------------
	def registerCustomWidget(self,customWidgetType):
		"""
		registerCustomWidget(customWidgetType)
			customWidgetType=Object

		Registers a Python created custom widget to QUiLoader, so it can be recognized when
		loading a .ui file
		The custom widget type is passed via the customWidgetType argument.
		This is needed when you want to override a virtual method of some widget in the interface,
		since duck punching will not work with widgets created by QUiLoader based on the contents
		of the .ui file.
		(Remember that duck punching virtual methods is an invitation for your own demise!)
		Lets see an obvious example
		If you want to create a new widget its probable youll end up
		overriding QWidgets paintEvent() method.
		"""
		self._custom_wigets[customWidgetType.__name__] = customWidgetType
		res = super(UiLoader,self).registerCustomWidget(customWidgetType)
		return res


GUI_Loader = UiLoader()
	#----------------------------------------------------------------------
def remove_Tab(node,tab_knob_name):
	"""
	addUserKnob {20 Tab_A l "Tab A"}
	addUserKnob {3 a_number l "A Number"} a_number
	addUserKnob {6 a_check_box l "A Check Box" +STARTLINE} a_check_box
	addUserKnob {20 Tab_B l "Tab B"}
	addUserKnob {3 other_number l "Other Number"} other_number
	"""
	tab_knob = node.knob(tab_knob_name)
	# Make Sure That This Knob Is Attached To A Node
	if node is not None:
		# Make A Variable That Will Tell The Code To Start Looking For The End Of This Tab
		# By Looking For The Next Tab Knob
		in_collection = False
		# Holds The Name Of Tab Knob That Comes After This Tab Knob
		end_tab_name = None
		# Holds The knobs that are associated with this tab
		knb_collection = []
		# Scan Each Line Of User Knobs On The Attaced Node
		for line in node.writeKnobs(nuke.WRITE_USER_KNOB_DEFS).splitlines():
			if len(line):
				if line.startswith("addUserKnob"):
					# Get The Knob Type Number
					user_knob_type = line.split()[1].replace("{","")
					# Get The Knob Name
					line_tab_name  = line.split()[2].replace("}","")
					# Check If We Have Not Found This Tab Knob Yet
					if not in_collection:
						# If Not Check if The Knob Type Is a tab and not a tab group
						if user_knob_type == '20' and not "n 1}" in line and not "n -1}" in line:
							# now check if the name matches this tab
							if line_tab_name == tab_knob.name:
								# We Are Now In This Tab Knob
								in_collection=True
					else:
						# If So Check if The Knob Type Is a tab and not a tab group
						if user_knob_type == '20' and not "n 1}" in line and not "n -1}" in line:
							# If So Then Mark it and stop this scan
							end_tab_name = line_tab_name
							break
				
		# Reset 
		in_collection = False
		# Scan Through All The Knobs On The Attached Node
		for knb in node.allKnobs():
			if knb.Class() == "Tab_Knob" and knb.name() == tab_knob.name:
				in_collection = True
				knb_collection.append(knb)
			elif in_collection:
				if knb.Class() == "Tab_Knob" and knb.name() == end_tab_name:
					in_collection = False
					break
				else:
					knb_collection.append(knb)

		for knb in reversed(knb_collection):
			node.removeKnob(knb)


class _CallBack_Singles(PYQT.QObject):
	Knob_Changed_Signal = PYQT.Signal(object,object)

CallBack_Singles = _CallBack_Singles()

def _on_knob_changed():
	""""""
	knb = nuke.thisKnob()
	nod = nuke.thisNode()
	CallBack_Singles.Knob_Changed_Signal.emit(nod,knb)

class UI_Base_Widget_Knob(PYQT.QWidget):
	Knob_Changed = PYQT.Signal(nuke.Knob)
	def __init__(self, node, uifile, parent=None):
		PYQT.QWidget.__init__(self, parent)
		master_Layout = PYQT.QVBoxLayout(self)
		master_Layout.setSpacing(0)
		master_Layout.setContentsMargins(0, 0, 0, 0)
		
		self.file_wig = GUI_Loader.load(uifile, parent_widget=self)
		master_Layout.addWidget(self.file_wig)
		self._nuke_node = node
		isinstance(self._nuke_node,nuke.Node)
		if len(moduleName):
			cmd = moduleName+"._on_knob_changed()"
		else:
			cmd = "_on_knob_changed()"
		self._nuke_node.knob('knobChanged').setValue(cmd)
		CallBack_Singles.Knob_Changed_Signal.connect(self._on_knob_changed)
		self.Knob_Changed.connect(self.on_knob_changed)
	#----------------------------------------------------------------------
	def _on_knob_changed(self,nod,knb):
		""""""
		if nod == self._nuke_node:
			self.Knob_Changed.emit(knb)
	#----------------------------------------------------------------------
	def on_knob_changed(self,knb):
		""""""
		pass
	#----------------------------------------------------------------------
	def makeUI(self):
		return self
	#----------------------------------------------------------------------
	def updateValue(self):
		return None
		
	@classmethod
	def add_Widget_Knob(cls,node,name,moduleName="",label='',tab="Widget"):
		if len(moduleName):
			cmd = moduleName+"."+cls.__name__+'(  nuke.thisNode()  )'
		else:
			cmd = cls.__name__+'(  nuke.thisNode()  )'
		if tab in node.knobs().keys():
			remove_Tab(node,tab)
		tab_knb = nuke.Tab_Knob(tab)
		node.addKnob(tab_knb)
		knb = nuke.PyCustom_Knob(name, "", cmd)
		node.addKnob(knb)
		return knb
		
class Base_Widget_Knob(PYQT.QWidget):
	def __init__(self, node, parent=None):
		PYQT.QWidget.__init__(self, parent)
		self._nuke_node = node
		
	def makeUI(self):
		return self
	def updateValue(self):
		return None
	
	@classmethod
	def add_Widget_Knob(cls,node,name,label=''):
		if len(moduleName):
			cmd = moduleName+"."+cls.__name__+'(  nuke.thisNode()  )'
		else:
			cmd = cls.__name__+'(  nuke.thisNode()  )'
		knb = nuke.PyCustom_Knob(name, "", cmd)
		node.addKnob(knb)
		return knb
