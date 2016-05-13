# Keep all our functions out of the global scope
# See geometry/__init__.py for the work

try:
	import geometry
except ImportError:
	import os, sys
	sys.path.append( os.path.dirname(sys._getframe().f_code.co_filename) )
	import geometry
