import requests,os,json,time
from elasticsearch import Elasticsearch

directory='.'


i =1

for filename in os.listdir(directory):
	if filename.endswith('.json'):
		with open(filename) as fn:
			print(filename)
			for line in fn:
				js=json.loads(line)
				if 'findings' in js:
					js['findings'] = {}
					print(js['findings'])

