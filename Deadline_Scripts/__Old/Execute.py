import os
import nuke
import argparse


Nuke_Files = [
'X:/Critical-Mass/CRMS-17-001_Nissan_TLJ8_Configurators_and_Print_Images/users/rbobo/TEST/nuke/comp_1.nk',
'X:/Critical-Mass/CRMS-17-001_Nissan_TLJ8_Configurators_and_Print_Images/users/rbobo/TEST/nuke/comp_2.nk',
'X:/Critical-Mass/CRMS-17-001_Nissan_TLJ8_Configurators_and_Print_Images/users/rbobo/TEST/nuke/comp_3.nk',
]
nuke.scriptOpen(Nuke_Files[(int(os.environ['STARTFRAME'])) - 1])
for node in nuke.allNodes('Write'):
	if node.knob('disable').value() == True:
		pass
	else:
		nuke.execute(node, 1, 1)