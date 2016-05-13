# 

import nuke

kGlobalSettings = {
 'darwin':'/Library/Fonts/Andale Mono.ttf',
 'win32' : '/Windows/Fonts/arial.ttf',
 'win64' : '/Windows/Fonts/arial.ttf',
 'linux' : '/usr/share/fonts/truetype/Vera.ttff',
 'linux2' : '/usr/share/fonts/truetype/Vera.ttf',

 # Enable font hotkey preferences
 'hotkeys': False
}

def font() :
	k = nuke.toNode('preferences').knob('polyTextFont')
	return k.value() if k else ""
