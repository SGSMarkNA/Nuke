try:
	import nuke
except ImportError:
	nuke = None

def expaned_frame_ranges(expression):
	"""expression input should be a string of space seperated frames or frame ranges"""
	# storage list for collecting all expaded frames
	expanded_frames = []
	# Seperate the expressions
	expression_items = expression.split()

	# iterate through each expression item
	for item in expression_items:
		# convert the expression into a Frame Range
		nfr = nuke.FrameRange(item)
		# expand the Frame Range into a list of frames
		frame_list = list(nfr)
		# add to the final collection
		expanded_frames.extend(frame_list)

	#remove any duplicate frames by converting the list to a set
	expanded_frames = list(set(expanded_frames))

	return expanded_frames

def frame_list_to_frameranges(framelist):
	ranges = nuke.FrameRanges( " ".join([str(f) for f in framelist]))
	ranges.compact()
	return ranges


def distribute_frames_by_task_size(framelist,task_size):
	if isinstance(framelist,str):
		framelist = expaned_frame_ranges(framelist)
	
	rez = []
	frame_count = len(framelist)
	frame_set_len = frame_count/task_size
	remainder_frames = frame_count%task_size

	for i in range(task_size):
		st = i*frame_set_len
		end = (i+1)*frame_set_len
		if remainder_frames and task_size==i+1:
			ranges = nuke.FrameRanges( " ".join([str(f) for f in framelist[st:]]))
		else:
			ranges = nuke.FrameRanges( " ".join([str(f) for f in framelist[st:end]]))
		ranges.compact()
		rez.append(ranges)

	return rez

#import Scripts.AnimationFns.frame_ranges as frame_ranges
#expression = "1-15 20 22 25 40-55 60"

#def expaned_frame_ranges(expression):
	#"""expression input should be a string of space seperated frames or frame ranges"""

	## storage list for collecting all expaded frames
	#expanded_frames = []
	## Seperate the expressions
	#expression_items = expression.split()

	## iterate through each expression item
	#for item in expression_items:
	## convert the expression into a Frame Range
	#nfr = nuke.FrameRange(item)
	## expand the Frame Range into a list of frames
	#frame_list = list(nfr)
	## add to the final collection
	#expanded_frames.extend(frame_list)

	##remove any duplicate frames by converting the list to a set
	#expanded_frames = list(set(expanded_frames))

	#return expanded_frames

#expaned_frame_ranges(expression)