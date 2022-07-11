try :
	import nuke
except ImportError:
	nuke = None

def set_selected_font_size():
	knobname = 'note_font_size'
	nfs = int(nuke.getInput("Font Size"))
	for n in nuke.selectedNodes():
		n[knobname].setValue(nfs)

def set_selected_values():
	inputPanel = nuke.Panel("ChangeValue")
	inputPanel.addSingleLineInput("Node_Class", "*")
	inputPanel.addSingleLineInput("Knob_Name", "size")
	inputPanel.addSingleLineInput("Knob_Value", "10")
	inputPanel.show()

	Class = inputPanel.value("Node_Class")
	Name = inputPanel.value("Knob_Name")
	Value = inputPanel.value("Knob_Value")
	knoblist = []
	for i in nuke.selectedNodes():
		if i.Class() == Class:
			if Name in i.knobs():
				knb = i[Name]
				knoblist.append(knb)
	if len(knoblist):
		typ = type(knb.value())
		Value = typ(Value)
		for knb in knoblist:
			knb.setValue(Value)

def Int_To_Hex(intValue):
	hexValue = '%x' % intValue
	return hexValue

def RGB_To_Hex_Color(r, g, b):
	hexCol = '#%02x%02x%02x' % (r, g, b)
	return hexCol

def Float_To_Int(col):
	rgb = int(col*255)