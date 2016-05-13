try:
	import nuke
except ImportError:
	nuke = None

def copy_bounding_box(Master, slaves, offset = 0):
	"""
	Copy The Values Of The Master BBox_Knob To All slave BBox_Knobs Optional
	Offset Input Offset Effects The Overall Size Of Box In all Direction
	"""
	# Make sure the Master input is of type BBox_Knob
	if not typeChecks.is_BBox_Knob(Master):
		# If Not Raise a ValueError and Tell Tell The User
		raise ValueError(),str(
			"Master Input Must Be A BBox_Knob And A "+
			str(type(Master))+
			" was Found instead")
	# Grab and store the values for the Master BBox_Knob 
	x,y,r,t = Master.x(),Master.y(),Master.r(),Master.t()
	# Check if the slaves input is a list
	if isinstance(slaves,list):
		# If so scan through Each one Make sure it is of type BBox_Knob
		for i,v in enumerate(slaves):
			# Check if the slave at index i is of type BBox_Knob
			if not typeChecks.is_BBox_Knob(v):
				# If Not Raise a ValueError and Tell Tell The User
				raise ValueError(),str(
					"Found "+
					(str(type(v)))+
					" at index "+
					str(i)+
					" all input slaves must be of type BBox_Knob")
		# iterate Through each slave and set it's values to the master with
		# the optional offset
		for s in slaves:
			s.setX( x - offset )
			s.setY( y - offset )
			s.setR( r + offset )
			s.setT( t + offset )
	# Check if the slave is of type BBox_Knob
	elif typeChecks.is_BBox_Knob(slaves):
		# set the BBox_Knob values to that of the Master
		slaves.setX( x - offset )
		slaves.setY( y - offset )
		slaves.setR( r + offset )
		slaves.setT( t + offset )
	else:
		# Raise a ValueError and Tell Tell The User
		nuke.message("slaves Input Must Be A BBox_Knob or a list of "+
				     "BBox_Knobs And A %s was Found instead" % str(type(slaves))
				     )
		raise ValueError()
	
def copy_xy_pos(From,To, offsetX=0, offsetY=0):
	x = float(From.xpos() + offsetX)
	y = float(From.ypos() + offsetY)
	To.setXYpos(int(x), int(y))
	
def copy_views(From, To):
	To.knob( "views" ).setValue( From.knob( "views" ).value() )
	
def copy_file_path(From, To):
	Value = str(From.knob("file").value())
	To.knob( "file" ).setValue( From.knob("file").value())
