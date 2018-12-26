import glob
import os
import re
import platform
import shutil
name_num_ext_pattern = re.compile(r"(?P<name>[A-Za-z_]+)(?P<number>[0-9]+)(\W)(?P<ext>\w+)")

#----------------------------------------------------------------------
def Assine_Version_Frame_Data(filename):
	""""""
	path_to_frames = filename
	slices = path_to_frames.split(".")
	file_ext       = slices[-1]
	file_path      = ".".join(slices[:-1])
	file_base_name = os.path.basename(file_path)
	file_base_name = file_base_name.replace("#", "")
	folder_name    = os.path.dirname(file_path)
	files = glob_file_matchs(folder_name, file_base_name, file_ext)
	start, end = determan_start_end(files)
	frame_count = len(files)
	frame_range = "%i-%i" % (start, end)
	print files
	print frame_range, start, end, frame_count
	
def filenameFix(filename):
	return filename.replace( "\\", "/" )

def file_seq_dict(root_folder,res={}):
	
	root, dirs, files = os.walk(root_folder).next()
	
	for d in dirs:
		print d
		child_folder = filenameFix(os.path.join(root,d))
		
		image_files = os.walk(child_folder).next()[2]
		
		if len(image_files):
			res[d]=construct_image_seq_data(child_folder,image_files)
		else:
			res[d] = {}
			
		file_seq_dict(child_folder,res[d])
	
	return res
	
def construct_image_seq_data(root,files):
	seqBuilder = {}
	if len(files):
		
		file_names = []
		
		for f in files:
			print "\t",f
			
			match = name_num_ext_pattern.match(f)
			
			if match and match.group() == f:
				
				groups = match.groupdict()
				
				name, padding, ext   = groups["name"], len(groups["number"]), groups["ext"]
				
				if not name in file_names:
					
					file_names.append(name)
					
					seqBuilder[name]=construct_image_seq_dict(os.path.join(root,f))			
	return seqBuilder

def construct_file_sequence_expression(folder_path,file_name,frame_padding,file_extension):
	name = file_name + ".%0" + str(frame_padding) + "d." + file_extension
	expr = os.path.join(folder_path,name)
	
	return filenameFix(expr)

def glob_file_matchs(folder_name,file_base_name,file_ext):
	
	glob_pattern = os.path.join( folder_name, str( file_base_name + "*." + file_ext ) )
	
	matching_paths = glob.glob(glob_pattern)
	matching_paths.sort()
	
	return matching_paths

def paths_to_names(file_paths):
	names = [os.path.basename(f) for f in file_paths]
	return names

def determan_start_end(file_paths):
	
	file_names = paths_to_names(file_paths)
	
	ints = []
	for f in file_names:
		m = name_num_ext_pattern.match(f)
		if m is None:
			print f
		else:
			ints.append(int(m.groupdict()["number"]))
	
	if len(ints):
		start = min(ints)
		
		end   = max(ints)
		
		return start,end
	return 0,0

def construct_image_seq_dict(path,as_Nuke_Knobs=False,as_tcl=False):
	path = filenameFix(path)
	if not os.path.exists(path):
		raise ValueError("The input path %s does not exist" % path)
	
	name,number,ext = None,None,None
	
	file_name    = os.path.basename(path)
	
	folder_name  = os.path.dirname(path)
	
	match        = name_num_ext_pattern.match(file_name)
	
	if not match or not match.group() == file_name:
		raise ValueError("Was not able to find a valid file numbering pattern from %s" % (file_name))
	
	groups = match.groupdict()
	
	name, padding, ext   = groups["name"], len(groups["number"]), groups["ext"]
	
	matching_paths = glob_file_matchs(folder_name,name,ext)
	
	file_count = len(matching_paths)
	
	start_knob,end_knob = determan_start_end(matching_paths)
	
	file_knob = construct_file_sequence_expression(folder_name,name,padding,ext)
	matching_paths = [filenameFix(m) for m in matching_paths]
	if as_Nuke_Knobs:
		knob_values = dict(file=file_knob,
		                   name=name,
		                   cacheLocal="always",
		                   on_error="black",
		                   origfirst=start_knob,
		                   origlast=end_knob,
		                   last=end_knob,
		                   first=start_knob,
		                   origset=True)
		if as_tcl:
			tcl = ""
			for k,v in knob_values.items():
				if v == True:
					tcl += "%s true " % k
				elif v == False:
					tcl += "%s false " % k
				else:
					tcl += "%s %r " % (k,v)
			return tcl
	
		return knob_values
	
	else:
		res = file_sequence()
		res.file_count   = file_count
		res.file_ext     = ext
		res.file_expr    = file_knob
		res.folder_path  = folder_name
		res.file_padding = padding
		res.file_paths   = matching_paths
		res.file_name    = name
		res.last_frame   = end_knob
		res.first_frame  = start_knob
		return res
		

	
class file_sequence(object):
	def __init__(self):
		self.file_name    = ""
		self.file_count   = 0
		self.file_padding = 0
		self.file_ext     = ""
		self.last_frame   = 0
		self.first_frame  = 0
		self.file_expr    = ''
		self.file_paths   = []
		self.folder_path  = ''
	#----------------------------------------------------------------------
	def reverse_Seq(self):
		""""""
		dest_folder = os.path.join(self.folder_path,"Reversed")
		if not os.path.exists(dest_folder):
			os.makedirs(dest_folder)
		reversed_paths = [os.path.join(dest_folder,os.path.basename(item)) for item in reversed(self.file_paths)]
		
		for src,dest in zip(self.file_paths,reversed_paths):
			shutil.copyfile(src, dest)