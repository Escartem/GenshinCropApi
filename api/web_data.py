from json_utils import *


def web_data(event):
	data = {}
	query = event["queryStringParameters"]
	version = None

	if "v" in query:
		version = str(query["v"])

	# deprecated
	if version in ["1", "2"]:
		data = fetch_json("gdata_old")[version]
	# live
	elif version == "3":
		# global
		data["data"] = {
			"ver": "3.0.0",
			"paths": {
				"api_base": "https://api.escartem.eu.org/gcrop",
				"char_ys": "char/gi",
				"char_hsr": "char/sr",
				"map_ys": "map",
				"db_base": "https://ua4e.escartem.eu.org",
				"tile_ys": "hk4e/map",
				"cards_ys": "hk4e/face",
				"cards_hsr": "hkrpg/face"
			},
		}
		
		# sr
		data["sr"] = {
			"ver": "2.1.5",
			"chars": apply_override(fetch_json("HSR_v3"))
		}
		
		# ys
		data["ys"] = {
			"ver": "2.4.2",
			"chars": apply_override(fetch_json("YS_v3"))
		}
		
		# map
		mapGameVersion = "4.2"
		indexes = {}
		mapData = fetch_json(mapGameVersion)
		
		for key in mapData:
			index = mapData[key]
			indexes[index["id"]] = {
				"game_version": index["game_version"],
				"index_version": index["index_version"],
				"length": index["length"]
			}

		data["map"] = {
			"ver": "1.4.0",
			"indexes": indexes
		}
		
		# message
		data["notification"] = ""

	if data == {}:
		return message("missing or invalid version", 404)
	
	return message(data, 200, True)
