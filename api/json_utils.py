from time import time
from base64 import b64encode
from json import loads, dumps


# main api version stored here
VERSION = "2.0.0"


def fetch_json(name):
	with open(f"data/{name}.json", "r") as f:
		data = loads(f.read())
		f.close()
	return data

def apply_override(data):
	overrides = data["OVERRIDES"]

	for char in overrides["CHARS_RENAMES"]:
		data[char[1]] = data[char[0]].copy()
		data.pop(char[0])

	for char in overrides["CHARS_EXCLUDES"]:
		data.pop(char)
	
	for char in overrides["NAMES_EXCLUDES"]:
		temp = data[char[0]][0]
		for name in char[1]:
			temp.pop(temp.index(name))
	
	data.pop("OVERRIDES")
	data = dict(sorted(data.items()))

	return data

def encode_data(data):
	if type(data) == dict:
		data = dumps(data)
	encoded_dict = b64encode(data.encode("utf-8")).decode("utf-8")

	return encoded_dict

def default_headers():
	headers = {
		"Content-Type": "image/png",
		"Cache-Control": "private, max-age=0, no-cache",
		"Access-Control-Allow-Origin": "*",
		"Access-Control-Expose-Headers": "*",
		"version": VERSION
	}
	
	return headers

def create_splash_headers(char, crop, aliases, result):
	uid = {
		"s": char,
		"c": crop,
		"t": time()
	}

	encoded_uid = encode_data(uid)

	alias = ".".join([elem.lower() for elem in aliases])
	
	headers = default_headers()

	headers.update({
		"uid": encoded_uid,
		"char": char,
		"display": aliases[0],
		"alias": alias,
		"result": result
	})

	return headers

def create_result_url(game, char, crop):
	result_data = f'{char}.{crop[0]}.{crop[1]}.{crop[2]}.{crop[3]}'
	result_url = f"https://api.escartem.eu.org/gcrop/result/{game}{encode_data(result_data)}"

	return result_url

def return_image(headers, image):
	return {
		"headers": headers,
		"statusCode": 200,
		"body": image,
		"isBase64Encoded": True
	}

def message(msg, code=403, override=False):
	return {
		"statusCode": code,
		"headers": {"Access-Control-Allow-Origin": "*"},
		"body": dumps({"message": msg}) if not override else dumps(msg)
	}
