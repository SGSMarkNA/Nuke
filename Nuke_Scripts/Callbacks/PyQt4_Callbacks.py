from PySide import QtCore
import  nuke

class _CallBack_Singles(QtCore.QObject):
	Node_Selected_Signal      = QtCore.Signal(object)
	Node_UnSelected_Signal    = QtCore.Signal(object)
	Node_Pos_Changed_Signal   = QtCore.Signal(object)
	Knob_X_Pos_Changed_Signal = QtCore.Signal(object)
	Knob_Y_Pos_Changed_Signal = QtCore.Signal(object)


CallBack_Singles = _CallBack_Singles()

def Emit_Node_Selection_Changed():
	knob = nuke.thisKnob()
	if not knob == None:
		if nuke.thisKnob().name() == "selected":
			if nuke.thisKnob().value():
				CallBack_Singles.Node_Selected_Signal.emit(nuke.thisKnob().node())
			else:
				CallBack_Singles.Node_UnSelected_Signal.emit(nuke.thisKnob().node())

def Emit_Node_Pos_Changed():
	knob = nuke.thisKnob()
	if not knob == None:
		if knob.name() in ["xpos", "ypos"]:
			node = knob.node()
			CallBack_Singles.Node_Pos_Changed_Signal.emit(node)
			if knob.name() == "xpos":
				CallBack_Singles.Knob_X_Pos_Changed_Signal.emit(knob)
			elif knob.name() == "ypos":
				CallBack_Singles.Knob_Y_Pos_Changed_Signal.emit(knob)