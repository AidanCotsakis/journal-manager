from PgUI_Settings import *

class PgUI_Cell():
	def __init__(self, parent, col, row, width, height, margins, enabled, tag):
		self.parent = parent
		self.col_g = col # grid col (starting from 0)
		self.row_g = row # grid row (starting from 0)
		self.width_g = width # number of grid cells in width
		self.height_g = height # number of grid cells in height
		self.margins = margins

		self.win = self.parent.win

		self.xOffsetFromParent_px = self.parent.childWidth_px * self.col_g + self.margins
		self.yOffsetFromParent_px = self.parent.childHeight_px * self.row_g + self.margins
		self.width_px = self.parent.childWidth_px * self.width_g - self.margins * 2
		self.height_px = self.parent.childHeight_px * self.height_g - self.margins * 2
		self.xPos_px = 0
		self.yPos_px = 0

		self.depth = self.parent.depth + 1
		self.moved = True

		self.enabled = enabled
		self.inView = True

		self.box = (0,0,0,0)

		self.tag = tag

	def handleClicks(self, pos, left = False, right = False):
		return False

	def handleReleaseClicks(self, pos, left = False, right = False):
		return False

	def handleKeyPress(self, key, letter):
		pass

	def handleKeyRelease(self, key, letter):
		pass

	def draw(self):
		pass

	def search(self, string):
		return False

	def handleScroll(self, pos, up = False, down = False):
		return False