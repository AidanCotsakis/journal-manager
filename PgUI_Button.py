import importlib

from PgUI_Cell import *
from PgUI_Settings import *
from PgUI_Text import *
from PgUI_Image import *
from PgUI_Slider import *
PgUI_List = importlib.import_module('PgUI_List')
PgUI_Container = importlib.import_module('PgUI_Container')
import pygame

class PgUI_Button(PgUI_Cell):
	def __init__(self, parent, col, row, width, height, margins, onPress, colour = "Default", args = None, link = None, enabled = True, tag = ""):
		super().__init__(parent = parent, col = col, row = row, width = width, height = height, margins = margins, enabled = enabled, tag = tag)

		self.childWidth_px = self.width_px
		self.childHeight_px = self.height_px

		self.child = None

		self.onPress = onPress

		self.args = args

		self.link = link

		if colour == "Default":
			fillValue = 20 + 10 * self.depth
			self.colour = (fillValue, fillValue, fillValue)
		elif type(colour) == str:
			self.colour = COLOURS[colour]
		else:
			self.colour = colour

	def add_container(self, margins = MARGINS, cols = 1, rows = 1, colour = CONTAINER_COLOUR, enabled = True, tag = ""):
		container = PgUI_Container(self, col = 0, row = 0, width = 1, height = 1, margins = margins, cols = cols, rows = rows, colour = colour, enabled = enabled, tag = tag)
		self.child = container
		return container

	def add_list(self, margins = MARGINS, rows = 1, colour = LIST_COLOUR, searchBox = None, enabled = True, tag = ""):
		listBox = PgUI_List.PgUI_List(self, col = 0, row = 0, width = 1, height = 1, margins = margins, rows = rows, colour = colour, searchBox = searchBox, enabled = enabled, tag = tag)
		self.child = listBox
		return listBox

	def add_button(self, margins = MARGINS, onPress = None, colour = BUTTON_COLOUR, args = [], link = None, enabled = True, tag = ""):
		button = PgUI_Button.PgUI_Button(self, col = 0, row = 0, width = 1, height = 1, margins = margins, onPress = onPress, colour = colour, args = args, link = link, enabled = enabled, tag = tag)
		self.child = button
		return button

	def add_text(self, margins = MARGINS, text = "", size = 24, colour = TEXT_COLOUR, editable = False, horizontalAlign = "left", verticalAlign = "top", bold = False, italic = False, censored = False, searchable = True, enabled = True, link = None, tag = ""):
		text = PgUI_Text(self, col = 0, row = 0, width = 1, height = 1, margins = margins, text = text, size = size, colour = colour, editable = editable, horizontalAlign = horizontalAlign, verticalAlign = verticalAlign, bold = bold, italic = italic, censored = censored, searchable = searchable, enabled = enabled, link = link, tag = tag)
		self.child = text
		return text

	def add_slider(self, margins = MARGINS, value = 0.5, railColour = RAIL_COLOUR, thumbColour = THUMB_COLOUR, enabled = True, tag = ""):
		slider = PgUI_Slider(self, col = 0, row = 0, width = 1, height = 1, margins = margins, value = value, railColour = railColour, thumbColour = thumbColour, enabled = enabled, tag = tag)
		self.child = slider
		return slider

	def add_image(self, margins = MARGINS, path = "", enabled = True, tag = ""):
		image = PgUI_Image(self, col = 0, row = 0, width = 1, height = 1, margins = margins, path = path, enabled = enabled, tag = tag)
		self.child = image
		return image

	def handleClicks(self, pos, left = False, right = False):
		if self.enabled and self.inView:
			clicked = False
			if self.child:
				clicked = self.child.handleClicks(pos, left, right) == True or clicked

			if not clicked:
				clicked = pointBoxCollision(pos, self.box)
				
				if clicked:
					self.onPress(self, self.link, self.args)

			return clicked
		else:
			return False

	def handleReleaseClicks(self, pos, left = False, right = False):
		if self.enabled and self.inView:
			clicked = False
			if self.child:
				clicked = self.child.handleReleaseClicks(pos, left, right) == True or clicked

			return clicked
		else:
			return False

	def handleScroll(self, pos, up = False, down = False):
		if self.enabled and self.inView and self.child:
			return self.child.handleScroll(pos, up, down)
		return False

	def search(self, string):
		found = False
		if self.child:
			found = self.child.search(string) == True or found
		if self.link and not found:
			found = self.link.search(string) == True or found
		
		return found

	def handleKeyPress(self, key, letter):
		if self.enabled and self.inView and self.child:
			self.child.handleKeyPress(key, letter)

	def handleKeyRelease(self, key, letter):
		if self.enabled and self.inView and self.child:
			self.child.handleKeyRelease(key, letter)

	def draw(self):
		if self.enabled and self.inView:
			if self.moved:
				self.xPos_px = self.parent.xPos_px + self.xOffsetFromParent_px
				self.yPos_px = self.parent.yPos_px + self.yOffsetFromParent_px
				self.box = (self.xPos_px, self.yPos_px, self.width_px, self.height_px)
				self.moved = False
				if self.child:
					self.child.moved = True
			
			if self.colour != None:
				pygame.draw.rect(self.win, self.colour, (self.xPos_px, self.yPos_px, self.width_px, self.height_px), border_radius=5, width = 5)

			if self.child:
				self.child.draw()