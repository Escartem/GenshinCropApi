from io import BytesIO
from requests import get
from random import randint
from base64 import b64encode
from PIL import Image, ImageOps, ImageDraw, ImageFont


clamp = lambda mn, val, mx: max(mn, min(val, mx))

def fetch_image(url):
	img_blob = get(url).content
	img_object = Image.open(BytesIO(img_blob)).convert("RGBA")

	return img_object

def crop_image(img, crop_data):
	crop = []

	for e in crop_data:
		crop.append(randint(e[0], e[1]))
	
	old_crop = crop.copy()

	crop[2] += crop[0]
	crop[3] += crop[1]

	cropped_img = img.crop(crop)

	return cropped_img, old_crop

def render_image(img):
	imgByteArray = BytesIO()
	img.save(imgByteArray, format="PNG")
	imgByteArray = imgByteArray.getvalue()
	imgData = b64encode(imgByteArray).decode("utf-8")

	return imgData
