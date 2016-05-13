import nuke

def RGB_To_Hex_Color(r, g, b):
	hexCol = '#%02x%02x%02x' % (r, g, b)
	return hexCol

def get_views():
	res   =[]
	views = nuke.root().knob("views").toScript()
	views = views.replace("{","").replace("}","")
	views = views.splitlines()
	for line in views:
		name,color=[l.strip() for l in line.split()]
		res.append(Nuke_View(name, color))
	return res

class Nuke_View(nuke.View):
	def __init__(self,view,color):
		super(Nuke_View,self).__init__(view)
		self.color = color
		self._name_overide = False

	@property
	def index(self):
		return self.value()

	@property
	def name(self):
		return self.string()
	@name.setter
	def name(self, value):
		self._name_overide = value

	@property
	def string_line(self):
		if self._name_overide:
			return " ".join(self._name_overide, self.color)
		else:
			return " ".join(self.name, self.color)


class Nuke_Views(nuke.utils.FnPySingleton):

	#----------------------------------------------------------------------
	def __init__(self):
		""""""
		super(Nuke_Views, self).__init__()
		self.from_nuke_views()

	def get_view(self, arg):
		if isinstance(arg, str):
			if self.has_view(arg):
				return self.view_names.index(arg)
		if isinstance(arg, int):
			return self._views[arg]

	def has_view(self, name):
		return name in self.view_names

	@property
	def view_names(self):
		return [v.name for v in self._views]

	def from_nuke_views(self):
		self._views = get_views()

	def remove_View(self, name, delay_update=False):
		nuke.deleteView(name)
		if not delay_update:
			self.from_nuke_views()

	def add_View(self, name, delay_update=False):
		nuke.addView(name)
		if not delay_update:
			self.from_nuke_views()

	def set_nuke_views(self):
		lines = [v.string_line for v in self._views]
		expression = "\n".join(lines)
		nuke.root().knob("views").fromScript(expression)

	def rename_view(self, old_name, new_name, delay_update=False):
		view = self.get_view(old_name)
		view.name = new_name
		self.set_nuke_views()

nuke_views = Nuke_Views()