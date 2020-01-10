from elasticsearch import Elasticsearch
import elastic_creds
from index_settings import settings 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n","--index_name")

query= {
    "query" : {
	        "match_all" : {}
			    }
				}

cla = parser.parse_args()

if  cla.index_name is None :
	index_name='test-syntax'
else:
	index_name = cla.index_name


es = Elasticsearch(elastic_creds.host,httpauth=(elastic_creds.user,elastic_creds.password),port=elastic_creds.port)
print(es.info())


if not es.ping():
    raise ValueError("Can't connect to Elastic")

if es.indices.exists(index=index_name):
	print("Delete the index")
	response = es.indices.delete(index=index_name,ignore=[400,404])
	if 'error' in response:
		print("failed to delete index ")
		exit()

response = es.indices.create(index=index_name,ignore=400, body=settings)
print(response)
print("created index {}".format(index_name))

