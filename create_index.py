from elasticsearch import Elasticsearch
import elastic_creds
from index_settings import settings 
import argparse
import nipper_lib

query= {
    "query" : {
	        "match_all" : {}
			    }
				}

cla = nipper_lib.parser.parse_args()

if  cla.index_name is None :
	index_name='nipper'
else:
	index_name = cla.index_name

delete_it = cla.delete_index
delete_docs = cla.delete_docs

es = Elasticsearch(elastic_creds.host,httpauth=(elastic_creds.user,elastic_creds.password),port=elastic_creds.port)
print(es.info())


if not es.ping():
    raise ValueError("Can't connect to Elastic")

nipper_lib.initialise_index(es,index_name,delete_it,delete_docs)

