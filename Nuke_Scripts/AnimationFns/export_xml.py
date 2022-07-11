try:
	import nuke
except ImportError:
	nuke = None

from xml.etree import cElementTree as etree

def xml_Animation_Export(knb,make_CONSTANT=True):
	if make_CONSTANT:
		for anim in knb.animations():
			anim.changeInterpolation(list(anim.keys()),nuke.CONSTANT)
	root = etree.Element("Animations")
	tree = etree.ElementTree(root)

	knob_anims_elem = etree.SubElement(root,"Knob",{"name":knb.name(),"Class":knb.Class()})

	for anim in knb.animations():
		animCurve_elem = etree.SubElement(knob_anims_elem,"Curve",{"field":anim.knobAndFieldName().split(".")[1],'index':str(anim.knobIndex())})
		for key in list(anim.keys()):
			key_elem = etree.SubElement(animCurve_elem,"Key")
			etree.SubElement(key_elem,"x").text = str(key.x)
			etree.SubElement(key_elem,"y").text = str(key.y)
	return tree