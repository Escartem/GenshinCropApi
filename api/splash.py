from base64 import b64decode
from random import choice, randint

from json_utils import *
from image_utils import *


DB_URL = "https://bluedb.escartem.eu.org/gcrop"


def gen(json_file, game, crop_data):
	# choose char
	all_characters = fetch_json(json_file)
	curr_char = choice(list(all_characters)[:-1])

	# char meta
	# TODO: ignore overrides
	aliases = all_characters[curr_char][0]
	aliases = [aliases] if type(aliases) != list else aliases

	# prepare img
	file_format = "png" if game[0] == "ys" else "webp"
	char_img = fetch_image(f"{DB_URL}/{game[0]}/splash/{curr_char}.{file_format}")
	char_size = char_img.size
	
	# bad crop override as in this is a bad way to do this
	if game[0] == "ys":
		crop_data[0] = (crop_data[0][0], char_size[0]-crop_data[0][0])
		crop_data[1] = (crop_data[1][0], char_size[1]-crop_data[1][0])

	cropped_img, crop = crop_image(char_img, crop_data)

	# prepare response
	rendered_img = render_image(cropped_img)
	result_url = create_result_url(game[1], curr_char, crop)
	headers = create_splash_headers(curr_char, crop_data, aliases, result_url)
	
	return return_image(headers, rendered_img)

def ys_gen():
	# this is bad
	crop_data = [
		(270, 0),
		(320, 0),
		(100, 150),
		(100, 200)
	]
	
	return gen("YS_v3", ["ys", "y"], crop_data)

def hsr_gen():
	crop_data = [
		(450, 1598),
		(450, 1498),
		(100, 150),
		(100, 300)
	]
	
	return gen("HSR_v3", ["hsr", "s"], crop_data)

def gen_result(game, result):
	rid = b64decode(result).decode("utf-8").split(".")

	file_format = "png" if game == "ys" else "webp"
	char_url = f"{DB_URL}/{game}/splash/{rid[0]}.{file_format}"

	result_img = fetch_image(char_url)

	sizes = [result_img.size[0], result_img.size[1]]
	
	# i mean why not
	posX = int(rid[1])
	posY = int(rid[2])
	sizeX = int(rid[3])
	sizeY = int(rid[4])
	
	crop_data = [
		clamp(0, posX-sizeX, sizes[0]),
		clamp(0, posY-sizeY, sizes[1]),
		clamp(0, posX+2*sizeX, sizes[0]),
		clamp(0, posY+2*sizeY, sizes[1])
	]
	
	# left bottom right top
	Adraw = ImageDraw.Draw(result_img)
	w=5
	Adraw.line((posX, posY, posX, posY+sizeY), fill="red", width=w)
	Adraw.line((posX, posY+sizeY, posX+sizeX, posY+sizeY), fill="red", width=w)
	Adraw.line((posX+sizeX, posY+sizeY, posX+sizeX, posY), fill="red", width=w)
	Adraw.line((posX+sizeX, posY, posX, posY), fill="red", width=w)
	
	result_img = result_img.crop(crop_data)
	
	return return_image(default_headers(), render_image(result_img))
