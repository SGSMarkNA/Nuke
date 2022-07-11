import nuke
from .Group import Group
class Root(Group):

	def __init__(self):
		Group.__init__(self,nuke.root())

	@property
	def lastFrame(self):
		"""self.lastFrame() -> Integer. Last frame. @return: Integer."""
		return self_node.lastFrame()

	@property
	def maximumInputs(self):
		""""""
		return self_node.maximumInputs()

	@property
	def modified(self):
		"""self.modified() -> True if modified, False otherwise. Get or set the 'modified' flag in a script @return: True if modified, False otherwise."""
		return self_node.modified()

	@property
	def channels(self):
		"""nuke.Root.channels() -> Channel list. Class method. @return: Channel list."""
		return self_node.channels()

	@property
	def firstFrame(self):
		"""self.firstFrame() -> Integer. First frame. @return: Integer."""
		return self_node.firstFrame()

	@property
	def layers(self):
		"""nuke.Root.layers() -> Layer list. Class method. @return: Layer list."""
		return self_node.layers()

	@property
	def fps(self):
		"""self.fps() -> Integer. FPS. @return: Integer."""
		return self_node.fps()

	@property
	def proxy(self):
		"""self.proxy() -> True if proxy is set, False otherwise. @return: True if proxy is set, False otherwise."""
		return self_node.proxy()

	@property
	def clones(self):
		""""""
		return self_node.clones()

	#def setProxy(self,b):
	#    """self.setProxy(b) -> None. Set proxy. @param b: Boolean convertible object. @return: None."""
	#    return self_node.setProxy(b)
	#
	#def addView(self,s):
	#    """self.addView(s) -> None. Add view. @param s: Name of view. @return: None."""
	#    return self_node.addView(s)
	#
	#
	#def deleteView(self,s):
	#    """self.deleteView(s) -> None. Delete view. @param s: Name of view. @return: None."""
	#    return self_node.deleteView(s)
	#
	#
	#def mergeFrameRange(self):
	#    """self.mergeFrameRange(a, b) -> None. Merge frame range. @param a: Low-end of interval range. @param b: High-end of interval range. @return: None."""
	#    return self_node.mergeFrameRange()
	#
	#
	#def setModified(self,b):
	#    """self.setModified(b) -> None. Set the 'modified' flag in a script. Setting the value will turn the indicator in the title bar on/off and will start or stop the autosave timeout. @param b: Boolean convertible object. @return: None."""
	#    return self_node.setModified(b)
	#
	#def setView(self,s):
	#    """self.setView(s) -> None. Set view. @param s: Name of view. @return: None."""
	#    return self_node.setView(s)
	#
	#
	#def setFrame(self,n):
	#    """self.setFrame(n) -> None. Set frame. @param n: Frame number. @return: None."""
	#    return self_node.setFrame(n)
	#
	#
	#def optionalInput(self):
	#    """"""
	#    return self_node.optionalInput()