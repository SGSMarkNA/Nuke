try :
	import nuke
except ImportError:
	nuke = None

def bookend():
	frame = nuke.frame()
	knob = nuke.thisKnob()

	try:
		size = knob.arraySize()
		array = True
	except:
		size = 1
		array = False

	if not knob.isAnimated():
		for i in range(size):
			if array:
				value = knob.getValueAt(frame, i)
			else:
				value = knob.value()
			knob.setAnimated(i)
			knob.animation(i).setKey(frame - 1, value)
			knob.animation(i).setKey(frame + 1, value)

	else:
		for i in range(size):
			before = knob.animation(i).evaluate(frame - 1)
			after = knob.animation(i).evaluate(frame + 1)
			knob.animation(i).setKey(frame - 1, before)
			knob.animation(i).setKey(frame + 1, after)