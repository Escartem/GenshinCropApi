from random import choice

from json_utils import *
from image_utils import *


DB_URL = f'{fetch_json("config")["DB_URL"]}/hk4e/map'


def map(id):
	mapVersion = "4.2"
	mapData = fetch_json(mapVersion)

	if id not in list(mapData.keys()):
		return message("unknown index", 404)

	data = mapData[id]
	selected = choice(data["files"])
	
	url = f'{DB_URL}/{data["path"]}/{selected["name"]}'
	img = render_image(fetch_image(url))
	
	headers = default_headers()
	headers.update({
		"index-version": f'{data["game_version"]}-{data["index_version"]}',
		"rx": selected["x"],
		"ry": selected["y"],
		"size": data["size"]
	})
	
	return return_image(headers, img)
