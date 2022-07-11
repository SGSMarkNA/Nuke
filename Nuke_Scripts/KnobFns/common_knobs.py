

from collections import namedtuple,_itemgetter
import os

namedtuple("KnobTypes", "ObsoleteKnob StringKnob FileKnob IntKnob EnumKnob BitMaskKnob BoolKnob DoubleKnob FloatKnob ArrayKnob ChannelMaskKnob ChannelKnob XYKnob XYZKnob WHKnob BBoxKnob SizeKnob FormatKnob ColorKnob AColorKnob TabKnob CustomKnob PyScriptKnob TextEditorKnob Transform2DKnob SpacerKnob TextKnob HelpKnob MultilineStringKnob AxisKnob UVKnob Box3Knob ScriptKnob LookupCurvesKnob TooltipKnob PulldownKnob EyeDropperKnob RangeKnob HistogramKnob KeyerKnob ColorChipKnob LinkKnob ScaleKnob MultilineEvalStringKnob OneViewKnob MultiViewKnob ViewViewKnob PyPulldownKnob GPUEngineKnob MultiArrayKnob ViewPairKnob ListKnob PythonKnob MetaDataKnob PixelAspectKnob CpKnob ToolbarKnob TabGroupKnob PluginPythonKnob ExoGroupKnob MenuKnob PasswordKnob ToolboxKnob TableKnob InputOnlyChannelMaskKnob InputOnlyChannelKnob")

class KnobTypes(tuple):
	'KnobTypes(ObsoleteKnob, StringKnob, FileKnob, IntKnob, EnumKnob, BitMaskKnob, BoolKnob, DoubleKnob, FloatKnob, ArrayKnob, ChannelMaskKnob, ChannelKnob, XYKnob, XYZKnob, WHKnob, BBoxKnob, SizeKnob, FormatKnob, ColorKnob, AColorKnob, TabKnob, CustomKnob, PyScriptKnob, TextEditorKnob, Transform2DKnob, SpacerKnob, TextKnob, HelpKnob, MultilineStringKnob, AxisKnob, UVKnob, Box3Knob, ScriptKnob, LookupCurvesKnob, TooltipKnob, PulldownKnob, EyeDropperKnob, RangeKnob, HistogramKnob, KeyerKnob, ColorChipKnob, LinkKnob, ScaleKnob, MultilineEvalStringKnob, OneViewKnob, MultiViewKnob, ViewViewKnob, PyPulldownKnob, GPUEngineKnob, MultiArrayKnob, ViewPairKnob, ListKnob, PythonKnob, MetaDataKnob, PixelAspectKnob, CpKnob, ToolbarKnob, TabGroupKnob, PluginPythonKnob, ExoGroupKnob, MenuKnob, PasswordKnob, ToolboxKnob, TableKnob, InputOnlyChannelMaskKnob, InputOnlyChannelKnob)'

	__slots__ = ()

	_fields = ('ObsoleteKnob', 'StringKnob', 'FileKnob', 'IntKnob', 'EnumKnob', 'BitMaskKnob', 'BoolKnob', 'DoubleKnob', 'FloatKnob', 'ArrayKnob', 'ChannelMaskKnob', 'ChannelKnob', 'XYKnob', 'XYZKnob', 'WHKnob', 'BBoxKnob', 'SizeKnob', 'FormatKnob', 'ColorKnob', 'AColorKnob', 'TabKnob', 'CustomKnob', 'PyScriptKnob', 'TextEditorKnob', 'Transform2DKnob', 'SpacerKnob', 'TextKnob', 'HelpKnob', 'MultilineStringKnob', 'AxisKnob', 'UVKnob', 'Box3Knob', 'ScriptKnob', 'LookupCurvesKnob', 'TooltipKnob', 'PulldownKnob', 'EyeDropperKnob', 'RangeKnob', 'HistogramKnob', 'KeyerKnob', 'ColorChipKnob', 'LinkKnob', 'ScaleKnob', 'MultilineEvalStringKnob', 'OneViewKnob', 'MultiViewKnob', 'ViewViewKnob', 'PyPulldownKnob', 'GPUEngineKnob', 'MultiArrayKnob', 'ViewPairKnob', 'ListKnob', 'PythonKnob', 'MetaDataKnob', 'PixelAspectKnob', 'CpKnob', 'ToolbarKnob', 'TabGroupKnob', 'PluginPythonKnob', 'ExoGroupKnob', 'MenuKnob', 'PasswordKnob', 'ToolboxKnob', 'TableKnob', 'InputOnlyChannelMaskKnob', 'InputOnlyChannelKnob')

	def __new__(_cls, ObsoleteKnob, StringKnob, FileKnob, IntKnob, EnumKnob, BitMaskKnob, BoolKnob, DoubleKnob, FloatKnob, ArrayKnob, ChannelMaskKnob, ChannelKnob, XYKnob, XYZKnob, WHKnob, BBoxKnob, SizeKnob, FormatKnob, ColorKnob, AColorKnob, TabKnob, CustomKnob, PyScriptKnob, TextEditorKnob, Transform2DKnob, SpacerKnob, TextKnob, HelpKnob, MultilineStringKnob, AxisKnob, UVKnob, Box3Knob, ScriptKnob, LookupCurvesKnob, TooltipKnob, PulldownKnob, EyeDropperKnob, RangeKnob, HistogramKnob, KeyerKnob, ColorChipKnob, LinkKnob, ScaleKnob, MultilineEvalStringKnob, OneViewKnob, MultiViewKnob, ViewViewKnob, PyPulldownKnob, GPUEngineKnob, MultiArrayKnob, ViewPairKnob, ListKnob, PythonKnob, MetaDataKnob, PixelAspectKnob, CpKnob, ToolbarKnob, TabGroupKnob, PluginPythonKnob, ExoGroupKnob, MenuKnob, PasswordKnob, ToolboxKnob, TableKnob, InputOnlyChannelMaskKnob, InputOnlyChannelKnob):
		return _tuple.__new__(_cls, (ObsoleteKnob, StringKnob, FileKnob, IntKnob, EnumKnob, BitMaskKnob, BoolKnob, DoubleKnob, FloatKnob, ArrayKnob, ChannelMaskKnob, ChannelKnob, XYKnob, XYZKnob, WHKnob, BBoxKnob, SizeKnob, FormatKnob, ColorKnob, AColorKnob, TabKnob, CustomKnob, PyScriptKnob, TextEditorKnob, Transform2DKnob, SpacerKnob, TextKnob, HelpKnob, MultilineStringKnob, AxisKnob, UVKnob, Box3Knob, ScriptKnob, LookupCurvesKnob, TooltipKnob, PulldownKnob, EyeDropperKnob, RangeKnob, HistogramKnob, KeyerKnob, ColorChipKnob, LinkKnob, ScaleKnob, MultilineEvalStringKnob, OneViewKnob, MultiViewKnob, ViewViewKnob, PyPulldownKnob, GPUEngineKnob, MultiArrayKnob, ViewPairKnob, ListKnob, PythonKnob, MetaDataKnob, PixelAspectKnob, CpKnob, ToolbarKnob, TabGroupKnob, PluginPythonKnob, ExoGroupKnob, MenuKnob, PasswordKnob, ToolboxKnob, TableKnob, InputOnlyChannelMaskKnob, InputOnlyChannelKnob))

	@classmethod
	def _make(cls, iterable, new=tuple.__new__, len=len):
		'Make a new KnobTypes object from a sequence or iterable'
		result = new(cls, iterable)
		if len(result) != 66:
			raise TypeError('Expected 66 arguments, got %d' % len(result))
		return result

	def __repr__(self):
		return 'KnobTypes(ObsoleteKnob=%r, StringKnob=%r, FileKnob=%r, IntKnob=%r, EnumKnob=%r, BitMaskKnob=%r, BoolKnob=%r, DoubleKnob=%r, FloatKnob=%r, ArrayKnob=%r, ChannelMaskKnob=%r, ChannelKnob=%r, XYKnob=%r, XYZKnob=%r, WHKnob=%r, BBoxKnob=%r, SizeKnob=%r, FormatKnob=%r, ColorKnob=%r, AColorKnob=%r, TabKnob=%r, CustomKnob=%r, PyScriptKnob=%r, TextEditorKnob=%r, Transform2DKnob=%r, SpacerKnob=%r, TextKnob=%r, HelpKnob=%r, MultilineStringKnob=%r, AxisKnob=%r, UVKnob=%r, Box3Knob=%r, ScriptKnob=%r, LookupCurvesKnob=%r, TooltipKnob=%r, PulldownKnob=%r, EyeDropperKnob=%r, RangeKnob=%r, HistogramKnob=%r, KeyerKnob=%r, ColorChipKnob=%r, LinkKnob=%r, ScaleKnob=%r, MultilineEvalStringKnob=%r, OneViewKnob=%r, MultiViewKnob=%r, ViewViewKnob=%r, PyPulldownKnob=%r, GPUEngineKnob=%r, MultiArrayKnob=%r, ViewPairKnob=%r, ListKnob=%r, PythonKnob=%r, MetaDataKnob=%r, PixelAspectKnob=%r, CpKnob=%r, ToolbarKnob=%r, TabGroupKnob=%r, PluginPythonKnob=%r, ExoGroupKnob=%r, MenuKnob=%r, PasswordKnob=%r, ToolboxKnob=%r, TableKnob=%r, InputOnlyChannelMaskKnob=%r, InputOnlyChannelKnob=%r)' % self

	def _asdict(t):
		'Return a new dict which maps field names to their values'
		return {'ObsoleteKnob': t[0], 'StringKnob': t[1], 'FileKnob': t[2], 'IntKnob': t[3], 'EnumKnob': t[4], 'BitMaskKnob': t[5], 'BoolKnob': t[6], 'DoubleKnob': t[7], 'FloatKnob': t[8], 'ArrayKnob': t[9], 'ChannelMaskKnob': t[10], 'ChannelKnob': t[11], 'XYKnob': t[12], 'XYZKnob': t[13], 'WHKnob': t[14], 'BBoxKnob': t[15], 'SizeKnob': t[16], 'FormatKnob': t[17], 'ColorKnob': t[18], 'AColorKnob': t[19], 'TabKnob': t[20], 'CustomKnob': t[21], 'PyScriptKnob': t[22], 'TextEditorKnob': t[23], 'Transform2DKnob': t[24], 'SpacerKnob': t[25], 'TextKnob': t[26], 'HelpKnob': t[27], 'MultilineStringKnob': t[28], 'AxisKnob': t[29], 'UVKnob': t[30], 'Box3Knob': t[31], 'ScriptKnob': t[32], 'LookupCurvesKnob': t[33], 'TooltipKnob': t[34], 'PulldownKnob': t[35], 'EyeDropperKnob': t[36], 'RangeKnob': t[37], 'HistogramKnob': t[38], 'KeyerKnob': t[39], 'ColorChipKnob': t[40], 'LinkKnob': t[41], 'ScaleKnob': t[42], 'MultilineEvalStringKnob': t[43], 'OneViewKnob': t[44], 'MultiViewKnob': t[45], 'ViewViewKnob': t[46], 'PyPulldownKnob': t[47], 'GPUEngineKnob': t[48], 'MultiArrayKnob': t[49], 'ViewPairKnob': t[50], 'ListKnob': t[51], 'PythonKnob': t[52], 'MetaDataKnob': t[53], 'PixelAspectKnob': t[54], 'CpKnob': t[55], 'ToolbarKnob': t[56], 'TabGroupKnob': t[57], 'PluginPythonKnob': t[58], 'ExoGroupKnob': t[59], 'MenuKnob': t[60], 'PasswordKnob': t[61], 'ToolboxKnob': t[62], 'TableKnob': t[63], 'InputOnlyChannelMaskKnob': t[64], 'InputOnlyChannelKnob': t[65]}

	def _replace(_self, **kwds):
		'Return a new KnobTypes object replacing specified fields with new values'
		result = _self._make(list(map(kwds.pop, ('ObsoleteKnob', 'StringKnob', 'FileKnob', 'IntKnob', 'EnumKnob', 'BitMaskKnob', 'BoolKnob', 'DoubleKnob', 'FloatKnob', 'ArrayKnob', 'ChannelMaskKnob', 'ChannelKnob', 'XYKnob', 'XYZKnob', 'WHKnob', 'BBoxKnob', 'SizeKnob', 'FormatKnob', 'ColorKnob', 'AColorKnob', 'TabKnob', 'CustomKnob', 'PyScriptKnob', 'TextEditorKnob', 'Transform2DKnob', 'SpacerKnob', 'TextKnob', 'HelpKnob', 'MultilineStringKnob', 'AxisKnob', 'UVKnob', 'Box3Knob', 'ScriptKnob', 'LookupCurvesKnob', 'TooltipKnob', 'PulldownKnob', 'EyeDropperKnob', 'RangeKnob', 'HistogramKnob', 'KeyerKnob', 'ColorChipKnob', 'LinkKnob', 'ScaleKnob', 'MultilineEvalStringKnob', 'OneViewKnob', 'MultiViewKnob', 'ViewViewKnob', 'PyPulldownKnob', 'GPUEngineKnob', 'MultiArrayKnob', 'ViewPairKnob', 'ListKnob', 'PythonKnob', 'MetaDataKnob', 'PixelAspectKnob', 'CpKnob', 'ToolbarKnob', 'TabGroupKnob', 'PluginPythonKnob', 'ExoGroupKnob', 'MenuKnob', 'PasswordKnob', 'ToolboxKnob', 'TableKnob', 'InputOnlyChannelMaskKnob', 'InputOnlyChannelKnob'), _self)))
		if kwds:
			raise ValueError('Got unexpected field names: %r' % list(kwds.keys()))
		return result

	def __getnewargs__(self):
		return tuple(self)

	ObsoleteKnob = property(_itemgetter(0))
	StringKnob = property(_itemgetter(1))
	FileKnob = property(_itemgetter(2))
	IntKnob = property(_itemgetter(3))
	EnumKnob = property(_itemgetter(4))
	BitMaskKnob = property(_itemgetter(5))
	BoolKnob = property(_itemgetter(6))
	DoubleKnob = property(_itemgetter(7))
	FloatKnob = property(_itemgetter(8))
	ArrayKnob = property(_itemgetter(9))
	ChannelMaskKnob = property(_itemgetter(10))
	ChannelKnob = property(_itemgetter(11))
	XYKnob = property(_itemgetter(12))
	XYZKnob = property(_itemgetter(13))
	WHKnob = property(_itemgetter(14))
	BBoxKnob = property(_itemgetter(15))
	SizeKnob = property(_itemgetter(16))
	FormatKnob = property(_itemgetter(17))
	ColorKnob = property(_itemgetter(18))
	AColorKnob = property(_itemgetter(19))
	TabKnob = property(_itemgetter(20))
	CustomKnob = property(_itemgetter(21))
	PyScriptKnob = property(_itemgetter(22))
	TextEditorKnob = property(_itemgetter(23))
	Transform2DKnob = property(_itemgetter(24))
	SpacerKnob = property(_itemgetter(25))
	TextKnob = property(_itemgetter(26))
	HelpKnob = property(_itemgetter(27))
	MultilineStringKnob = property(_itemgetter(28))
	AxisKnob = property(_itemgetter(29))
	UVKnob = property(_itemgetter(30))
	Box3Knob = property(_itemgetter(31))
	ScriptKnob = property(_itemgetter(32))
	LookupCurvesKnob = property(_itemgetter(33))
	TooltipKnob = property(_itemgetter(34))
	PulldownKnob = property(_itemgetter(35))
	EyeDropperKnob = property(_itemgetter(36))
	RangeKnob = property(_itemgetter(37))
	HistogramKnob = property(_itemgetter(38))
	KeyerKnob = property(_itemgetter(39))
	ColorChipKnob = property(_itemgetter(40))
	LinkKnob = property(_itemgetter(41))
	ScaleKnob = property(_itemgetter(42))
	MultilineEvalStringKnob = property(_itemgetter(43))
	OneViewKnob = property(_itemgetter(44))
	MultiViewKnob = property(_itemgetter(45))
	ViewViewKnob = property(_itemgetter(46))
	PyPulldownKnob = property(_itemgetter(47))
	GPUEngineKnob = property(_itemgetter(48))
	MultiArrayKnob = property(_itemgetter(49))
	ViewPairKnob = property(_itemgetter(50))
	ListKnob = property(_itemgetter(51))
	PythonKnob = property(_itemgetter(52))
	MetaDataKnob = property(_itemgetter(53))
	PixelAspectKnob = property(_itemgetter(54))
	CpKnob = property(_itemgetter(55))
	ToolbarKnob = property(_itemgetter(56))
	TabGroupKnob = property(_itemgetter(57))
	PluginPythonKnob = property(_itemgetter(58))
	ExoGroupKnob = property(_itemgetter(59))
	MenuKnob = property(_itemgetter(60))
	PasswordKnob = property(_itemgetter(61))
	ToolboxKnob = property(_itemgetter(62))
	TableKnob = property(_itemgetter(63))
	InputOnlyChannelMaskKnob = property(_itemgetter(64))
	InputOnlyChannelKnob = property(_itemgetter(65))
#----------------------------------------------------------------------
def None_To_SelectedNode(val):
	"""Simple Function That Checks If the Input arg val == None or is not instance of nuke.Node set The val to the last selected node"""
	import nuke
	if not isinstance(val,nuke.Node) or val == None:
		val = nuke.selectedNode()
	return val
#----------------------------------------------------------------------
def None_To_Selected(val):
	"""Simple Function That Checks If the Input arg val == None or is not list of nuke.Nodes then setd The val to the selected nodes"""
	import nuke
	if val == None:
		val = nuke.selectedNodes()
	return val
#----------------------------------------------------------------------
def find_common_knobs(nodelist=None):
	"""Returns knobs That Are Found On all the nodes in nodelist"""

	# If nodelist is equal to None then set nodelist to the currently selected Nodes
	nodelist = None_To_Selected(nodelist)
	# Storge list for All Commom Knobs
	common_Knobs = []


	def build_knob_sets(nodelist):
		# Storage list that will containe list
		# for knobs for each nodetype found in nodelist
		knob_sets = []
		# Stoarge list that will cantaine nodeTypes
		# That have already had there knobs collected
		scaned_Types = []
		for nod in nodelist:

			if not nod.Class() in scaned_Types:

				scaned_Types.append(nod.Class())
				knbs = list(nod.knobs().values())
				knob_sets.append(knbs)

		return knob_sets
	knob_sets = build_knob_sets(nodelist)

	for knbs in knob_sets:

		for item in knbs:

			addItem = True

			for single_set in knob_sets:

				if not item.name() in [k.name() for k in single_set]:

					addItem = False
					break

			if addItem and not item.name() in [k.name() for k in common_Knobs] and not item.Class() == "Obsolete_Knob":
				common_Knobs.append(item)

	return common_Knobs
#----------------------------------------------------------------------
def link_common_knob_names(master=None,nodes=None,exclude_names=[],include_names=[]):
	nodes = None_To_Selected(nodes)
	master = None_To_SelectedNode()
	if master in nodes:
		nodes.remove(master)

	for knb in common_knobs.find_common_knobs(nodes+[master]):
		if not knb.name() in exclude_names and knb.name() in include_names:
			for n in nodes:
				try:
					n.knob(knb.name()).setExpression( master.fullName() + "." + knb.name() )
				except:
					print("Could not Set Expression for knob %s from master Node %s to slave node %s" % (knb.name(),master.name(),n.name()))
#----------------------------------------------------------------------
def Copy_common_knob_names(master=None,nodes=None,exclude_names=[],include_names=[]):
	nodes = None_To_Selected(nodes)
	master = None_To_SelectedNode()
	if master in nodes:
		nodes.remove(master)

	for knb in common_knobs.find_common_knobs(nodes+[master]):
		if not knb.name() in exclude_names and knb.name() in include_names:
			for n in nodes:
				try:
					n.knob(knb.name()).fromScript(master.knob(knb.name()).toScript())
				except:
					print("Could not Copy knob %s from master Node %s to slave node %s" % (knb.name(),master.name(),n.name()))
#----------------------------------------------------------------------
def get_knob_Class(knobs):
	import nuke
	return [n.Class() for n in knobs if isinstance(n,nuke.Knob)]
#----------------------------------------------------------------------
def get_knob_names(knobs):
	import nuke
	return [n.name() for n in knobs if isinstance(n,nuke.Knob)]
