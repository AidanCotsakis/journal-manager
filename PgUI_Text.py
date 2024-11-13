from PgUI_Cell import *
from PgUI_Settings import *
import pygame
import clipboard

class PgUI_Text(PgUI_Cell):
	def __init__(self, parent, col, row, width, height, margins, text, size = 24, colour = "Default", editable = False, horizontalAlign = "left", verticalAlign = "top", bold = False, italic = False, censored = False, searchable = True, enabled = True, link = None, tag = ""):
		super().__init__(parent = parent, col = col, row = row, width = width, height = height, margins = margins, enabled = enabled, tag = tag)
		self.text = text

		self.size = size # int/float of font size in pixels
		
		if colour == "Default":
			self.colour = COLOURS["White"]
		elif type(colour) == str:
			self.colour = COLOURS[colour]
		else:
			self.colour = colour

		self.editable = editable # true or false if the user can click and type in the box
		self.bold = bold
		self.italic = italic

		self.selectFont()

		self.horizontalAlign = horizontalAlign
		self.verticalAlign = verticalAlign

		self.typeLineFrames = 30 #number of frames per cycle of the type bar 

		# self.renderedFont = self.font.render(self.text, True, self.colour)

		self.selected = False
		self.ticker = 0

		self.heldKey = None # [key, unicode/letter, tickerTime]
		self.heldKeyDelay = 15 #ticks for the key to be held and repeatedly entered

		self.censored = censored
		self.searchable = searchable
		self.link = link

		self.surface = None

	def selectFont(self):
		if self.bold and self.italic: self.path = FONT_BOLD_ITALIC
		elif self.bold: self.path = FONT_BOLD
		elif self.italic: self.path = FONT_ITALIC
		else: self.path = FONT
		self.font = pygame.font.Font(self.path, self.size) # make pygame font object

	def renderSurface(self, ignoreDynamic = False):
		self.surface = pygame.Surface([self.width_px, self.height_px], pygame.SRCALPHA, 32).convert_alpha()

		# FIND WHERE EACH LINE SHPOULD BE
		textBreaks = self.text.split("\n")

		textLines = []
		# break each newline and wrap text if it is greater than the surface size
		for textBreak in textBreaks:
			words = textBreak.split(" ")

			if self.censored:
				words = ["*" * len(i) for i in words]

			textLine = [words[0]]
			for word in words[1:]:
				textLine.append(word)
				if self.font.render(" ".join(textLine), True, self.colour).get_size()[0] > self.surface.get_size()[0]:
					textLines.append(" ".join(textLine[:-1]))
					textLine = [word]
			
			textLines.append(" ".join(textLine))

		renderedLines = []
		# render all the final text lines
		for textLine in textLines:
			renderedLines.append(self.font.render(textLine, True, self.colour))

		# find the height each line should be
		lineHeight = 0
		for renderedLine in renderedLines:
			if renderedLine.get_size()[1] > lineHeight:
				lineHeight = renderedLine.get_size()[1]

		totalHeight = lineHeight*len(renderedLines)

		lastLineOffset = [0,0]

		# paste the rendered text lines onto the surface depending on the chosen alignment
		for renderedLine in enumerate(renderedLines):
			offset = [0,0]

			if self.horizontalAlign == "mid":
				offset[0] = int(self.surface.get_size()[0]/2 - renderedLine[1].get_size()[0]/2)
			elif self.horizontalAlign == "right":
				offset[0] = int(self.surface.get_size()[0] - renderedLine[1].get_size()[0])

			if self.verticalAlign == "top":
				offset[1] = lineHeight*renderedLine[0]
			elif self.verticalAlign == "mid":
				offset[1] = lineHeight*renderedLine[0] + int(self.surface.get_size()[1]/2 - totalHeight/2)
			elif self.verticalAlign == "bottom":
				offset[1] = lineHeight*renderedLine[0] + int(self.surface.get_size()[1] - totalHeight)

			self.surface.blit(renderedLine[1], offset)

			self.lastLineOffset = [offset[0] + renderedLine[1].get_size()[0], offset[1]]

		self.lineHeight = lineHeight

	def handleClicks(self, pos, left = False, right = False):
		if self.enabled and self.inView:
			if left:
				clicked = pointBoxCollision(pos, self.box) and self.editable

				if clicked and not self.selected:
					self.selected = True

				elif self.editable and self.selected and not clicked:
					self.selected = False
					self.ticker = 0

				return clicked
			return False
		else:
			return False

	def handleKeys(self, key, letter):
		if self.selected:
			if key == pygame.K_BACKSPACE and len(self.text) >= 1:
				self.text = self.text[:-1]
			elif key == pygame.K_RETURN:
				self.text += "\n"
			elif letter in VALID_CHARACTERS:
				self.text += letter
			elif key == 98: #bold
				self.bold = not self.bold
				self.selectFont()
			elif key == 105: #italic
				self.italic = not self.italic
				self.selectFont()
			elif key == 99: #copy
				clipboard.copy(self.text)
				self.heldKey = None
			elif key == 118: #paste
				self.text += clipboard.paste()
				self.heldKey = None

			self.renderSurface()

	def handleKeyPress(self, key, letter):
		if self.enabled and self.inView:
			if self.selected:
				self.heldKey = [key, letter, self.ticker]
				self.handleKeys(key, letter)

	def handleKeyRelease(self, key, letter):
		if self.enabled and self.inView:
			if self.heldKey != None and self.heldKey[:-1] == [key, letter]:
				self.heldKey = None

	def handleSelected(self):
		if self.enabled and self.inView:
			self.ticker += 1

			if self.heldKey != None and self.ticker - self.heldKey[2] >= self.heldKeyDelay:
				self.handleKeys(self.heldKey[0], self.heldKey[1])

	def search(self, string):
		return self.searchable and string.lower() in self.text.lower()

	def handleLink(self):
		if self.link and self.link.text != self.text:
			self.text = self.link.text
			self.renderSurface()

	def draw(self):
		if self.enabled and self.inView:
			if not self.surface:
				self.renderSurface()

			self.handleLink()

			if self.moved:
				self.xPos_px = self.parent.xPos_px + self.xOffsetFromParent_px
				self.yPos_px = self.parent.yPos_px + self.yOffsetFromParent_px
				self.box = (self.xPos_px, self.yPos_px, self.width_px, self.height_px)
				self.moved = False
			
			self.win.blit(self.surface, (self.xPos_px, self.yPos_px))

			if self.selected:
				self.handleSelected()

			if self.selected and self.ticker % self.typeLineFrames < self.typeLineFrames/2:
				pygame.draw.rect(self.win, self.colour, (self.xPos_px + self.lastLineOffset[0], self.yPos_px + self.lastLineOffset[1], 2, int(self.lineHeight*0.85)))