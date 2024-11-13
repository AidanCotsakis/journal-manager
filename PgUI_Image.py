from PgUI_Cell import *
from PgUI_Settings import *
import pygame

class PgUI_Image(PgUI_Cell):
	def __init__(self, parent, col, row, width, height, margins, path, enabled = True, tag = ""):
		super().__init__(parent = parent, col = col, row = row, width = width, height = height, margins = margins, enabled = enabled, tag = tag)
		
		self.path = path
		self.image = None

	def loadImage(self):
		image = pygame.image.load(self.path)
		imWidth = image.get_width()
		imHeight = image.get_height()

		widthScaleFactor = self.width_px / imWidth 
		heightScaleFactor = self.height_px / imHeight

		scaleFactor = min(widthScaleFactor, heightScaleFactor)

		newSize = (int(imWidth * scaleFactor), int(imHeight * scaleFactor))

		self.image = pygame.transform.smoothscale(image, newSize)
		self.xDrawOffset_px = int(self.width_px/2 - self.image.get_width()/2)
		self.yDrawOffset_px = int(self.height_px/2 - self.image.get_height()/2)


	def draw(self):
		if self.enabled and self.inView:
			if not self.image:
				self.loadImage()

			if self.moved:
				self.xPos_px = self.parent.xPos_px + self.xOffsetFromParent_px
				self.yPos_px = self.parent.yPos_px + self.yOffsetFromParent_px
				self.box = (self.xPos_px, self.yPos_px, self.width_px, self.height_px)
				self.moved = False

			self.win.blit(self.image, (self.xPos_px + self.xDrawOffset_px, self.yPos_px + self.yDrawOffset_px))


		