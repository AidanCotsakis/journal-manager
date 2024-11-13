import importlib

from PgUI_Cell import *
from PgUI_Settings import *
from PgUI_Text import *
from PgUI_Image import *
from PgUI_Slider import *
PgUI_Button = importlib.import_module('PgUI_Button')
PgUI_Container = importlib.import_module('PgUI_Container')
import pygame

class PgUI_List(PgUI_Cell):
	def __init__(self, parent, col, row, width, height, margins, rows, colour = "Default", searchBox = None, enabled = True, tag = ""):
		super().__init__(parent = parent, col = col, row = row, width = width, height = height, margins = margins, enabled = enabled, tag = tag)
		
		self.rows = rows
		self.searchBox = searchBox

		self.childWidth_px = self.width_px
		self.childHeight_px = int(self.height_px/self.rows)

		self.children = []

		self.prevSearch = "-"

		self.scrollAmount = 0

		self.numEnabled = 0

		if colour == "Default":
			fillValue = 20 + 10 * self.depth
			self.colour = (fillValue, fillValue, fillValue)
		elif type(colour) == str:
			self.colour = COLOURS[colour]
		else:
			self.colour = colour

	def add_container(self, col = 0, row = 0, width = 1, height = 1, margins = MARGINS, cols = 1, rows = 1, colour = CONTAINER_COLOUR, enabled = True, tag = ""):
		container = PgUI_Container.PgUI_Container(self, col = col, row = row, width = width, height = height, margins = margins, cols = cols, rows = rows, colour = colour, enabled = enabled, tag = tag)
		self.children.append(container)
		return container

	def add_button(self, col = 0, row = 0, width = 1, height = 1, margins = MARGINS, onPress = None, colour = BUTTON_COLOUR, args = [], link = None, enabled = True, tag = ""):
		button = PgUI_Button.PgUI_Button(self, col = col, row = row, width = width, height = height, margins = margins, onPress = onPress, colour = colour, args = args, link = link, enabled = enabled, tag = tag)
		self.children.append(button)
		return button

	def add_text(self, col = 0, row = 0, width = 1, height = 1, margins = MARGINS, text = "", size = 24, colour = TEXT_COLOUR, editable = False, horizontalAlign = "left", verticalAlign = "top", bold = False, italic = False, censored = False, searchable = True, enabled = True, link = None, tag = ""):
		text = PgUI_Text(self, col = col, row = row, width = width, height = height, margins = margins, text = text, size = size, colour = colour, editable = editable, horizontalAlign = horizontalAlign, verticalAlign = verticalAlign, bold = bold, italic = italic, censored = censored, searchable = searchable, enabled = enabled, link = link, tag = tag)
		self.children.append(text)
		return text

	def add_image(self, col = 0, row = 0, width = 1, height = 1, margins = MARGINS, path = "", enabled = True, tag = ""):
		image = PgUI_Image(self, col = col, row = row, width = width, height = height, margins = margins, path = path, enabled = enabled, tag = tag)
		self.children.append(image)
		return image

	def add_slider(self, col = 0, row = 0, width = 1, height = 1, margins = MARGINS, value = 0.5, railColour = RAIL_COLOUR, thumbColour = THUMB_COLOUR, enabled = True, tag = ""):
		slider = PgUI_Slider(self, col = col, row = row, width = width, height = height, margins = margins, value = value, railColour = railColour, thumbColour = thumbColour, enabled = enabled, tag = tag)
		self.children.append(slider)
		return slider

	def add_list(self, col = 0, row = 0, width = 1, height = 1, margins = MARGINS, rows = 1, colour = LIST_COLOUR, searchBox = None, enabled = True, tag = ""):
		listBox = PgUI_List(self, col = col, row = row, width = width, height = height, margins = margins, rows = rows, colour = colour, searchBox = searchBox, enabled = enabled, tag = tag)
		self.children.append(listBox)
		return listBox

	def handleClicks(self, pos, left = False, right = False):
		if self.enabled and self.inView:
			clicked = False
			for child in self.children:
				clicked = child.handleClicks(pos, left, right) == True or clicked

			return clicked
		else:
			return False

	def handleReleaseClicks(self, pos, left = False, right = False):
		if self.enabled and self.inView:
			clicked = False
			for child in self.children:
				clicked = child.handleReleaseClicks(pos, left, right) == True or clicked

			return clicked
		else:
			return False

	def search(self, string):
		found = False
		for child in self.children:
			found = child.search(string) == True or found

		return found

	def handleKeyPress(self, key, letter):
		if self.enabled and self.inView:
			for child in self.children:
				child.handleKeyPress(key, letter)

	def handleKeyRelease(self, key, letter):
		if self.enabled and self.inView:
			for child in self.children:
				child.handleKeyRelease(key, letter)	

	def handleSearch(self):
		if self.searchBox and self.searchBox.enabled and self.searchBox.text != self.prevSearch:
			self.prevSearch = self.searchBox.text
			self.numEnabled = 0
			if self.searchBox.text == "":
				for child in self.children:
					child.enabled = True
					self.numEnabled += 1
			else:
				for child in self.children:
					child.enabled = child.search(self.searchBox.text)
					if child.enabled:
						self.numEnabled += 1
			self.scrollAmount = max(0, self.numEnabled - self.rows) 
			self.rePosition()

	def handleScroll(self, pos, up = False, down = False):
		scrolled = False
		if self.enabled and self.inView:
			for child in self.children:
				scrolled = child.handleScroll(pos, up, down) == True or scrolled

		if not scrolled:
			if pointBoxCollision(pos, self.box):
				scrolled = True
				if down and self.scrollAmount + self.rows < self.numEnabled:
					self.scrollAmount += 1
				elif up and self.scrollAmount > 0:
					self.scrollAmount -= 1

				self.rePosition()

		return scrolled

	def rePosition(self):
		i = 0
		for child in self.children:
			if child.enabled:
				if i >= self.scrollAmount and i < self.scrollAmount + self.rows:
					child.inView = True
					child.row_g = i - self.scrollAmount
					child.yOffsetFromParent_px = self.childHeight_px * child.row_g + child.margins
					child.moved = True
				else:
					child.inView = False
				i += 1

	def draw(self):
		if self.enabled and self.inView:
			
			self.handleSearch()

			if self.moved:
				self.xPos_px = self.parent.xPos_px + self.xOffsetFromParent_px
				self.yPos_px = self.parent.yPos_px + self.yOffsetFromParent_px
				self.box = (self.xPos_px, self.yPos_px, self.width_px, self.height_px)
				self.moved = False
				for child in self.children:
					child.moved = True
			
			if self.colour != None:
				pygame.draw.rect(self.win, self.colour, (self.xPos_px, self.yPos_px, self.width_px, self.height_px), border_radius=5)

			for child in self.children:
				child.draw()