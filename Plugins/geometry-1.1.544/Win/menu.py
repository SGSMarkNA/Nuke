# GUI mode, setup the menus
# See geometry/cmd.py for the work

import geometry.commands

geometry.commands.setupNodes(nuke.menu('Nodes').addMenu('Geometry'))

# Following code are examples of setting up hot-key bindings
# the import line below must also be uncommented to use them

# import geometry.selection

# Houdini style component selection...
# nuke.menu('Nuke').addCommand ('SelectPoints', 'geometry.selection.setMode(2)', '2')
# nuke.menu('Nuke').addCommand ('SelectEdges',	'geometry.selection.setMode(1)', '3')
# nuke.menu('Nuke').addCommand ('SelectFaces',	'geometry.selection.setMode(0)', '4')

# Cycle component selection
# nuke.menu('Nuke').addCommand ('CycleSelectF', 'geometry.selection.setMode()', 'Shift+e')
# nuke.menu('Nuke').addCommand ('CycleSelectB', 'geometry.selection.setMode(-1)', 'Ctrl+Shift+e')

# Edge topology hot keys
# nuke.menu('Nuke').addCommand ('OverEdgeLoop', 'geometry.selection.edgeLoop(True)', 'e')
# nuke.menu('Nuke').addCommand ('SelEdgeRing',  'geometry.selection.edgeRing(False)', 'Shift+e')

# Font cycling 
# import geometry.fontcycler
# geometry.fontcycler.addCommand('fontFwd1', 1,  'f')
# geometry.fontcycler.addCommand('fontBwd10', -10,  'd')
