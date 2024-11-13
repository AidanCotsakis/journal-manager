from PgUI_Cell import *
from PgUI_Settings import *
import pygame

class PgUI_Slider(PgUI_Cell):
	def __init__(self, parent, col, row, width, height, margins, enabled = True, value = 0.5, railColour = RAIL_COLOUR, thumbColour = THUMB_COLOUR, tag = ""):
		super().__init__(parent = parent, col = col, row = row, width = width, height = height, margins = margins, enabled = enabled, tag = tag)
		
		self.value = value

		self.thumbRadius = 10
		
		self.length = self.width_px - self.thumbRadius * 2
		self.thumbOffset = self.length * self.value

		self.clicked = False

		self.midOffset_px = int(self.height_px/2)
		self.halfRailWidth = 3

		if railColour == "Default":
			fillValue = 20 + 10 * self.depth
			self.railColour = (fillValue, fillValue, fillValue)
		elif type(railColour) == str:
			self.railColour = COLOURS[railColour]
		else:
			self.railColour = railColour

		if thumbColour == "Default":
			fillValue = 20 + 10 * self.depth
			self.thumbColour = COLOURS["White"]
		elif type(thumbColour) == str:
			self.thumbColour = COLOURS[thumbColour]
		else:
			self.thumbColour = thumbColour

	def handleClicks(self, pos, left = False, right = False):
		if self.enabled and self.inView and left:
			self.clicked = pointBoxCollision(pos, self.box)

		return self.clicked

	def handleReleaseClicks(self, pos, left = False, right = False):
		if self.clicked:
			self.clicked = False
			return True
		else:
			return False

	def handleHold(self):
		if self.clicked:
			mouseX, _ = pygame.mouse.get_pos()

			xDiff = self.xPos_px + self.thumbRadius

			self.value = (mouseX - xDiff)/self.length
			self.value = max(0.0, self.value)
			self.value = min(1.0, self.value)

	def draw(self):
		if self.enabled and self.inView:

			if self.moved:
				self.xPos_px = self.parent.xPos_px + self.xOffsetFromParent_px
				self.yPos_px = self.parent.yPos_px + self.yOffsetFromParent_px
				self.box = (self.xPos_px, self.yPos_px, self.width_px, self.height_px)
				self.moved = False

			self.handleHold()

			# self.win.blit(self.image, (self.xPos_px + self.xDrawOffset_px, self.yPos_px + self.yDrawOffset_px))
			pygame.draw.rect(self.win, self.railColour, (self.xPos_px + self.thumbRadius, self.yPos_px + self.midOffset_px - self.halfRailWidth, self.length, self.halfRailWidth * 2 + 1), 0, self.halfRailWidth + 1)
			pygame.draw.circle(self.win, self.thumbColour, (self.xPos_px + self.thumbRadius + int(self.value * self.length), self.yPos_px + self.midOffset_px), self.thumbRadius)