import map
import splash
from json_utils import *
from web_data import web_data


def lambda_handler(event, context):
	path = list(filter(None, event["path"].split("/")))[1:]
	
	# char
	if path[0] == "char":
		if path[1] == "gi":
			if event["httpMethod"] == "OPTIONS":
				return {
					'statusCode': 204,
					'headers': {
						'Access-Control-Allow-Origin': '*',
						'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
						'Access-Control-Allow-Headers': 'Content-Type, regions',
						'Access-Control-Allow-Credentials': 'true'  # Optional
					}
				}

			regions = None

			if "regions" in event["headers"]:
				regions = event["headers"]["regions"]

			return splash.ys_gen(regions)
		elif path[1] == "sr":
			return splash.hsr_gen()
	
	# char result
	elif path[:-1]==["result"]:
		rid = event["path"].split("/")[-1]
		
		if rid[0] == "y":
			return splash.gen_result("ys", rid[1:])
		elif rid[0] == "s":
			return splash.gen_result("hsr", rid[1:])
	
	# map
	elif path[:-1]==["map"] or path==["map"]:
		return map.map(path[-1])

	# web data
	elif path==["data"]:
		return web_data(event)
	
	else:
		return message("forbidden")
