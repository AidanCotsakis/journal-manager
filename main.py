import pygame
import PgUI
import os
from tkinter import *
from tkinter import filedialog
from datetime import datetime

# Image paths
NEW_IMAGE = "add_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"
EXIT_IMAGE = "close_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"
FORWARD_IMAGE = "arrow_forward_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"
BACK_IMAGE = "arrow_back_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"
DONE_IMAGE = "check_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"

pygame.init()

sentimentAnalysis = False

windowSize = (1920, 1080)

clock = pygame.time.Clock()
pygame.display.set_caption("Password Manager")
os.environ['SDL_VIDEO_CENTERED'] = '1'
win = pygame.display.set_mode(windowSize, pygame.NOFRAME)

UI = PgUI.PgUI(win, windowSize[0], windowSize[1], 9, 1)

# Used to read from the meta file, this stores sentiment analysis
def getMetaData():
	with open("files/meta.txt", "r") as f:
		content = f.read()
	meta = {}
	for row in content.split("\n"):
		if row == "": continue
		entries = row.strip().split(" ")
		date = entries[0]
		meta[date] = {}
		for entry in entries[1:]:
			split = entry.split(":")
			label = split[0]
			value = split[1]

			if label == "positive" or label == "negative":
				value = float(value)

			meta[date][label] = value

	return meta
if sentimentAnalysis:
	meta = getMetaData()

# Creates a page object
pages = []
def addPage(button = None, link = None, args = [], date = "", text = ""):
	col1 = UI.add_container(width = 8, enabled = False)
	col1_largeContainer = col1.add_container(rows = 15, cols = 8, colour = None)
	if os.path.exists(f"files/{date}.jpg"):
		col1_image = col1_largeContainer.add_image(path = f"files/{date}.jpg", width = 3, height = 15)
	else:
		col1_image = col1_largeContainer.add_image(path = f"files/NoPhoto.jpg", width = 3, height = 15)
	col1_title = col1_largeContainer.add_text(text = date, col = 3, bold = True, size = 48, colour = "Gold", margins = 0, width = 5, verticalAlign = "mid", horizontalAlign = "mid")
	col1_text = col1_largeContainer.add_text(text = text, col = 3, row = 1, height = 13, width = 5, verticalAlign = "mid")
	listButton = col2_list.add_button(onPress = enablePage, margins = 0, link = col1).add_text(text = date, colour = getSentimentColour(date), margins = 0, link = col1_title, verticalAlign = "mid", horizontalAlign = "mid").parent
	pages.append(col1)

# Focuses a page object and disables previously enabled page
enabledIndex = 0
enabledPage = None
def enablePage(button = None, link = None, args = []):
	global enabledPage, enabledIndex
	if enabledPage:
		enabledPage.enabled = False
	link.enabled = True
	enabledPage = link
	try:
		enabledIndex = pages.index(enabledPage)
	except:
		enabledIndex = len(pages) - 1

# Enables the next page
def nextPage(button, link, args):
	global enabledIndex
	newIndex = (enabledIndex + 1) % len(pages)
	page = pages[newIndex]
	enablePage(link = page)

# Enables the previous page
def prevPage(button, link, args):
	global enabledIndex
	newIndex = (enabledIndex + len(pages) - 1 ) % len(pages)
	page = pages[newIndex]
	enablePage(link = page)

# Exits the program
def quit(button, link, args):
	global loop

	loop = False

# Handles commiting a new entry
def finishNewEntry(button, link, args):
	date = args[0].text
	if date != "":
		text = args[1].text
		if text == "":
			text = "No Text"
		with open(f"files/{date}.txt", "w") as f:
			f.write(text)

		filetypes = (
		("JPG files", "*.jpg"),
		("All files", "*.*")
		)
		intitalImagePath = filedialog.askopenfilename(initialdir = "D://Downloads", filetypes=filetypes)
		if intitalImagePath != "":
			os.rename(intitalImagePath,f"files/{date}.jpg")

		addPage(date = date, text = text)
		enablePage(link = pages[-1])

# Handles seting up the page to enter a new entry
def promptNewEntry(button, link, args):
	current_date = datetime.now()
	formatted_date = current_date.strftime("%Y-%m-%d")
	col1 = UI.add_container(width = 8, enabled = False)
	col1_largeContainer = col1.add_container(rows = 15, cols = 8, colour = None)
	col1_title = col1_largeContainer.add_text(text = formatted_date, col = 3, bold = True, size = 48, colour = "Gold", margins = 0, width = 5, verticalAlign = "mid", horizontalAlign = "mid", editable = True)
	col1_text = col1_largeContainer.add_text(text = "", col = 3, row = 1, height = 13, width = 5, verticalAlign = "mid", editable = True)
	col1_image = col1_largeContainer.add_image(path = f"files/NoPhoto.jpg", width = 3, height = 15)
	enablePage(link = col1)
	col1_buttonContainer = col1_largeContainer.add_container(margins = 0, row = 14, col = 7, rows = 2, cols = 6, colour = None)
	col1_doneButton = col1_buttonContainer.add_button(onPress = finishNewEntry, margins = 0, row = 1, col = 5, colour = None, args = [col1_title, col1_text]).add_image(path = DONE_IMAGE, margins = 0).parent

# Returns a colour based on the pre cached sentiment analysis
def getSentimentColour(date):
	if sentimentAnalysis:
		if date not in meta:
			return (255,255,255)
		positive = meta[date]["positive"]
		negative = meta[date]["negative"]

		if positive > negative:
			scale = 1-(positive-0.5)
			return (255*scale,255,255*scale)
		elif negative > positive:
			scale = 1-(negative-0.5)
			return (255,255*scale,255*scale)
	return (255,255,255)

# Runs a sentiment analysis on each entry if it is not already in the meta file
def setMeta():
	imported = False

	for page in pages:
		date = page.children[0].children[1].text
		if date not in meta:
			text = page.children[0].children[2].text
			if text == "No Text":
				continue
			if not imported:
				from transformers import AutoTokenizer, AutoModelForSequenceClassification
				import torch
				import torch.nn.functional as F
				import re

				# Load the model and tokenizer from local storage
				model = AutoModelForSequenceClassification.from_pretrained("./local_model/")
				tokenizer = AutoTokenizer.from_pretrained("./local_model/")

				def chunk_text(text):
					sentence_pattern = r'(?<=[.!?])\s+'
					sentences = re.split(sentence_pattern, text.strip())
					return sentences

				# Function to get sentiment scores for each chunk
				def analyze_sentiment(text):
					chunks = chunk_text(text)  # Split long text into chunks
					total_neg, total_pos, total_weight = 0, 0, 0  # Accumulate scores

					# Process each chunk
					for chunk in chunks:
						if chunk == "No Text":
							total_neg += 0.5
							total_pos += 0.5
							total_weight += 1
						else:
							inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)
							
							with torch.no_grad():
								outputs = model(**inputs)
								logits = outputs.logits
								probs = F.softmax(logits, dim=-1)
							
							neg_score, pos_score = probs[0].tolist()
							weight = len(chunk.split(" "))
							total_neg += neg_score*weight
							total_pos += pos_score*weight
							total_weight += weight
							print(weight)
							print(f"Chunk: {chunk} | Neg: {neg_score:.4f}, Pos: {pos_score:.4f}")

					# Average the scores over all chunks
					avg_neg = (total_neg / len(chunks)) / (total_weight / len(chunks))
					avg_pos = (total_pos / len(chunks)) / (total_weight / len(chunks))

					return avg_pos, avg_neg

				imported = True

			positive, negative = analyze_sentiment(text)

			with open("files/meta.txt", "a") as f:
				f.write(f"{date} positive:{positive} negative:{negative}\n")

# Main layout of the page
col2 = UI.add_container(col = 8)
col2_largeContainer = col2.add_container(rows = 30, cols = 6, colour = None)
col2_searchLabel = col2_largeContainer.add_text(text = "SEARCH:", bold = True, colour = "Gold", margins = 0, width = 6, verticalAlign = "mid")
col2_searchBox = col2_largeContainer.add_text(text = "", row = 1, margins = 0, width = 6, editable = True, verticalAlign = "mid")
col2_searchLabel = col2_largeContainer.add_text(text = "ENTRIES:", row = 2, bold = True, colour = "Gold", margins = 0, width = 6, verticalAlign = "mid")
col2_list = col2_largeContainer.add_list(searchBox = col2_searchBox, row = 3, rows = 26, height = 26, width = 6, margins = 0, colour = None)
col2_nextButton = col2_largeContainer.add_button(onPress = nextPage, margins = 0, row = 29, col = 3, colour = None).add_image(path = FORWARD_IMAGE, margins = 0).parent
col2_prevButton = col2_largeContainer.add_button(onPress = prevPage, margins = 0, row = 29, col = 2, colour = None).add_image(path = BACK_IMAGE, margins = 0).parent
col2_exitButton = col2_largeContainer.add_button(onPress = quit, margins = 0, row = 29, col = 5, colour = None).add_image(path = EXIT_IMAGE, margins = 0).parent
col2_newButton = col2_largeContainer.add_button(onPress = promptNewEntry, margins = 0, row = 29, col = 0, colour = None).add_image(path = NEW_IMAGE, margins = 0).parent

for path in os.listdir("files/"):
	if path.endswith(".txt") and path != "meta.txt":
		with open(f"files/{path}", "r") as f:
			content = f.read()
		date = path.removesuffix(".txt")
		addPage(date = date, text = content)
col2_list.rePosition()

enablePage(None, pages[-1], None)

# Main loop, most logic happens within UI.tick().
loop = True
while loop:
	clock.tick(30)
	UI.tick()

	for event in pygame.event.get():
		# Exit program
		if event.type == pygame.QUIT:
			loop = False

	win.fill((0,0,0))

	UI.draw()
	pygame.display.update()

pygame.quit()
if sentimentAnalysis:
	setMeta()
