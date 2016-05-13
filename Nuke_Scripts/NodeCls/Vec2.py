
import nuke
from _nukemath import Vector2 as VEC2
class Vector2(VEC2):

	def __init__(self,*args):
		if len(args) == 1 and isinstance(args[0],nuke.Node):
			args = float(args[0].xpos()),float(args[0].ypos())
		return super(Vector2,self).__init__(*args)

	def cross(self, *args):
		"""cross( (Vector2)arg1, (Vector2)arg2) -> float :"""
		return super(Vector2,self).cross(*args)

	def distanceBetween(self,*args):
		"""distanceBetween( (Vector2)arg1, (Vector2)arg2) -> float :"""
		return super(Vector2,self).distanceBetween(*args)

	def distanceSquared(self,*args):
		"""distanceSquared( (Vector2)arg1, (Vector2)arg2) -> float :"""
		return super(Vector2,self).distanceSquared(*args)

	def dot(self,*args):
		"""dot( (Vector2)arg1, (Vector2)arg2) -> float :"""
		return super(Vector2,self).dot(*args)

	def length(self):
		"""length( (Vector2)arg1) -> float :"""
		return super(Vector2,self).length()

	def lengthSquared(self):
		"""lengthSquared( (Vector3)arg1) -> float :"""
		return super(Vector2,self).lengthSquared()

	def negate(self):
		"""negate( (Vector2)arg1) -> None :"""
		return super(Vector2,self).negate()

	def normalize(self):
		"""normalize( (Vector2)arg1) -> float :"""
		return super(Vector2,self).normalize()

	def set(*args):
		"""set( (Vector2)arg1, (float)arg2) -> None :
		set( (Vector2)arg1, (float)arg2, (float)arg3) -> None :
		set( (Vector2)arg1, (Vector2)arg2) -> None :"""
		return super(Vector2,self).set(*args)