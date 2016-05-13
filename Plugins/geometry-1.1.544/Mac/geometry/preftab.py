
import nuke

class PrefTab :
	def __init__( self ) :
		self.prefs = nuke.toNode('preferences')

	def setDefaults( self, name, alwaysSave = False ) :
		k = nuke.Tab_Knob(name)
		if alwaysSave: k.setFlag(nuke.ALWAYS_SAVE)
		self.prefs.addKnob(k)
		return True

	def set( self, knobs, clzz, place = True ) :
		i = 0
		kns = []
		for kn in knobs:
			k = eval('nuke.'+clzz+'("'+kn[0]+'")')
			k.setValue(kn[1])
			self.prefs.addKnob(k)
			k.setFlag(nuke.NO_ANIMATION|nuke.STARTLINE if place and i % 2 == 0 else nuke.NO_ANIMATION)
			kns.append(k)
			if len(kn) > 2 : k.setTooltip(kn[2]);
			i = i + 1
		return kns

	def watch( self, proc, args = (), keys = {} ) :
		nuke.addKnobChanged(proc, args, keys, 'Preferences', self.prefs)

	def knob( self, name ) :
		return self.prefs.knob(name)

	def value( self, name, deflt = None ) :
		k = self.knob(name)
		return k.value() if k else deflt
