from PgUI_Container import *

pygame.init()

class PgUI(PgUI_Container):
	def __init__(self, win, width_px, height_px, cols, rows):
		self.win = win

		self.width_px = width_px
		self.height_px = height_px

		self.childWidth_px = self.width_px
		self.childHeight_px = self.height_px

		self.depth = -1

		super().__init__(self, col = 0, row = 0, width = 1, height = 1, cols = cols, rows = rows, margins = MARGINS, colour = CONTAINER_COLOUR)

	def tick(self):
		for event in pygame.event.get():
			pygame.event.post(event)
			if event.type == pygame.MOUSEBUTTONDOWN:
				mousePos = pygame.mouse.get_pos()
				# LEFT CLICK
				if event.button == 1:
					self.handleClicks(mousePos, left = True)
				# SCROLL UP
				if event.button == 4:
					self.handleScroll(mousePos, up = True)
				# SCROLL DOWN
				if event.button == 5:
					self.handleScroll(mousePos, down = True)

			if event.type == pygame.MOUSEBUTTONUP:
				mousePos = pygame.mouse.get_pos()
				# LEFT CLICK
				if event.button == 1:
					self.handleReleaseClicks(mousePos, left = True)

			if event.type == pygame.KEYDOWN:
				self.handleKeyPress(event.key, event.unicode)

			if event.type == pygame.KEYUP:
				self.handleKeyRelease(event.key, event.unicode)
