try:
	import PySide2
	from PySide2 import QtCore, QtGui, QtUiTools, QtWidgets
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtUiTools import *
	# from PySide2.QtWebKit import *
	from PySide2.QtWidgets import *
	import shiboken2 as sip
	wraperfn       = sip.wrapInstance
	Qt             = QtCore.Qt
	QtSlot         = QtCore.Slot
	QtSignal       = QtCore.Signal
	QtProperty     = QtCore.Property
	PySide_version = PySide2.__version_info__[0]
except:
	import PySide
	from PySide import QtCore, QtGui, QtUiTools, QtWebKit
	from PySide.QtCore import *
	from PySide.QtGui import *
	from PySide.QtUiTools import *
	from PySide.QtWebKit import *
	try:
		import PySide.shiboken as shiboken
	except:
		try:
			import shiboken
		except:
			shiboken = None
	if shiboken is not None:
		sip        = shiboken
		wraperfn   = shiboken.wrapInstance
	Qt             = QtCore.Qt
	QtSlot         = QtCore.Slot
	QtSignal       = QtCore.Signal
	QtProperty     = QtCore.Property
	PySide_version = PySide.__version_info__[0]
if not hasattr(Qt, 'MiddleButton'):
	Qt.MiddleButton = Qt.MidButton # some Qt code uses MidButton and other places it uses MiddleButton
