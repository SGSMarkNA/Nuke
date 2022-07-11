from . import Vec2

class Node_List(list):
	@property
	def center(self):
		Xpositions = [ n.xpos()+n.screenWidth()/2 for n in self]
		Ypositions = [ n.ypos()+n.screenHeight()/2 for n in self]
		try:
			x = float( sum( Xpositions ) ) / len( self )
			y = float( sum( Ypositions ) ) / len( self )
			return Vec2.Vector2(x,y)
		except ZeroDivisionError:
			return Vec2.Vector2(0,0)